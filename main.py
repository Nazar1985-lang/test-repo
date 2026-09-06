from core.engine import TradingEngine


def main():
    engine = TradingEngine()

    engine.start()

    # Імітуємо досягнення денного ліміту збитку
    engine.risk_manager.add_daily_loss(300)

    entry_price = 105

    moving_average = 100

    signal = engine.strategy.generate_signal(
        entry_price,
        moving_average,
    )

    print(f"Daily loss: ${engine.risk_manager.get_daily_loss():.2f}")
    print(f"Daily loss limit: ${engine.risk_manager.get_daily_loss_limit():.2f}")
    print(f"Signal: {signal}")

    if signal != "HOLD":
        if not engine.can_trade():
            print("TRADE BLOCKED BY ENGINE")
        else:
            print("ERROR: TRADE WAS NOT BLOCKED")


if __name__ == "__main__":
    main()
