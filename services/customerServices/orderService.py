from collections import defaultdict

import database.connection as connection
from services.customerServices.cart import get_cart
from utils.log_config import logger


def get_checkout_summary(user_id):
    cart_result = get_cart(user_id)
    if not cart_result["success"]:
        logger.warning(f"Checkout failed for {user_id}: cart could not be loaded")
        return {"success": False, "message": cart_result.get("message", "Cart could not be loaded."), "items": [], "total": 0.0}

    items = cart_result.get("items", [])
    total = float(cart_result.get("total", 0.0) or 0.0)

    if not items:
        logger.info(f"Customer {user_id} checked out empty cart")
        return {"success": False, "message": "Your cart is empty.", "items": [], "total": 0.0}

    logger.info(f"Customer {user_id} viewed checkout summary with total {total}")
    return {"success": True, "message": "Cart summary loaded successfully.", "items": items, "total": total}


def get_customer_orders(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT o.order_id, o.status, o.total_price, o.created_at,
                   oi.order_item_id, oi.menu_id, oi.quantity, oi.price_at_order,
                   m.title, m.user_id AS restaurant_id
            FROM orders o
            INNER JOIN order_items oi ON oi.order_id = o.order_id
            INNER JOIN menus m ON m.menu_id = oi.menu_id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC, o.order_id DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        grouped = defaultdict(list)
        for row in rows:
            grouped[row["order_id"]].append(row)

        orders = []
        for order_id, order_rows in grouped.items():
            first_row = order_rows[0]
            item_list = []
            for row in order_rows:
                item_list.append(
                    {
                        "menu_id": row["menu_id"],
                        "title": row["title"],
                        "quantity": int(row["quantity"]),
                        "price_at_order": float(row["price_at_order"]),
                    }
                )

            orders.append(
                {
                    "order_id": order_id,
                    "status": first_row["status"],
                    "total_price": float(first_row["total_price"]),
                    "created_at": first_row["created_at"],
                    "items": item_list,
                }
            )

        logger.info(f"Customer {user_id} opened order history with {len(orders)} orders")
        return {"success": True, "orders": orders}
    except Exception as exc:
        logger.error(f"Error while fetching customer orders for {user_id}: {exc}")
        return {"success": False, "message": f"Error while fetching orders: {exc}", "orders": []}


def place_order_from_cart(user_id, payment_method, payment_details=None):
    try:
        cart_result = get_cart(user_id)
        if not cart_result["success"]:
            logger.warning(f"Order failed for {user_id}: cart could not be loaded")
            return {"success": False, "message": cart_result.get("message", "Cart could not be loaded.")}

        items = cart_result.get("items", [])
        if not items:
            logger.info(f"Customer {user_id} tried to place empty order")
            return {"success": False, "message": "Your cart is empty. Nothing to order."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart_row = cursor.fetchone()
        if not cart_row:
            cursor.close()
            conn.close()
            logger.warning(f"Order failed: cart not found for {user_id}")
            return {"success": False, "message": "Cart not found."}

        cart_id = cart_row[0]

        grouped_items = defaultdict(list)
        for item in items:
            menu_id = int(item["menu_id"])
            cursor.execute(
                "SELECT user_id, title, price FROM menus WHERE menu_id = %s",
                (menu_id,),
            )
            menu_row = cursor.fetchone()
            if not menu_row:
                continue
            restaurant_id = menu_row[0]
            grouped_items[restaurant_id].append(
                {
                    "menu_id": menu_id,
                    "title": menu_row[1],
                    "price": float(menu_row[2]),
                    "quantity": int(item["quantity"]),
                }
            )

        created_orders = []

        for restaurant_id, restaurant_items in grouped_items.items():
            order_total = sum((item["price"] * item["quantity"]) for item in restaurant_items)
            cursor.execute(
                "INSERT INTO orders (user_id, status, total_price) VALUES (%s, %s, %s)",
                (user_id, "ordered", order_total),
            )
            order_id = cursor.lastrowid

            for item in restaurant_items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, menu_id, quantity, price_at_order)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order_id, item["menu_id"], item["quantity"], item["price"]),
                )

            created_orders.append(
                {
                    "restaurant_id": restaurant_id,
                    "order_id": order_id,
                    "total_price": order_total,
                }
            )

        if created_orders:
            cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
            conn.commit()

        cursor.close()
        conn.close()

        logger.info(f"Customer {user_id} placed order successfully using {payment_method}")
        return {
            "success": True,
            "message": "Order placed successfully.",
            "payments": {"method": payment_method, "details": payment_details},
            "orders": created_orders,
        }
    except Exception as exc:
        logger.error(f"Error while placing order for {user_id}: {exc}")
        return {"success": False, "message": f"Error while placing order: {exc}"}
