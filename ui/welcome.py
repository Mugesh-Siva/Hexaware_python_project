import auth.customerLogin as custLogin
import auth.restaurentLogin as restLogin
def welcome():
    while True:
        try:
            print()
            print("="*49)
            print("Welcome")
            print("="*49)
            print()
            print("1. Customer Login")
            print("2. Restaurent Login")
            print("3. Create Customer Account")
            print("4. Create Restaurent Account")
            print("5. Exit The App")
            choice=int(input("Enter your choice: "))
            match choice:
                case 1:
                    custLogin.customerLogin()
                    
                case 2:
                    restLogin.restaurentLogin()
                case 3:
                    pass
                case 4: 
                    pass
                case 5:
                    print()
                    print("="*49)
                    print("Thank You")
                    print("="*49)
                    print()
                    break
                case _:
                    print()
                    print("="*49)
                    print("Enter The Corrrect choice")
                    print("="*49)
        except:
            print()
            print("="*49)
            print("Enter a Valid Input")
            print("="*49)
                


        