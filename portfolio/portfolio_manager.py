class PortfolioManager:
    def __init__(self, starting_capital):
        if starting_capital <= 0:
            raise ValueError("Starting capital must be greater than zero")

        self.starting_capital = starting_capital
        self.cash = starting_capital
        self.positions = {}

    def get_total_value(self, prices=None):
        total_value = self.cash

        if prices:
            for symbol, quantity in self.positions.items():
                price = prices.get(symbol)

                if price is not None:
                    if price <= 0:
                        raise ValueError("Price must be greater than zero")

                    total_value += quantity * price

        return total_value

    def get_position(self, symbol):
        return self.positions.get(symbol, 0)

    def add_position(self, symbol, quantity, price):
        if not symbol:
            raise ValueError("Symbol is required")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if price <= 0:
            raise ValueError("Price must be greater than zero")

        position_value = quantity * price

        if position_value > self.cash:
            raise ValueError("Not enough cash to open position")

        self.cash -= position_value

        current_quantity = self.get_position(symbol)

        self.positions[symbol] = current_quantity + quantity

    def remove_position(self, symbol, quantity, price):
        if not symbol:
            raise ValueError("Symbol is required")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if price <= 0:
            raise ValueError("Price must be greater than zero")

        current_quantity = self.get_position(symbol)

        if quantity > current_quantity:
            raise ValueError("Not enough position to remove")

        position_value = quantity * price

        self.cash += position_value

        self.positions[symbol] = current_quantity - quantity

    def get_cash(self):
        return self.cash

    def get_position_value(self, symbol, price):
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        quantity = self.get_position(symbol)

        return quantity * price
