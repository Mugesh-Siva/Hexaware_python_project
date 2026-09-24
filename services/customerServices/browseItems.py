import database.connection as connection


def get_menu_page(page_number=0, page_size=10):
    try:
        offset = page_number * page_size
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_id, title, description, price, nutrients, availability, user_id
            FROM menus
            WHERE availability = 1
            ORDER BY menu_id
            LIMIT %s OFFSET %s
            """,
            (page_size, offset),
        )

        items = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM menus WHERE availability = 1")
        total_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "success": True,
            "items": items,
            "total_count": total_count,
        }

    except Exception as exc:
        return {
            "success": False,
            "message": f"Error while fetching menu items: {exc}",
            "items": [],
            "total_count": 0,
        }


def add_item_to_cart(user_id, menu_id, quantity):
    try:
        menu_id = int(menu_id)
        quantity = int(quantity)

        if quantity <= 0:
            return {"success": False, "message": "Quantity must be greater than 0."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_id, title, user_id, price, availability
            FROM menus
            WHERE menu_id = %s
            """,
            (menu_id,),
        )
        menu = cursor.fetchone()

        if not menu:
            cursor.close()
            conn.close()
            return {"success": False, "message": "Item not found."}

        if menu[4] != 1:
            cursor.close()
            conn.close()
            return {"success": False, "message": "This item is currently unavailable."}

        cursor.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if not cart:
            cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
            cart_id = cursor.lastrowid
        else:
            cart_id = cart[0]

        cursor.execute(
            """
            SELECT cart_item_id, quantity
            FROM cart_items
            WHERE cart_id = %s AND menu_id = %s
            """,
            (cart_id, menu_id),
        )
        cart_item = cursor.fetchone()

        if cart_item:
            new_quantity = cart_item[1] + quantity
            cursor.execute(
                "UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s",
                (new_quantity, cart_item[0]),
            )
        else:
            cursor.execute(
                """
                INSERT INTO cart_items (cart_id, menu_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (cart_id, menu_id, quantity),
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "success": True,
            "message": f"Added {quantity} x {menu[1]} to cart.",
        }

    except ValueError:
        return {"success": False, "message": "Invalid quantity. Please enter a positive integer."}
    except Exception as exc:
        return {"success": False, "message": f"Error while adding to cart: {exc}"}
