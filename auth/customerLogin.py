import ui.welcome as prevMenu
def customerLogin():
    hasCustLoggedin=False

    while hasCustLoggedin is False:
        print()
        print("="*49)
        print("Welcome Customer")
        print("="*49)
        print()
        print("Enter 0 in the ID and Password feilds to Exit the the previous menu")
        id=input("Enter your ID: ")
        password=input("Enter your password: ")
        if(id=="0" and password=="0"):
            print()
            return
    

            

