import database.connection as connection


def addMenu(user_id, title, description, price, nutrients, role=None):
    try:
        title = (title or "").strip()
        description = (description or "").strip()
        nutrients = (nutrients or "").strip()

        if not title:
            return {"success": False, "message": "Menu title cannot be empty."}

        if not price:
            return {"success": False, "message": "Price cannot be empty."}

        price = float(price)
        if price < 0:
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

        return {
            "success": True,
            "message": "Menu added successfully",
            "menu_id": menu_id,
        }

    except ValueError:
        return {"success": False, "message": "Invalid price. Please enter a number."}
    except Exception as exc:
        return {"success": False, "message": f"Error occurred while adding menu: {exc}"}