import hashlib
import os

import database.connection as connection
from utils.log_config import logger


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


def createCustomer(name, address, contact_number, user_id, recovery_email, password):
    try:
        if not user_id or not password:
            logger.warning("Customer registration failed: user ID or password is empty.")
            return {"success": False, "message": "User ID and password are required."}

        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            logger.warning(f"Customer registration failed: duplicate ID {user_id}")
            return {"success": False, "message": "User already exists with this ID. Please choose another one."}

        hashed_password = _hash_password(password)
        cursor.execute(
            """
            INSERT INTO users (id, password, role, name, address, contact_number, recovery_email, balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, hashed_password, "customer", name, address, contact_number, recovery_email, 0.00),
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Customer account created successfully: {user_id}")
        return {"success": True, "message": "User registration successful."}
    except Exception as exc:
        logger.error(f"Customer registration error for {user_id}: {exc}")
        return {"success": False, "message": f"Error while creating customer: {exc}"}


def getCustomerById(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, name, address, contact_number, recovery_email, role, balance
            FROM users
            WHERE id = %s AND role = %s
            """,
            (user_id, "customer"),
        )
        customer = cursor.fetchone()
        cursor.close()
        conn.close()

        if not customer:
            logger.warning(f"Customer profile request failed: {user_id} not found")
            return {"success": False, "message": "Customer not found."}

        logger.info(f"Customer profile opened for: {user_id}")
        return {"success": True, "customer": customer}
    except Exception as exc:
        logger.error(f"Error while reading customer {user_id}: {exc}")
        return {"success": False, "message": f"Error while fetching customer: {exc}"}


def updateCustomerProfile(user_id, field_name, new_value):
    allowed_fields = {"name", "address", "contact_number", "recovery_email"}
    if field_name not in allowed_fields:
        logger.warning(f"Customer profile update failed for {user_id}: invalid field {field_name}")
        return {"success": False, "message": "This field cannot be edited."}

    try:
        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET {field_name} = %s WHERE id = %s AND role = %s",
            (new_value, user_id, "customer"),
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            logger.warning(f"Customer profile update failed: customer {user_id} not found")
            return {"success": False, "message": "Profile update failed. Customer not found."}

        logger.info(f"Customer profile updated: {user_id} -> {field_name}")
        return {"success": True, "message": "Profile updated successfully."}
    except Exception as exc:
        logger.error(f"Error while updating customer profile {user_id}: {exc}")
        return {"success": False, "message": f"Error while updating profile: {exc}"}


def loginCustomer(user_id, password):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, password FROM users WHERE id = %s AND role = %s",
            (user_id, "customer"),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            logger.warning(f"Customer login failed: user {user_id} not found")
            return False

        result = verify_password(password, user["password"])
        if result:
            logger.info(f"Customer login success: {user_id}")
        else:
            logger.warning(f"Customer login failed: wrong password for {user_id}")
        return result
    except Exception as exc:
        logger.error(f"Customer login error for {user_id}: {exc}")
        return False
