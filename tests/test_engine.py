from core.engine import TradingEngine


def test_engine_starts():
    engine = TradingEngine()

    assert engine.status == "STOPPED"

    engine.start()

    assert engine.status == "RUNNING"


def test_engine_allows_trade():
    engine = TradingEngine()

    engine.start()

    assert engine.can_trade() is True


def test_engine_blocks_trade_after_daily_loss_limit():
    engine = TradingEngine()

    engine.start()

    engine.risk_manager.add_daily_loss(300)

    assert engine.can_trade() is False


def test_engine_stops():
    engine = TradingEngine()

    engine.start()
    engine.stop()

    assert engine.status == "STOPPED"
    assert engine.can_trade() is False
