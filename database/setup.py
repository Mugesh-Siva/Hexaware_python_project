import database.connection as connection


def _add_missing_column(cursor, column_name, definition):
    cursor.execute("SHOW COLUMNS FROM users LIKE %s", (column_name,))
    if cursor.fetchone() is None:
        cursor.execute(f"ALTER TABLE users ADD COLUMN {definition}")


def setupDatabase():
    try:
        if not connection.createDatabaseIfNotExists():
            return False
        conn = connection.createConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                name VARCHAR(100) DEFAULT NULL,
                address VARCHAR(255) DEFAULT NULL,
                contact_number VARCHAR(30) DEFAULT NULL,
                recovery_email VARCHAR(255) DEFAULT NULL,
                balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
            )
            """
        )

        _add_missing_column(cursor, "name", "name VARCHAR(100) NULL")
        _add_missing_column(cursor, "address", "address VARCHAR(255) NULL")
        _add_missing_column(cursor, "contact_number", "contact_number VARCHAR(30) NULL")
        _add_missing_column(cursor, "recovery_email", "recovery_email VARCHAR(255) NULL")
        _add_missing_column(cursor, "balance", "balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS menus (
                menu_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                title VARCHAR(100) NOT NULL,
                description VARCHAR(300),
                availability TINYINT(1) NOT NULL DEFAULT 1,
                price DECIMAL(10, 2) NOT NULL,
                nutrients VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS carts (
                cart_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        try:
            cursor.execute("ALTER TABLE carts ADD UNIQUE (user_id)")
        except Exception:
            pass

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cart_items (
                cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
                cart_id INT NOT NULL,
                menu_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
                FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
            )
            """
        )

        try:
            cursor.execute("ALTER TABLE cart_items ADD UNIQUE (cart_id, menu_id)")
        except Exception:
            pass

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pending',
                total_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                menu_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                price_at_order DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
            )
            """
        )

        conn.commit()
        conn.close()
        return True
    except Exception as exc:
        print(f"Error occurred while setting up the database: {exc}")
        return False