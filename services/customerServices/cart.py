import database.connection as connection
from utils.log_config import logger


def get_cart(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if not cart:
            cursor.close()
            conn.close()
            logger.info(f"Customer {user_id} opened empty cart")
            return {"success": True, "items": [], "total": 0.0}

        cart_id = cart[0]
        cursor.execute(
            """
            SELECT ci.cart_item_id, m.menu_id, m.title, m.price, ci.quantity,
                   (m.price * ci.quantity) AS subtotal
            FROM cart_items ci
            INNER JOIN menus m ON ci.menu_id = m.menu_id
            WHERE ci.cart_id = %s
            ORDER BY m.menu_id
            """,
            (cart_id,),
        )

        rows = cursor.fetchall()
        items = []
        total = 0.0

        for row in rows:
            subtotal = float(row[3]) * int(row[4])
            total += subtotal
            items.append(
                {
                    "cart_item_id": row[0],
                    "menu_id": row[1],
                    "title": row[2],
                    "price": float(row[3]),
                    "quantity": int(row[4]),
                    "subtotal": subtotal,
                }
            )

        cursor.close()
        conn.close()

        logger.info(f"Customer {user_id} checked cart with {len(items)} items")
        return {"success": True, "items": items, "total": total}

    except Exception as exc:
        logger.error(f"Customer cart error for {user_id}: {exc}")
        return {"success": False, "message": f"Error while loading cart: {exc}", "items": [], "total": 0.0}


def update_cart_quantity(cart_item_id, new_quantity):
    try:
        cart_item_id = int(cart_item_id)
        new_quantity = int(new_quantity)

        if new_quantity <= 0:
            return remove_cart_item(cart_item_id)

        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s",
            (new_quantity, cart_item_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Cart item {cart_item_id} quantity changed to {new_quantity}")
        return {"success": True, "message": "Cart item updated successfully."}

    except ValueError:
        logger.warning(f"Invalid cart quantity entered for item {cart_item_id}")
        return {"success": False, "message": "Invalid quantity. Please enter a positive integer."}
    except Exception as exc:
        logger.error(f"Error while updating cart item {cart_item_id}: {exc}")
        return {"success": False, "message": f"Error while updating cart item: {exc}"}


def remove_cart_item(cart_item_id):
    try:
        cart_item_id = int(cart_item_id)

        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE cart_item_id = %s", (cart_item_id,))
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Cart item {cart_item_id} removed from cart")
        return {"success": True, "message": "Item removed from cart."}

    except ValueError:
        logger.warning(f"Invalid cart item number entered: {cart_item_id}")
        return {"success": False, "message": "Invalid item number."}
    except Exception as exc:
        logger.error(f"Error while removing cart item {cart_item_id}: {exc}")
        return {"success": False, "message": f"Error while removing item: {exc}"}
