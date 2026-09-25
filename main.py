import database.setup as setup
import ui.welcome as welcome


def main():
    try:
        if not setup.setupDatabase():
            print()
            print("=" * 49)
            print("Database setup failed. Please ensure MySQL is running and try again.")
            print("=" * 49)
            return
        welcome.welcome()
    except Exception as exc:
        print()
        print("=" * 49)
        print(f"Application startup failed: {exc}")
        print("=" * 49)


if __name__ == "__main__":
    main()
