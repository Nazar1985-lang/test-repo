import pytest

from execution.execution_manager import ExecutionManager


def test_paper_buy():
    execution = ExecutionManager(mode="PAPER")

    execution.execute(
        symbol="BTCUSDT",
        signal="BUY",
        quantity=1,
        price=100,
    )


def test_paper_sell():
    execution = ExecutionManager(mode="PAPER")

    execution.execute(
        symbol="BTCUSDT",
        signal="SELL",
        quantity=1,
        price=100,
    )


def test_paper_hold():
    execution = ExecutionManager(mode="PAPER")

    execution.execute(
        symbol="BTCUSDT",
        signal="HOLD",
        quantity=0,
        price=100,
    )


def test_live_trading_blocked():
    execution = ExecutionManager(mode="LIVE")

    with pytest.raises(RuntimeError):
        execution.execute(
            symbol="BTCUSDT",
            signal="BUY",
            quantity=1,
            price=100,
        )
