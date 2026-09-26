import database.connection as connection
from utils.log_config import logger

VALID_ORDER_STATUSES = (
    "ordered",
    "cooked",
    "packed",
    "out_of_delivery",
    "received",
)


def get_orders_for_restaurant(restaurant_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                o.order_id,
                o.user_id,
                u.name AS customer_name,
                o.status,
                o.total_price,
                o.created_at,
                oi.order_item_id,
                oi.menu_id,
                oi.quantity,
                oi.price_at_order,
                m.title AS menu_title
            FROM orders o
            INNER JOIN order_items oi ON oi.order_id = o.order_id
            INNER JOIN menus m ON m.menu_id = oi.menu_id
            INNER JOIN users u ON u.id = o.user_id
            WHERE m.user_id = %s
            ORDER BY o.created_at DESC, o.order_id DESC
            """,
            (restaurant_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        grouped = {}
        for row in rows:
            order_id = row["order_id"]
            if order_id not in grouped:
                grouped[order_id] = {
                    "order_id": order_id,
                    "customer_id": row["user_id"],
                    "customer_name": row["customer_name"] or row["user_id"],
                    "status": row["status"],
                    "total_price": float(row["total_price"]),
                    "created_at": row["created_at"],
                    "items": [],
                }

            grouped[order_id]["items"].append(
                {
                    "order_item_id": row["order_item_id"],
                    "menu_id": row["menu_id"],
                    "title": row["menu_title"],
                    "quantity": int(row["quantity"]),
                    "price_at_order": float(row["price_at_order"]),
                }
            )

        order_list = list(grouped.values())
        logger.info(f"Restaurant {restaurant_id} opened order list with {len(order_list)} orders")
        return {"success": True, "message": "Orders loaded successfully.", "orders": order_list}

    except Exception as exc:
        logger.error(f"Error while loading restaurant orders for {restaurant_id}: {exc}")
        return {"success": False, "message": f"Error while loading restaurant orders: {exc}", "orders": []}


def update_order_status(order_id, restaurant_id, new_status):
    try:
        order_id = int(order_id)
        if new_status not in VALID_ORDER_STATUSES:
            logger.warning(f"Restaurant {restaurant_id} tried invalid status: {new_status}")
            return {"success": False, "message": "Invalid order status selected."}

        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE orders o
            INNER JOIN order_items oi ON oi.order_id = o.order_id
            INNER JOIN menus m ON m.menu_id = oi.menu_id
            SET o.status = %s
            WHERE o.order_id = %s AND m.user_id = %s
            """,
            (new_status, order_id, restaurant_id),
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            logger.warning(f"Restaurant {restaurant_id} could not update order {order_id}")
            return {"success": False, "message": "Order not found for this restaurant."}

        logger.info(f"Restaurant {restaurant_id} updated order {order_id} status to {new_status}")
        return {"success": True, "message": "Order status updated successfully."}
    except ValueError:
        logger.warning(f"Restaurant {restaurant_id} entered invalid order ID: {order_id}")
        return {"success": False, "message": "Invalid order ID. Please enter a number."}
    except Exception as exc:
        logger.error(f"Error while updating order status for restaurant {restaurant_id}: {exc}")
        return {"success": False, "message": f"Error while updating order status: {exc}"}
