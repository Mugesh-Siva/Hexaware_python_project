import database.connection as connection


def get_hotbite_balance(user_id):
    try:
        conn = connection.createConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return 0.0

        return float(row.get("balance") or 0.0)
    except Exception:
        return 0.0


def add_hotbite_balance(user_id, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return {"success": False, "message": "Top-up amount must be greater than 0."}

        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE id = %s",
            (amount, user_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "success": True,
            "message": f"Hotbite balance topped up successfully by ₹{amount:.2f}.",
        }
    except ValueError:
        return {"success": False, "message": "Invalid amount. Please enter a valid number."}
    except Exception as exc:
        return {"success": False, "message": f"Error while topping up Hotbite balance: {exc}"}


def deduct_hotbite_balance(user_id, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return {"success": False, "message": "Amount must be greater than 0."}

        conn = connection.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET balance = balance - %s WHERE id = %s AND balance >= %s",
            (amount, user_id, amount),
        )
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        if affected == 0:
            return {"success": False, "message": "Insufficient balance."}

        return {"success": True, "message": "Hotbite balance used successfully."}
    except ValueError:
        return {"success": False, "message": "Invalid amount. Please enter a valid number."}
    except Exception as exc:
        return {"success": False, "message": f"Error while deducting Hotbite balance: {exc}"}
