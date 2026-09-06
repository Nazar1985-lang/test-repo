class SignalStrategy:
    def __init__(self):
        self.name = "Basic Signal Strategy"

    def generate_signal(self, price, moving_average):
        if price > moving_average:
            return "BUY"

        if price < moving_average:
            return "SELL"

        return "HOLD"
