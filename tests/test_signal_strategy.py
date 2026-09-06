from strategies.signal_strategy import SignalStrategy


def test_buy_signal():
    strategy = SignalStrategy()

    signal = strategy.generate_signal(
        price=105,
        moving_average=100,
    )

    assert signal == "BUY"


def test_sell_signal():
    strategy = SignalStrategy()

    signal = strategy.generate_signal(
        price=95,
        moving_average=100,
    )

    assert signal == "SELL"


def test_hold_signal():
    strategy = SignalStrategy()

    signal = strategy.generate_signal(
        price=100,
        moving_average=100,
    )

    assert signal == "HOLD"
