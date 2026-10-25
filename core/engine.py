import time
import signal
from config.settings import (
    ENGINE_NAME,
    MODE,
    STARTING_CAPITAL,
    MAX_RISK_PER_TRADE,
    MAX_DAILY_LOSS,
    TICK_INTERVAL_SECONDS,
)

from risk.risk_manager import RiskManager
from portfolio.portfolio_manager import PortfolioManager
from strategies.signal_strategy import SignalStrategy
from execution.execution_manager import ExecutionManager
from core.backoff import ExponentialBackoff


class TradingEngine:
    def __init__(self):
        self.name = ENGINE_NAME
        self.mode = MODE
        self.capital = STARTING_CAPITAL
        self.max_risk_per_trade = MAX_RISK_PER_TRADE
        self.max_daily_loss = MAX_DAILY_LOSS
        self.tick_interval = TICK_INTERVAL_SECONDS

        self.tick_count = 0
        self.status = "STOPPED"
        self.last_tick_time = None
        self.backoff = ExponentialBackoff(
            base_delay=1.0,
            max_delay=30.0,
        )

        signal.signal(signal.SIGTERM, self._handle_shutdown)

        self.risk_manager = RiskManager(
            self.capital,
            self.max_risk_per_trade,
            self.max_daily_loss,
        )

        self.portfolio = PortfolioManager(self.capital)
        self.strategy = SignalStrategy()
        self.execution = ExecutionManager(self.mode)

    def start(self):
        self.status = "RUNNING"
        print(f"{self.name}: {self.status}")
        print(f"Mode: {self.mode}")
        print(f"Starting capital: ${self.capital:.2f}")
        print(f"Max risk per trade: {self.max_risk_per_trade:.0%}")
        print(f"Max daily loss: {self.max_daily_loss:.0%}")
        print(f"Portfolio cash: ${self.portfolio.cash:.2f}")

    def check_watchdog(self, timeout_seconds=None):
        if self.last_tick_time is None:
            return False

        if timeout_seconds is None:
            timeout_seconds = self.tick_interval * 2

        elapsed = time.monotonic() - self.last_tick_time
        return elapsed > timeout_seconds

    def run_single_tick(self):
        if self.status != "RUNNING":
            return

        self.tick_count += 1
        self.last_tick_time = time.monotonic()

        print(f"Tick: {self.tick_count}")
        print(f"Heartbeat: tick={self.tick_count}")

    def run(self, max_ticks=None):
        if self.status != "RUNNING":
            return

        next_tick = time.monotonic()

        while self.status == "RUNNING":
            self.tick_count += 1
            self.last_tick_time = time.monotonic()

            print(f"Tick: {self.tick_count}")
            print(f"Heartbeat: tick={self.tick_count}")

            if max_ticks is not None and self.tick_count >= max_ticks:
                break

            next_tick += self.tick_interval
            sleep_time = next_tick - time.monotonic()

            if sleep_time > 0:
                time.sleep(sleep_time)

    def _handle_shutdown(self, signum, frame):
        self.stop()

    def stop(self):
        self.status = "STOPPED"
        print(f"{self.name}: {self.status}")

    def can_trade(self):
        if self.status != "RUNNING":
            return False

        if self.risk_manager.is_daily_loss_limit_reached():
            return False

        return True
