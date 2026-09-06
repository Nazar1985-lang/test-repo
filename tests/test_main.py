import runpy
from unittest.mock import Mock

import main as main_module


def create_fake_engine(signal, can_trade):
    engine = Mock()

    engine.risk_manager.get_daily_loss.return_value = 300
    engine.risk_manager.get_daily_loss_limit.return_value = 300
    engine.strategy.generate_signal.return_value = signal
    engine.can_trade.return_value = can_trade

    return engine


def test_main_blocks_trade(monkeypatch, capsys):
    fake_engine = create_fake_engine("BUY", False)

    monkeypatch.setattr(
        main_module,
        "TradingEngine",
        lambda: fake_engine,
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "TRADE BLOCKED BY ENGINE" in output


def test_main_allows_trade(monkeypatch, capsys):
    fake_engine = create_fake_engine("BUY", True)

    monkeypatch.setattr(
        main_module,
        "TradingEngine",
        lambda: fake_engine,
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "ERROR: TRADE WAS NOT BLOCKED" in output


def test_main_hold(monkeypatch, capsys):
    fake_engine = create_fake_engine("HOLD", True)

    monkeypatch.setattr(
        main_module,
        "TradingEngine",
        lambda: fake_engine,
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "Signal: HOLD" in output
    assert "TRADE BLOCKED BY ENGINE" not in output
    assert "ERROR: TRADE WAS NOT BLOCKED" not in output


def test_main_script_entrypoint(capsys):
    runpy.run_path(
        "main.py",
        run_name="__main__",
    )

    output = capsys.readouterr().out

    assert "TRADE BLOCKED BY ENGINE" in output
