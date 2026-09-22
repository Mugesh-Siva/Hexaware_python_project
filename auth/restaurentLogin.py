import ui.welcome as prevMenu
import database.connection as conn
def restaurentLogin():
    hasRestLoggedin=False
    connection=conn.createConnection()
    curser=connection.cursor()
    role="customer"
    print("="*49)
    print("Welcome to Restaurent Login")
    print("="*49)

    while hasRestLoggedin is False:
        

        print()
        print("Enter 0 in the ID and Password feilds to Exit the the previous menu")
        id=input("Enter your ID: ")
        password=input("Enter your password: ")
        if(id=="0" and password=="0"):
            print()
            return
        curser.execute("SELECT id, password FROM users WHERE id=? AND password =? AND role=?",(id,password,role))
        user=curser.fetchone()
        if user:
            print()
            print("="*49)
            print("Login Sucessfull")
            print("="*49)
            hasRestLoggedin=True
        else:
            print()
            print("="*49)
            print("Invalid ID or Password")
            print("="*49)
            
    

    

            

