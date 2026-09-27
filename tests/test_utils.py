import database.connection as connection

def cleanup_test_user(user_id):
    if not user_id:
        return
    try:
        conn = connection.createConnection()
        cursor = conn.cursor()
        
        # 1. Delete order_items that belong to the user's orders
        cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE user_id = %s)", (user_id,))
        
        # 2. Delete the user's orders
        cursor.execute("DELETE FROM orders WHERE user_id = %s", (user_id,))
        
        # 3. Delete cart_items that belong to the user's cart
        cursor.execute("DELETE FROM cart_items WHERE cart_id IN (SELECT cart_id FROM carts WHERE user_id = %s)", (user_id,))
        
        # 4. Delete the user's carts
        cursor.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))
        
        # 5. For restaurants, delete cart_items and order_items that reference their menus
        cursor.execute("DELETE FROM cart_items WHERE menu_id IN (SELECT menu_id FROM menus WHERE user_id = %s)", (user_id,))
        cursor.execute("DELETE FROM order_items WHERE menu_id IN (SELECT menu_id FROM menus WHERE user_id = %s)", (user_id,))
        
        # 6. Delete the restaurant's menus
        cursor.execute("DELETE FROM menus WHERE user_id = %s", (user_id,))
        
        # 7. Delete the user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error during teardown for user {user_id}: {e}")
