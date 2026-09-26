from services.restaurantServices.orderService import get_orders_for_restaurant


class orderListUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def listOrders(self):
        print()
        print("=" * 49)
        print("ORDER LIST")
        print("=" * 49)

        result = get_orders_for_restaurant(self.id)
        if not result["success"]:
            print(result["message"])
            return

        orders = result["orders"]
        if not orders:
            print("No orders have been placed for this restaurant yet.")
            print("=" * 49)
            return

        for order in orders:
            print(f"Order ID        : {order['order_id']}")
            print(f"Customer Name   : {order['customer_name']}")
            print(f"Customer ID     : {order['customer_id']}")
            print(f"Delivery Address: {order.get('customer_address', 'Address not set')}")
            print(f"Status          : {order['status']}")
            print(f"Ordered At      : {order['created_at']}")
            print("Items:")

            for item in order["items"]:
                print(
                    f"  - {item['title']} x{item['quantity']} "
                    f"@ ₹{item['price_at_order']:.2f} each"
                )

            print(f"Total Amount   : ₹{order['total_price']:.2f}")
            print("-" * 49)

        print("=" * 49)
