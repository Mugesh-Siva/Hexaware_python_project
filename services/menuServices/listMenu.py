import database.connection as connection
from utils.log_config import logger


def getMenusByRestaurant(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_id, title, description, availability, price, nutrients, created_at
            FROM menus
            WHERE user_id = %s
            ORDER BY menu_id ASC
            """,
            (user_id,),
        )

        menus = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Restaurant {user_id} opened menu list with {len(menus)} items")
        return {
            "success": True,
            "message": "Menus fetched successfully",
            "menus": menus,
        }

    except Exception as exc:
        logger.error(f"Error while fetching menus for restaurant {user_id}: {exc}")
        return {
            "success": False,
            "message": f"Error occurred while fetching menus: {exc}",
            "menus": [],
        }
