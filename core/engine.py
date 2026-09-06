from config.settings import (
    ENGINE_NAME,
    MODE,
    STARTING_CAPITAL,
    MAX_RISK_PER_TRADE,
    MAX_DAILY_LOSS,
)

from risk.risk_manager import RiskManager
from portfolio.portfolio_manager import PortfolioManager
from strategies.signal_strategy import SignalStrategy
from execution.execution_manager import ExecutionManager


class TradingEngine:
    def __init__(self):
        self.name = ENGINE_NAME
        self.mode = MODE
        self.capital = STARTING_CAPITAL
        self.max_risk_per_trade = MAX_RISK_PER_TRADE
        self.max_daily_loss = MAX_DAILY_LOSS
        self.status = "STOPPED"

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

    def stop(self):
        self.status = "STOPPED"
        print(f"{self.name}: {self.status}")

    def can_trade(self):
        if self.status != "RUNNING":
            return False

        if self.risk_manager.is_daily_loss_limit_reached():
            return False

        return True
