import database.connection as conn
import database.setup as setup


def registerRestaurent():
    setup.setupDatabase()
    role = "restaurant"
    connection = conn.createConnection()
    cursor = connection.cursor()
    print("=" * 49)
    print("Welcome to Restaurant Registration")
    print("=" * 49)

    while True:
        print()
        print("Enter 0 in the ID and Password fields to exit to the previous menu")
        user_id = input("Enter your ID: ").strip()
        password = input("Enter your password: ").strip()

        if user_id == "0" and password == "0":
            print()
            connection.close()
            return

        if not user_id or not password:
            print()
            print("=" * 49)
            print("ID and password cannot be empty")
            print("=" * 49)
            continue

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            print()
            print("=" * 49)
            print("User already exists with this ID. Please choose another one.")
            print("=" * 49)
            continue

        re_password = input("Re-enter your password: ").strip()

        if password == re_password:
            cursor.execute(
                "INSERT INTO users (id, password, role) VALUES (%s, %s, %s)",
                (user_id, password, role),
            )
            connection.commit()
            print()
            print("=" * 49)
            print("User Registration Successful")
            print("=" * 49)
            connection.close()
            return

        print()
        print("=" * 49)
        print("Passwords do not match")
        print("=" * 49)

