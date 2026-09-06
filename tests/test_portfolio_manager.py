import pytest

from portfolio.portfolio_manager import PortfolioManager


def test_initial_cash():
    portfolio = PortfolioManager(10000)

    assert portfolio.get_cash() == 10000


def test_invalid_starting_capital():
    with pytest.raises(ValueError, match="Starting capital must be greater than zero"):
        PortfolioManager(0)


def test_get_position_for_missing_symbol():
    portfolio = PortfolioManager(10000)

    assert portfolio.get_position("BTCUSDT") == 0


def test_get_total_value_without_prices():
    portfolio = PortfolioManager(10000)

    assert portfolio.get_total_value() == 10000


def test_add_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    assert portfolio.get_cash() == 7900
    assert portfolio.get_position("BTCUSDT") == 20


def test_add_position_to_existing_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=10,
        price=100,
    )

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=5,
        price=100,
    )

    assert portfolio.get_position("BTCUSDT") == 15
    assert portfolio.get_cash() == 8500


@pytest.mark.parametrize(
    ("symbol", "quantity", "price", "message"),
    [
        ("", 1, 100, "Symbol is required"),
        ("BTCUSDT", 0, 100, "Quantity must be greater than zero"),
        ("BTCUSDT", 1, 0, "Price must be greater than zero"),
    ],
)
def test_add_position_validation(symbol, quantity, price, message):
    portfolio = PortfolioManager(10000)

    with pytest.raises(ValueError, match=message):
        portfolio.add_position(symbol, quantity, price)


def test_add_position_when_not_enough_cash():
    portfolio = PortfolioManager(10000)

    with pytest.raises(ValueError, match="Not enough cash to open position"):
        portfolio.add_position(
            symbol="BTCUSDT",
            quantity=101,
            price=100,
        )


def test_remove_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    portfolio.remove_position(
        symbol="BTCUSDT",
        quantity=20,
        price=110,
    )

    assert portfolio.get_cash() == 10100
    assert portfolio.get_position("BTCUSDT") == 0


@pytest.mark.parametrize(
    ("symbol", "quantity", "price", "message"),
    [
        ("", 1, 100, "Symbol is required"),
        ("BTCUSDT", 0, 100, "Quantity must be greater than zero"),
        ("BTCUSDT", 1, 0, "Price must be greater than zero"),
    ],
)
def test_remove_position_validation(symbol, quantity, price, message):
    portfolio = PortfolioManager(10000)

    with pytest.raises(ValueError, match=message):
        portfolio.remove_position(symbol, quantity, price)


def test_remove_position_when_not_enough_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=10,
        price=100,
    )

    with pytest.raises(ValueError, match="Not enough position to remove"):
        portfolio.remove_position(
            symbol="BTCUSDT",
            quantity=11,
            price=100,
        )


def test_remove_partial_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=100,
    )

    portfolio.remove_position(
        symbol="BTCUSDT",
        quantity=5,
        price=110,
    )

    assert portfolio.get_position("BTCUSDT") == 15
    assert portfolio.get_cash() == 8550


def test_total_value():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    total_value = portfolio.get_total_value(prices={"BTCUSDT": 110})

    assert total_value == 10100


def test_total_value_ignores_missing_price():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    total_value = portfolio.get_total_value(prices={"ETHUSDT": 200})

    assert total_value == 7900


def test_total_value_rejects_invalid_price():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    with pytest.raises(ValueError, match="Price must be greater than zero"):
        portfolio.get_total_value(prices={"BTCUSDT": 0})


def test_position_value():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=100,
    )

    assert (
        portfolio.get_position_value(
            symbol="BTCUSDT",
            price=110,
        )
        == 2200
    )


def test_position_value_rejects_invalid_price():
    portfolio = PortfolioManager(10000)

    with pytest.raises(ValueError, match="Price must be greater than zero"):
        portfolio.get_position_value(
            symbol="BTCUSDT",
            price=0,
        )
