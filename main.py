import database.setup as setup
import ui.welcome as welcome


def main():
    setup.setupDatabase()
    welcome.welcome()


if __name__ == "__main__":
    main()
