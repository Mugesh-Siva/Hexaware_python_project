import database.connection as connection
from utils.log_config import logger


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

        logger.info(f"Customer opened menu page {page_number} with {len(items)} items")
        return {
            "success": True,
            "items": items,
            "total_count": total_count,
        }

    except Exception as exc:
        logger.error(f"Menu page error: {exc}")
        return {
            "success": False,
            "message": f"Error while fetching menu items: {exc}",
            "items": [],
            "total_count": 0,
        }


def search_menu_items(search_term, page_number=0, page_size=10):
    try:
        term = str(search_term or "").strip()
        if not term:
            logger.warning("Customer search failed: empty search term")
            return {"success": False, "message": "Search term is required.", "items": [], "total_count": 0}

        conn = connection.createConnection()
        cursor = conn.cursor()

        like_pattern = f"%{term}%"
        cursor.execute(
            """
            SELECT menu_id, title, description, price, nutrients, availability, user_id
            FROM menus
            WHERE availability = 1 AND title LIKE %s
            ORDER BY menu_id
            LIMIT %s OFFSET %s
            """,
            (like_pattern, page_size, page_number * page_size),
        )
        items = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) FROM menus WHERE availability = 1 AND title LIKE %s",
            (like_pattern,),
        )
        total_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        logger.info(f"Customer searched for '{term}' and got {len(items)} matches")
        return {
            "success": True,
            "items": items,
            "total_count": total_count,
            "search_term": term,
        }
    except Exception as exc:
        logger.error(f"Search menu error for '{search_term}': {exc}")
        return {
            "success": False,
            "message": f"Error while searching menu: {exc}",
            "items": [],
            "total_count": 0,
        }


def add_item_to_cart(user_id, menu_id, quantity):
    try:
        menu_id = int(menu_id)
        quantity = int(quantity)

        if quantity <= 0:
            logger.warning(f"Customer {user_id} tried to add invalid quantity {quantity} to cart")
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
            logger.warning(f"Customer {user_id} tried to add missing menu {menu_id} to cart")
            return {"success": False, "message": "Item not found."}

        if menu[4] != 1:
            cursor.close()
            conn.close()
            logger.warning(f"Customer {user_id} tried to add unavailable menu {menu_id} to cart")
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

        logger.info(f"Customer {user_id} added {quantity} of menu {menu_id} to cart")
        return {
            "success": True,
            "message": f"Added {quantity} x {menu[1]} to cart.",
        }

    except ValueError:
        logger.warning(f"Customer {user_id} entered invalid quantity while adding to cart")
        return {"success": False, "message": "Invalid quantity. Please enter a positive integer."}
    except Exception as exc:
        logger.error(f"Error while adding item to cart for {user_id}: {exc}")
        return {"success": False, "message": f"Error while adding to cart: {exc}"}
