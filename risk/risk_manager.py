class RiskManager:
    def __init__(self, capital, max_risk_per_trade, max_daily_loss):
        if capital <= 0:
            raise ValueError("Capital must be greater than zero")

        if max_risk_per_trade <= 0:
            raise ValueError("Max risk per trade must be greater than zero")

        if max_daily_loss <= 0:
            raise ValueError("Max daily loss must be greater than zero")

        self.capital = capital
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.daily_loss = 0.0

    def calculate_risk_amount(self):
        return self.capital * self.max_risk_per_trade

    def calculate_position_size(self, entry_price, stop_loss):
        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero")

        if stop_loss <= 0:
            raise ValueError("Stop loss must be greater than zero")

        if stop_loss >= entry_price:
            raise ValueError("Stop loss must be below entry price")

        risk_amount = self.calculate_risk_amount()
        risk_per_unit = entry_price - stop_loss

        return risk_amount / risk_per_unit

    def calculate_position_value(self, entry_price, position_size):
        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero")

        if position_size <= 0:
            raise ValueError("Position size must be greater than zero")

        return entry_price * position_size

    def is_position_affordable(self, entry_price, position_size):
        position_value = self.calculate_position_value(entry_price, position_size)

        return position_value <= self.capital

    def is_stop_loss_hit(self, current_price, stop_loss):
        if current_price <= 0:
            raise ValueError("Current price must be greater than zero")

        if stop_loss <= 0:
            raise ValueError("Stop loss must be greater than zero")

        return current_price <= stop_loss

    def add_daily_loss(self, loss_amount):
        if loss_amount < 0:
            raise ValueError("Loss amount cannot be negative")

        self.daily_loss += loss_amount

    def get_daily_loss(self):
        return self.daily_loss

    def get_daily_loss_limit(self):
        return self.capital * self.max_daily_loss

    def is_daily_loss_limit_reached(self):
        return self.daily_loss >= self.get_daily_loss_limit()
