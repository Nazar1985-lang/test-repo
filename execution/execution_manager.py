class ExecutionManager:
    def __init__(self, mode="PAPER"):
        self.mode = mode

    def execute(self, symbol, signal, quantity, price):
        if self.mode != "PAPER":
            raise RuntimeError("Live trading is disabled")

        if signal == "HOLD":
            print(f"{symbol}: HOLD")
            return

        print(f"[PAPER] {signal} {quantity} {symbol} at ${price:.2f}")
