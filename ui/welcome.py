import auth.customerLogin as custLogin
import auth.restaurentLogin as restLogin
import auth.registerCustomer as regCustomer
import auth.restaurentRegister as regRestaurent


def welcome():
    while True:
        try:
            print()
            print("=" * 49)
            print("Welcome")
            print("=" * 49)
            print()
            print("1. Customer Login")
            print("2. Restaurant Login")
            print("3. Create Customer Account")
            print("4. Create Restaurant Account")
            print("5. Exit The App")
            choice = int(input("Enter your choice: "))
            match choice:
                case 1:
                    custLogin.customerLogin()
                case 2:
                    restLogin.restaurentLogin()
                case 3:
                    regCustomer.registerCustomer()
                case 4:
                    regRestaurent.registerRestaurent()
                case 5:
                    print()
                    print("=" * 49)
                    print("Thank You")
                    print("=" * 49)
                    print()
                    break
                case _:
                    print()
                    print("=" * 49)
                    print("Enter The Correct choice")
                    print("=" * 49)
        except ValueError:
            print()
            print("=" * 49)
            print("Enter a Valid Input")
            print("=" * 49)
