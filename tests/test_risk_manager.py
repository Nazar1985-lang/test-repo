import pytest

from risk.risk_manager import RiskManager


def create_risk_manager():
    return RiskManager(
        capital=10000,
        max_risk_per_trade=0.01,
        max_daily_loss=0.03,
    )


def test_risk_amount():
    risk_manager = create_risk_manager()

    assert risk_manager.calculate_risk_amount() == 100


def test_invalid_capital():
    with pytest.raises(
        ValueError,
        match="Capital must be greater than zero",
    ):
        RiskManager(
            capital=0,
            max_risk_per_trade=0.01,
            max_daily_loss=0.03,
        )


def test_invalid_max_risk_per_trade():
    with pytest.raises(
        ValueError,
        match="Max risk per trade must be greater than zero",
    ):
        RiskManager(
            capital=10000,
            max_risk_per_trade=0,
            max_daily_loss=0.03,
        )


def test_invalid_max_daily_loss():
    with pytest.raises(
        ValueError,
        match="Max daily loss must be greater than zero",
    ):
        RiskManager(
            capital=10000,
            max_risk_per_trade=0.01,
            max_daily_loss=0,
        )


def test_position_size():
    risk_manager = create_risk_manager()

    position_size = risk_manager.calculate_position_size(
        entry_price=105,
        stop_loss=100,
    )

    assert position_size == 20


@pytest.mark.parametrize(
    ("entry_price", "stop_loss", "message"),
    [
        (0, 100, "Entry price must be greater than zero"),
        (105, 0, "Stop loss must be greater than zero"),
        (105, 105, "Stop loss must be below entry price"),
        (105, 110, "Stop loss must be below entry price"),
    ],
)
def test_position_size_validation(entry_price, stop_loss, message):
    risk_manager = create_risk_manager()

    with pytest.raises(ValueError, match=message):
        risk_manager.calculate_position_size(
            entry_price=entry_price,
            stop_loss=stop_loss,
        )


def test_position_value():
    risk_manager = create_risk_manager()

    assert (
        risk_manager.calculate_position_value(
            entry_price=100,
            position_size=2,
        )
        == 200
    )


@pytest.mark.parametrize(
    ("entry_price", "position_size", "message"),
    [
        (0, 1, "Entry price must be greater than zero"),
        (100, 0, "Position size must be greater than zero"),
    ],
)
def test_position_value_validation(entry_price, position_size, message):
    risk_manager = create_risk_manager()

    with pytest.raises(ValueError, match=message):
        risk_manager.calculate_position_value(
            entry_price=entry_price,
            position_size=position_size,
        )


def test_position_affordability():
    risk_manager = create_risk_manager()

    assert (
        risk_manager.is_position_affordable(
            entry_price=100,
            position_size=50,
        )
        is True
    )

    assert (
        risk_manager.is_position_affordable(
            entry_price=100,
            position_size=101,
        )
        is False
    )


def test_stop_loss_hit():
    risk_manager = create_risk_manager()

    assert (
        risk_manager.is_stop_loss_hit(
            current_price=100,
            stop_loss=100,
        )
        is True
    )

    assert (
        risk_manager.is_stop_loss_hit(
            current_price=101,
            stop_loss=100,
        )
        is False
    )


@pytest.mark.parametrize(
    ("current_price", "stop_loss", "message"),
    [
        (0, 100, "Current price must be greater than zero"),
        (100, 0, "Stop loss must be greater than zero"),
    ],
)
def test_stop_loss_validation(current_price, stop_loss, message):
    risk_manager = create_risk_manager()

    with pytest.raises(ValueError, match=message):
        risk_manager.is_stop_loss_hit(
            current_price=current_price,
            stop_loss=stop_loss,
        )


def test_daily_loss():
    risk_manager = create_risk_manager()

    assert risk_manager.get_daily_loss() == 0

    risk_manager.add_daily_loss(100)

    assert risk_manager.get_daily_loss() == 100


def test_negative_daily_loss():
    risk_manager = create_risk_manager()

    with pytest.raises(ValueError, match="Loss amount cannot be negative"):
        risk_manager.add_daily_loss(-1)


def test_daily_loss_limit():
    risk_manager = create_risk_manager()

    assert risk_manager.get_daily_loss_limit() == 300

    risk_manager.add_daily_loss(300)

    assert risk_manager.is_daily_loss_limit_reached() is True


def test_daily_loss_limit_not_reached():
    risk_manager = create_risk_manager()

    risk_manager.add_daily_loss(299)

    assert risk_manager.is_daily_loss_limit_reached() is False
