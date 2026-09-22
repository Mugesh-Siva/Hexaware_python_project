import ui.welcome as prevMenu


def restaurentLogin():
    print("="*49)
    print("Welcome Restaurent")
    print("="*49)

    hasRestLoggedin=False

    while hasRestLoggedin is False:
        print("Enter 0 in the ID and Password feilds to Exit the the previous menu")
        id=input("Enter your ID: ")
        password=input("Enter your password: ")
        if(id=="0" and password=="0"):
            print()
            return