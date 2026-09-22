import ui.welcome as prevMenu
import database.connection as conn
def registerCustomer():
    role="customer"
    hasRegistered=False
    connection=conn.createConnection()
    curser=connection.cursor()
    print("="*49)
    print("Welcome to Customer Registeration")
    print("="*49)

    while hasRegistered is False:
        print()

        
        print("Enter 0 in the ID and Password feilds to Exit the the previous menu")


        id=input("Enter your ID: ")
        password=input("Enter your password: ")

        if(id=="0" and password=="0"):
            print()
            return
        
        curser.execute("SELECT id FROM users WHERE id = ?",(id,))
        existing_user=curser.fetchone()
        if(existing_user):
               print()
               print("="*49)
               print("User Already Exist with the ID choose another")
               print("="*49)
               continue
        
        re_password=input("ReEnter your password: ")

        if(password==re_password):
             curser.execute("INSERT INTO users (id,password,role) VALUES(?,?,?)",(id,password,role))
             connection.commit()
             print()
             print("="*49)
             print("User Registeration Sucessfull")
             print("="*49)
             hasRegistered=True
        else:
            print("passwords do not match")
             
               


        
    

    

            

