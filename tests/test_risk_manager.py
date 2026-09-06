from risk.risk_manager import RiskManager


def test_risk_amount():
    risk_manager = RiskManager(
        capital=10000,
        max_risk_per_trade=0.01,
        max_daily_loss=0.03,
    )

    assert risk_manager.calculate_risk_amount() == 100


def test_position_size():
    risk_manager = RiskManager(
        capital=10000,
        max_risk_per_trade=0.01,
        max_daily_loss=0.03,
    )

    position_size = risk_manager.calculate_position_size(
        entry_price=105,
        stop_loss=100,
    )

    assert position_size == 20


def test_daily_loss_limit():
    risk_manager = RiskManager(
        capital=10000,
        max_risk_per_trade=0.01,
        max_daily_loss=0.03,
    )

    risk_manager.add_daily_loss(300)

    assert risk_manager.is_daily_loss_limit_reached() is True
