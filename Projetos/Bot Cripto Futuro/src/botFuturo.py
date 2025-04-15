import os
import sys
import time
from datetime import datetime
import logging
import pandas as pd
from binance.client import Client
from binance.enums import *
import requests

# Configuração de logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'logs', 'trading_bot.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Chaves de API
api_key = "hlwZvNGCgajED6ZzRinKB5yUgQcUvyEkzpmLeRw2Y5J9NWNZ6D7PV6PbBXwlSawH"
secret_key = "tLKAMdXGyiXSuKrEQzLyD28TmQmwrPwVBo6MjvXo6I86w0aTwLi45eku39jlSj1i"

# CONFIGURAÇÕES
STOCK_CODE = "XRP"
OPERATION_CODE = "XRPUSDT"  # Par para Futuros
CANDLE_PERIOD = Client.KLINE_INTERVAL_15MINUTE
INITIAL_CAPITAL = 1  # Capital inicial em USDT
LEVERAGE = 10  # Alavancagem segura
TRADE_CAPITAL_PERCENTAGE = 100  # Percentual do capital total a ser reinvestido

class BinanceFuturesTraderBot:
    def __init__(self, stock_code, operation_code, initial_capital, leverage, candle_period):
        self.stock_code = stock_code
        self.operation_code = operation_code
        self.capital = initial_capital
        self.leverage = leverage
        self.candle_period = candle_period

        # Inicializa o cliente Binance com Futuros
        self.client_binance = Client(
            api_key, secret_key, requests_params={"timeout": 20}
        )
        self.set_leverage()

        # Variáveis de estado
        self.last_trade_decision = False
        self.actual_trade_position = False
        self.stock_data = pd.DataFrame()

        # Atualiza dados iniciais
        self.update_all_data()
        print('__________________________________________')
        print('Robo Trader para Futuros iniciado...')

    def set_leverage(self):
        """Configura a alavancagem isolada para o par de futuros."""
        try:
            self.client_binance.futures_change_leverage(
                symbol=self.operation_code,
                leverage=self.leverage
            )
            logging.info(f"Alavancagem configurada para {self.leverage}x no par {self.operation_code}.")
        except Exception as e:
            logging.error(f"Erro ao configurar alavancagem: {e}")

    def get_stock_data_close_price_open_time(self):
        """Obtém os preços de fechamento e horários de abertura dos candles."""
        try:
            candles = self.client_binance.futures_klines(
                symbol=self.operation_code, interval=self.candle_period, limit=500
            )
            prices = pd.DataFrame(candles)
            prices.columns = [
                "open_time", "open_price", "high_price", "low_price", "close_price",
                "volume", "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "-"
            ]
            prices = prices[["close_price", "open_time"]]
            prices["close_price"] = prices["close_price"].astype(float)
            prices["open_time"] = pd.to_datetime(prices["open_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
            return prices
        except Exception as e:
            logging.error(f"Erro ao obter dados de candles para {self.operation_code}: {e}")
            return pd.DataFrame()

    def get_moving_average_trade_strategy(self, fast_window=7, slow_window=40):
        """Estratégia de Média Móvel."""
        self.stock_data["ma_fast"] = self.stock_data["close_price"].rolling(window=fast_window).mean()
        self.stock_data["ma_slow"] = self.stock_data["close_price"].rolling(window=slow_window).mean()

        last_ma_fast = self.stock_data["ma_fast"].iloc[-1]
        last_ma_slow = self.stock_data["ma_slow"].iloc[-1]
        ma_trade_decision = last_ma_fast > last_ma_slow

        print('------------------------------------------')
        print(f'Estratégia executada: Moving Average')
        print(f'({self.operation_code})\n | {last_ma_fast:.3f} = Última Média Rápida \n | {last_ma_slow:.3f} = Última Média Lenta')
        print(f'Decisão de posição: {"Comprar" if ma_trade_decision else "Vender"}')
        print('------------------------------------------')

        return ma_trade_decision

    def update_all_data(self):
        """Atualiza todos os dados necessários."""
        self.stock_data = self.get_stock_data_close_price_open_time()

    def calculate_trade_quantity(self):
        """Calcula a quantidade a ser negociada com base no capital disponível."""
        try:
            price = float(self.client_binance.futures_symbol_ticker(symbol=self.operation_code)["price"])
            exchange_info = self.client_binance.futures_exchange_info()
            
            # Obter a precisão do ativo
            precision = None
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == self.operation_code:
                    precision = int(symbol_info['quantityPrecision'])
                    break
            
            if precision is None:
                raise ValueError("Não foi possível obter a precisão para o ativo.")

            # Calcular a quantidade e ajustá-la à precisão permitida
            quantity = (self.capital / price) * self.leverage
            return round(quantity, precision)
        except Exception as e:
            logging.error(f"Erro ao calcular quantidade de negociação: {e}")
            return 0

    def open_position(self, side):
        """Abre uma posição Long ou Short."""
        try:
            position_side = "BUY" if side == "LONG" else "SELL"
            quantity = self.calculate_trade_quantity()
            if quantity > 0:
                order = self.client_binance.futures_create_order(
                    symbol=self.operation_code,
                    side=position_side,
                    type="MARKET",
                    quantity=quantity
                )
                logging.info(f"Posição {side} aberta: {order}")
                self.actual_trade_position = True
                return order
        except Exception as e:
            logging.error(f"Erro ao abrir posição {side}: {e}")

    def close_position(self):
        """Fecha a posição atual."""
        try:
            side = "SELL" if self.last_trade_decision else "BUY"
            quantity = self.calculate_trade_quantity()
            if quantity > 0:
                order = self.client_binance.futures_create_order(
                    symbol=self.operation_code,
                    side=side,
                    type="MARKET",
                    quantity=quantity
                )
                logging.info(f"Posição fechada: {order}")
                self.actual_trade_position = False
                return order
        except Exception as e:
            logging.error(f"Erro ao fechar posição: {e}")

    def execute(self):
        """Executa a lógica principal do bot."""
        self.update_all_data()

        print('__________________________________________')
        print(f'Executado ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
        print(f'Posição atual: {"Aberta" if self.actual_trade_position else "Fechada"}')

        ma_trade_decision = self.get_moving_average_trade_strategy()
        self.last_trade_decision = ma_trade_decision

        if not self.actual_trade_position and self.last_trade_decision:
            self.open_position("LONG")
        elif self.actual_trade_position and not self.last_trade_decision:
            self.close_position()

if __name__ == "__main__":
    FuturesTrader = BinanceFuturesTraderBot(STOCK_CODE, OPERATION_CODE, INITIAL_CAPITAL, LEVERAGE, CANDLE_PERIOD)
    while True:
        FuturesTrader.execute()
        time.sleep(60)
import os
import time
from datetime import datetime
import logging
import pandas as pd
from binance.client import Client
from binance.enums import *
import requests

# Configuração de logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Chaves de API (Substitua por chaves reais ou use variáveis de ambiente para maior segurança)
api_key = os.getenv("BINANCE_API_KEY", "sua_api_key")
secret_key = os.getenv("BINANCE_SECRET_KEY", "sua_secret_key")

# Configurações gerais
STOCK_CODE = "XRP"
OPERATION_CODE = "XRPUSDT"
CANDLE_PERIOD = Client.KLINE_INTERVAL_15MINUTE
INITIAL_CAPITAL = 1  # Capital inicial em USDT
LEVERAGE = 10
TRADE_CAPITAL_PERCENTAGE = 100  # Percentual do capital total a ser reinvestido
STOP_LOSS_PERCENTAGE = 1.5  # Stop Loss em percentual
TAKE_PROFIT_PERCENTAGE = 3  # Take Profit em percentual

class BinanceFuturesTraderBot:
    def __init__(self, stock_code, operation_code, initial_capital, leverage, candle_period):
        self.stock_code = stock_code
        self.operation_code = operation_code
        self.capital = initial_capital
        self.leverage = leverage
        self.candle_period = candle_period

        self.client_binance = Client(api_key, secret_key, requests_params={"timeout": 20})
        self.set_leverage()

        # Variáveis de estado
        self.last_trade_decision = None
        self.actual_trade_position = False
        self.stock_data = pd.DataFrame()
        self.precision = None  # Precisão do ativo
        self.update_precision()
        self.update_all_data()

        logging.info("Bot iniciado com sucesso!")

    def set_leverage(self):
        """Configura a alavancagem para o ativo."""
        try:
            self.client_binance.futures_change_leverage(symbol=self.operation_code, leverage=self.leverage)
            logging.info(f"Alavancagem configurada para {self.leverage}x no par {self.operation_code}.")
        except Exception as e:
            logging.error(f"Erro ao configurar alavancagem: {e}")

    def update_precision(self):
        """Obtém a precisão de quantidade permitida para o ativo."""
        try:
            exchange_info = self.client_binance.futures_exchange_info()
            for symbol_info in exchange_info["symbols"]:
                if symbol_info["symbol"] == self.operation_code:
                    self.precision = int(symbol_info["quantityPrecision"])
                    logging.info(f"Precisão de quantidade obtida: {self.precision}")
                    return
        except Exception as e:
            logging.error(f"Erro ao obter precisão do ativo: {e}")

    def update_all_data(self):
        """Atualiza os dados mais recentes do ativo."""
        self.stock_data = self.get_stock_data_close_price_open_time()

    def get_stock_data_close_price_open_time(self):
        """Obtém os dados de candles (preço de fechamento e horários)."""
        try:
            candles = self.client_binance.futures_klines(symbol=self.operation_code, interval=self.candle_period, limit=500)
            prices = pd.DataFrame(candles)
            prices.columns = [
                "open_time", "open_price", "high_price", "low_price", "close_price",
                "volume", "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "-"
            ]
            prices["close_price"] = prices["close_price"].astype(float)
            prices["open_time"] = pd.to_datetime(prices["open_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
            return prices[["close_price", "open_time"]]
        except Exception as e:
            logging.error(f"Erro ao obter dados de candles: {e}")
            return pd.DataFrame()

    def calculate_trade_quantity(self):
        """Calcula a quantidade a ser negociada respeitando a precisão."""
        try:
            price = float(self.client_binance.futures_symbol_ticker(symbol=self.operation_code)["price"])
            quantity = (self.capital * self.leverage) / price
            return round(quantity, self.precision)
        except Exception as e:
            logging.error(f"Erro ao calcular quantidade de negociação: {e}")
            return 0

    def get_rsi(self, period=14):
        """Calcula o Índice de Força Relativa (RSI)."""
        delta = self.stock_data["close_price"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.stock_data["rsi"] = rsi

    def moving_average_strategy(self):
        """Combinação de médias móveis e RSI para tomada de decisão."""
        self.stock_data["ma_fast"] = self.stock_data["close_price"].rolling(window=7).mean()
        self.stock_data["ma_slow"] = self.stock_data["close_price"].rolling(window=40).mean()
        self.get_rsi()

        ma_fast = self.stock_data["ma_fast"].iloc[-1]
        ma_slow = self.stock_data["ma_slow"].iloc[-1]
        rsi = self.stock_data["rsi"].iloc[-1]

        if ma_fast > ma_slow and rsi < 70:  # Confirmação de compra
            return "LONG"
        elif ma_fast < ma_slow and rsi > 30:  # Confirmação de venda
            return "SHORT"
        return None

    def execute_trade(self, decision):
        """Executa o trade com base na decisão da estratégia."""
        try:
            if decision == "LONG":
                self.open_position("LONG")
            elif decision == "SHORT":
                self.open_position("SHORT")
        except Exception as e:
            logging.error(f"Erro na execução do trade: {e}")

    def open_position(self, side):
        """Abre uma posição Long ou Short."""
        try:
            position_side = "BUY" if side == "LONG" else "SELL"
            quantity = self.calculate_trade_quantity()
            if quantity > 0:
                order = self.client_binance.futures_create_order(
                    symbol=self.operation_code,
                    side=position_side,
                    type="MARKET",
                    quantity=quantity
                )
                logging.info(f"Posição {side} aberta: {order}")
                self.actual_trade_position = True
        except Exception as e:
            logging.error(f"Erro ao abrir posição {side}: {e}")

    def execute(self):
        """Executa a lógica principal."""
        self.update_all_data()
        decision = self.moving_average_strategy()

        if decision and not self.actual_trade_position:
            self.execute_trade(decision)

if __name__ == "__main__":
    bot = BinanceFuturesTraderBot(STOCK_CODE, OPERATION_CODE, INITIAL_CAPITAL, LEVERAGE, CANDLE_PERIOD)
    while True:
        bot.execute()
        time.sleep(60)
