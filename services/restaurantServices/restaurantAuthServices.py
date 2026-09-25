import hashlib
import os

import database.connection as connection


def _hash_password(password):
    salt = os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt.hex() + ":" + derived_key.hex()


def verify_password(plain_password, stored_password):
    if not stored_password:
        return False

    if ":" not in stored_password:
        return plain_password == stored_password

    salt_hex, hashed_password = stored_password.split(":", 1)
    try:
        salt = bytes.fromhex(salt_hex)
        derived_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100_000)
        return hashed_password == derived_key.hex()
    except ValueError:
        return plain_password == stored_password


def isIdTaken(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception:
        return False


def createRestaurant(name, address, contact_number, user_id, recovery_email, password):
    try:
        if not user_id or not password:
            return {"success": False, "message": "Restaurant ID and password are required."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {"success": False, "message": "Restaurant already exists with this ID. Please choose another one."}

        hashed_password = _hash_password(password)
        cursor.execute(
            """
            INSERT INTO users (id, password, role, name, address, contact_number, recovery_email, balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, hashed_password, "restaurant", name, address, contact_number, recovery_email, 0.00),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Restaurant registration successful."}
    except Exception as exc:
        return {"success": False, "message": f"Error while creating restaurant: {exc}"}


def getRestaurantById(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, name, address, contact_number, recovery_email, role, balance
            FROM users
            WHERE id = %s AND role = %s
            """,
            (user_id, "restaurant"),
        )
        restaurant = cursor.fetchone()
        cursor.close()
        conn.close()

        if not restaurant:
            return {"success": False, "message": "Restaurant not found."}

        return {"success": True, "restaurant": restaurant}
    except Exception as exc:
        return {"success": False, "message": f"Error while fetching restaurant: {exc}"}


def updateRestaurantProfile(user_id, field_name, new_value):
    allowed_fields = {"name", "address", "contact_number", "recovery_email"}
    if field_name not in allowed_fields:
        return {"success": False, "message": "This field cannot be edited."}

    try:
        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET {field_name} = %s WHERE id = %s AND role = %s",
            (new_value, user_id, "restaurant"),
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return {"success": False, "message": "Profile update failed. Restaurant not found."}

        return {"success": True, "message": "Profile updated successfully."}
    except Exception as exc:
        return {"success": False, "message": f"Error while updating profile: {exc}"}


def loginRestaurant(user_id, password):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, password FROM users WHERE id = %s AND role = %s",
            (user_id, "restaurant"),
        )
        restaurant = cursor.fetchone()
        cursor.close()
        conn.close()

        if not restaurant:
            return False

        return verify_password(password, restaurant["password"])
    except Exception:
        return False
