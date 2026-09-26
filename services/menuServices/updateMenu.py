import database.connection as connection
from utils.log_config import logger


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
            logger.warning(f"Restaurant {user_id} tried to open missing menu {menu_id}")
            return {"success": False, "message": "Menu not found or does not belong to your restaurant."}

        logger.info(f"Restaurant {user_id} opened menu {menu_id} for editing")
        return {
            "success": True,
            "message": "Menu loaded successfully",
            "menu": menu,
        }

    except Exception as exc:
        logger.error(f"Error while loading menu {menu_id} for restaurant {user_id}: {exc}")
        return {"success": False, "message": f"Error occurred while loading menu: {exc}"}


def updateMenu(user_id, menu_id, title, description, availability, price, nutrients):
    try:
        menu_id = int(menu_id)
        title = (title or "").strip()
        description = (description or "").strip()
        nutrients = (nutrients or "").strip()

        if not title:
            logger.warning(f"Restaurant {user_id} tried to update menu {menu_id} without a title")
            return {"success": False, "message": "Title cannot be empty."}

        if availability not in (0, 1, "0", "1"):
            logger.warning(f"Restaurant {user_id} sent invalid availability for menu {menu_id}: {availability}")
            return {"success": False, "message": "Availability must be 0 or 1."}

        availability = int(availability)

        if price == "":
            logger.warning(f"Restaurant {user_id} left price empty while updating menu {menu_id}")
            return {"success": False, "message": "Price cannot be empty."}

        price = float(price)
        if price < 0:
            logger.warning(f"Restaurant {user_id} set negative price for menu {menu_id}: {price}")
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

        logger.info(f"Restaurant {user_id} updated menu {menu_id}")
        return {"success": True, "message": "Menu updated successfully"}

    except ValueError:
        logger.warning(f"Restaurant {user_id} entered invalid values while updating menu {menu_id}")
        return {"success": False, "message": "Invalid input. Please check Menu ID, price, or availability."}
    except Exception as exc:
        logger.error(f"Error while updating menu {menu_id} for restaurant {user_id}: {exc}")
        return {"success": False, "message": f"Error occurred while updating menu: {exc}"}