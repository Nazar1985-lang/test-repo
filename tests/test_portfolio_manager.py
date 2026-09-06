from portfolio.portfolio_manager import PortfolioManager


def test_initial_cash():
    portfolio = PortfolioManager(10000)

    assert portfolio.get_cash() == 10000


def test_add_position():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    assert portfolio.get_cash() == 7900
    assert portfolio.get_position("BTCUSDT") == 20


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


def test_total_value():
    portfolio = PortfolioManager(10000)

    portfolio.add_position(
        symbol="BTCUSDT",
        quantity=20,
        price=105,
    )

    total_value = portfolio.get_total_value(prices={"BTCUSDT": 110})

    assert total_value == 10100
