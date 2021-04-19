from maintenance_cart import MaintenanceCart

class MaintenanceYard:
    def __init__(self, id, name, exits, line_exits, maintenance_cart_number):
        self.id = id
        self.name = name
        self.stack = []
        self.secondary_stack = []
        self.exits = exits
        self.busy_exits = 0
        self.line_exits = line_exits
        self.maintenance_cart_number = maintenance_cart_number

    def generate_maintenance_carts(self):
        for i in range(self.maintenance_cart_number):
            cart = MaintenanceCart(i, True)
            self.secondary_stack.append(cart)

        cart = MaintenanceCart(self.maintenance_cart_number, False)
        self.secondary_stack.append(cart)