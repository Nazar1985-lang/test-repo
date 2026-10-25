import signal

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


def test_engine_runs_single_tick():
    engine = TradingEngine()
    engine.start()

    engine.run_single_tick()

    assert engine.tick_count == 1


def test_engine_records_last_tick_time():
    engine = TradingEngine()
    engine.start()

    assert engine.last_tick_time is None

    engine.run_single_tick()

    assert engine.last_tick_time is not None
    assert isinstance(engine.last_tick_time, float)


def test_watchdog_returns_false_before_first_tick():
    engine = TradingEngine()
    engine.start()

    assert engine.check_watchdog() is False


def test_watchdog_detects_delayed_tick(monkeypatch):
    engine = TradingEngine()
    engine.start()
    engine.run_single_tick()

    first_tick_time = engine.last_tick_time

    monkeypatch.setattr(
        "core.engine.time.monotonic",
        lambda: first_tick_time + 3,
    )

    assert engine.check_watchdog(timeout_seconds=2) is True


def test_engine_handles_sigterm():
    engine = TradingEngine()

    engine.start()
    engine._handle_shutdown(None, None)

    assert engine.status == "STOPPED"


def test_sigterm_handler_is_registered():
    engine = TradingEngine()

    handler = signal.getsignal(signal.SIGTERM)

    assert handler == engine._handle_shutdown


def test_engine_run_stops_when_status_changes():
    engine = TradingEngine()
    engine.start()

    engine.stop()
    engine.run()

    assert engine.status == "STOPPED"
    assert engine.tick_count == 0


def test_engine_stops_during_run(monkeypatch):
    engine = TradingEngine()
    engine.start()

    def stop_during_sleep(_seconds):
        engine.stop()

    monkeypatch.setattr("core.engine.time.sleep", stop_during_sleep)

    engine.run()

    assert engine.status == "STOPPED"
    assert engine.tick_count == 1


def test_engine_initializes_backoff():
    from core.backoff import ExponentialBackoff

    engine = TradingEngine()

    assert isinstance(engine.backoff, ExponentialBackoff)
    assert engine.backoff.base_delay == 1.0
    assert engine.backoff.max_delay == 30.0
    assert engine.backoff.attempt == 0


def test_engine_backoff_progresses_and_resets():
    engine = TradingEngine()

    assert engine.backoff.next_delay() == 1.0
    assert engine.backoff.next_delay() == 2.0
    assert engine.backoff.next_delay() == 4.0

    engine.backoff.reset()

    assert engine.backoff.next_delay() == 1.0


def test_engine_run_records_last_tick_time(monkeypatch):
    engine = TradingEngine()
    engine.start()

    first_tick_time = 100.0

    monkeypatch.setattr(
        "core.engine.time.monotonic",
        lambda: first_tick_time,
    )

    engine.run(max_ticks=1)

    assert engine.tick_count == 1
    assert engine.last_tick_time == first_tick_time


def test_watchdog_does_not_trigger_at_timeout_boundary(monkeypatch):
    engine = TradingEngine()
    engine.start()
    engine.run_single_tick()

    first_tick_time = engine.last_tick_time

    monkeypatch.setattr(
        "core.engine.time.monotonic",
        lambda: first_tick_time + 2,
    )

    assert engine.check_watchdog(timeout_seconds=2) is False
