import database.connection as connection
from utils.log_config import logger


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
            logger.warning(f"Restaurant {user_id} tried to open missing menu {menu_id}")
            return {"success": False, "message": "Menu not found or does not belong to your restaurant."}

        logger.info(f"Restaurant {user_id} opened menu {menu_id} details")
        return {"success": True, "message": "Menu loaded successfully", "menu": menu}

    except Exception as exc:
        logger.error(f"Error while loading menu {menu_id} for restaurant {user_id}: {exc}")
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

        logger.info(f"Restaurant {user_id} deleted menu {menu_id}")
        return {"success": True, "message": "Menu deleted successfully"}

    except ValueError:
        logger.warning(f"Restaurant {user_id} entered invalid menu ID while deleting: {menu_id}")
        return {"success": False, "message": "Invalid Menu ID. Please enter a number."}
    except Exception as exc:
        logger.error(f"Error while deleting menu {menu_id} for restaurant {user_id}: {exc}")
        return {"success": False, "message": f"Error occurred while deleting menu: {exc}"}