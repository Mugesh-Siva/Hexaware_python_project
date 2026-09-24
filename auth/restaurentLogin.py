import database.connection as conn
import ui.restaurent.restaurentHome as restHome


def restaurentLogin():
    connection = conn.createConnection()
    cursor = connection.cursor()
    role = "restaurant"
    print("=" * 49)
    print("Welcome to Restaurant Login")
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

        cursor.execute(
            "SELECT id, password FROM users WHERE id = %s AND password = %s AND role = %s",
            (user_id, password, role),
        )
        user = cursor.fetchone()

        if user:
            print()
            print("=" * 49)
            print("Login Successful")
            print("=" * 49)
            connection.close()
            restuarentUser=restHome.restaurentHome(user_id,role)
            restuarentUser.restUI()
        
            

            return

        print()
        print("=" * 49)
        print("Invalid ID or Password")
        print("=" * 49)

