import database.connection as connection


def getMenuForRestaurant(user_id, menu_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_id, title
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

        return {"success": True, "message": "Menu loaded successfully", "menu": menu}

    except Exception as exc:
        return {"success": False, "message": f"Error occurred while loading menu: {exc}"}


def deleteMenu(user_id, menu_id):
    try:
        menu_id = int(menu_id)

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM menus
            WHERE menu_id = %s AND user_id = %s
            """,
            (menu_id, user_id),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True, "message": "Menu deleted successfully"}

    except ValueError:
        return {"success": False, "message": "Invalid Menu ID. Please enter a number."}
    except Exception as exc:
        return {"success": False, "message": f"Error occurred while deleting menu: {exc}"}