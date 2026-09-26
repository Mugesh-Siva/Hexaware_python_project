import database.connection as connection
from utils.log_config import logger


def addMenu(user_id, title, description, price, nutrients, role=None):
    try:
        title = (title or "").strip()
        description = (description or "").strip()
        nutrients = (nutrients or "").strip()

        if not title:
            logger.warning(f"Restaurant {user_id} tried to add a menu without a title")
            return {"success": False, "message": "Menu title cannot be empty."}

        if not price:
            logger.warning(f"Restaurant {user_id} tried to add a menu without price")
            return {"success": False, "message": "Price cannot be empty."}

        price = float(price)
        if price < 0:
            logger.warning(f"Restaurant {user_id} tried to add a negative price: {price}")
            return {"success": False, "message": "Price cannot be negative."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        query = """
            INSERT INTO menus (user_id, title, description, price, nutrients)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (user_id, title, description, price, nutrients))
        conn.commit()

        menu_id = cursor.lastrowid
        cursor.close()
        conn.close()

        logger.info(f"Restaurant {user_id} added menu {title} with ID {menu_id}")
        return {
            "success": True,
            "message": "Menu added successfully",
            "menu_id": menu_id,
        }

    except ValueError:
        logger.warning(f"Restaurant {user_id} entered invalid price while adding menu")
        return {"success": False, "message": "Invalid price. Please enter a number."}
    except Exception as exc:
        logger.error(f"Error while adding menu for restaurant {user_id}: {exc}")
        return {"success": False, "message": f"Error occurred while adding menu: {exc}"}