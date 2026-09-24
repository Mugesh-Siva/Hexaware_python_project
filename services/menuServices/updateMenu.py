import database.connection as connection


def getMenuForRestaurant(user_id, menu_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_id, title, description, availability, price, nutrients
            FROM menus
            WHERE menu_id = %s AND user_id = %s
            """,
            (menu_id, user_id),
        )

        menu = cursor.fetchone()
        cursor.close()
        conn.close()

        if not menu:
            return {"success": False, "message": "Menu not found or does not belong to your restaurant."}

        return {
            "success": True,
            "message": "Menu loaded successfully",
            "menu": menu,
        }

    except Exception as exc:
        return {"success": False, "message": f"Error occurred while loading menu: {exc}"}


def updateMenu(user_id, menu_id, title, description, availability, price, nutrients):
    try:
        menu_id = int(menu_id)
        title = (title or "").strip()
        description = (description or "").strip()
        nutrients = (nutrients or "").strip()

        if not title:
            return {"success": False, "message": "Title cannot be empty."}

        if availability not in (0, 1, "0", "1"):
            return {"success": False, "message": "Availability must be 0 or 1."}

        availability = int(availability)

        if price == "":
            return {"success": False, "message": "Price cannot be empty."}

        price = float(price)
        if price < 0:
            return {"success": False, "message": "Price cannot be negative."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE menus
            SET title = %s,
                description = %s,
                availability = %s,
                price = %s,
                nutrients = %s
            WHERE menu_id = %s AND user_id = %s
            """,
            (title, description, availability, price, nutrients, menu_id, user_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True, "message": "Menu updated successfully"}

    except ValueError:
        return {"success": False, "message": "Invalid input. Please check Menu ID, price, or availability."}
    except Exception as exc:
        return {"success": False, "message": f"Error occurred while updating menu: {exc}"}