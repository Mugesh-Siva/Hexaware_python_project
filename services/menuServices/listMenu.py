import database.connection as connection


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

        return {
            "success": True,
            "message": "Menus fetched successfully",
            "menus": menus,
        }

    except Exception as exc:
        return {
            "success": False,
            "message": f"Error occurred while fetching menus: {exc}",
            "menus": [],
        }
