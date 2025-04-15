import os
import sys
import time
from datetime import datetime
import logging
import pandas as pd
from binance.client import Client
from binance.enums import *
import requests

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a função de criação de logs
from src.logs.Logger import createLogOrder

# Chaves de API
api_key = "hlwZvNGCgajED6ZzRinKB5yUgQcUvyEkzpmLeRw2Y5J9NWNZ6D7PV6PbBXwlSawH"
secret_key = "tLKAMdXGyiXSuKrEQzLyD28TmQmwrPwVBo6MjvXo6I86w0aTwLi45eku39jlSj1i"

# CONFIGURAÇÕES
STOCK_CODE = "XRP"  # Moeda XRP
OPERATION_CODE = "XRPUSDT"  # Par XRPUSDT
CANDLE_PERIOD = Client.KLINE_INTERVAL_30MINUTE  # Período de 30 minutos

# Configuração de logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'logs', 'trading_bot.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def retry_on_timeout(func):
    """Decorator para tentar novamente em caso de timeout."""
    def wrapper(*args, **kwargs):
        max_retries = 3
        delay = 5  # Tempo de espera entre tentativas, em segundos
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ReadTimeout:
                logging.warning(f"Timeout na tentativa {attempt + 1}/{max_retries}. Retentando em {delay}s...")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Erro desconhecido ao executar {func.__name__}: {e}")
                break
        logging.error(f"Todas as tentativas falharam para {func.__name__}")
        raise requests.exceptions.ReadTimeout(f"Falha após {max_retries} tentativas.")
    return wrapper

class BinanceTraderBot:
    def __init__(self, stock_code, operation_code, candle_period):
        self.stock_code = stock_code
        self.operation_code = operation_code
        self.candle_period = candle_period

        # Inicializa o cliente Binance com timeout estendido
        self.client_binance = Client(
            api_key, secret_key, requests_params={"timeout": 20}
        )
        self.synchronize_time()

        # Variáveis de estado
        self.last_trade_decision = False
        self.actual_trade_position = False
        self.last_stock_account_balance = 0.000
        self.stock_data = pd.DataFrame()

        # Atualiza dados iniciais
        self.update_all_data()
        print('__________________________________________')
        print('Robo Trader iniciado...')

    def synchronize_time(self):
        """Sincroniza o horário local com o da Binance."""
        try:
            server_time = self.client_binance.get_server_time()
            local_time = int(time.time() * 1000)
            diff = server_time['serverTime'] - local_time
            self.client_binance.timestamp_offset = diff  # Ajusta o timestamp offset
            logging.info(f"Horário sincronizado com diferença de {diff}ms.")
        except Exception as e:
            logging.error(f"Erro ao sincronizar horário: {e}")

    @retry_on_timeout
    def get_updated_account_data(self):
        try:
            return self.client_binance.get_account(recvWindow=60000)
        except Exception as e:
            logging.error(f"Erro ao obter dados da conta: {e}")
            return {}

    def get_base_asset_balance(self):
        """Obtém o saldo disponível do ativo base (USDT)."""
        try:
            for asset in self.account_data.get('balances', []):
                if asset['asset'] == 'USDT':
                    return float(asset['free'])
        except Exception as e:
            logging.error(f"Erro ao obter saldo do ativo base: {e}")
        return 0.0

    def get_last_stock_account_balance(self):
        try:
            for stock in self.account_data.get('balances', []):
                if stock['asset'] == self.stock_code:
                    return float(stock['free'])
        except Exception as e:
            logging.error(f"Erro ao obter saldo do ativo {self.stock_code}: {e}")
        return 0.0

    def get_actual_trade_position(self):
        return self.last_stock_account_balance > 0.001

    @retry_on_timeout
    def get_stock_data_close_price_open_time(self):
        try:
            candles = self.client_binance.get_klines(
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

    def get_lot_size_details(self):
        """Obtém os detalhes de tamanho de lote para o par de negociação."""
        try:
            symbol_info = self.client_binance.get_symbol_info(self.operation_code)
            for filter in symbol_info['filters']:
                if filter['filterType'] == 'LOT_SIZE':
                    return {
                        "minQty": float(filter['minQty']),
                        "maxQty": float(filter['maxQty']),
                        "stepSize": float(filter['stepSize'])
                    }
        except Exception as e:
            logging.error(f"Erro ao obter detalhes de LOT_SIZE: {e}")
            return None

    def update_all_data(self):
        self.account_data = self.get_updated_account_data()
        self.last_stock_account_balance = self.get_last_stock_account_balance()
        self.actual_trade_position = self.get_actual_trade_position()
        self.stock_data = self.get_stock_data_close_price_open_time()

    def buy_stock(self):
        if not self.actual_trade_position:
            try:
                # Obter saldo disponível do ativo base
                base_balance = self.get_base_asset_balance()
                if base_balance <= 0:
                    logging.error("Saldo insuficiente no ativo base.")
                    return False

                # Obter preço atual do ativo
                ticker_price = float(self.client_binance.get_symbol_ticker(symbol=self.operation_code)['price'])

                # Calcular a quantidade máxima que pode ser comprada
                max_quantity = base_balance / ticker_price

                # Ajustar quantidade para atender ao stepSize
                lot_size_details = self.get_lot_size_details()
                step_size = lot_size_details["stepSize"]
                adjusted_quantity = max_quantity // step_size * step_size

                # Verificar se a quantidade ajustada está acima do mínimo permitido
                if adjusted_quantity < lot_size_details["minQty"]:
                    logging.error("Quantidade ajustada está abaixo do limite mínimo.")
                    return False

                # Criar ordem de compra
                order_buy = self.client_binance.create_order(
                    symbol=self.operation_code,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=adjusted_quantity,
                    recvWindow=60000
                )
                logging.info(f"Ordem de compra criada: {order_buy}")
                self.actual_trade_position = True
                createLogOrder(order_buy)
                return order_buy
            except Exception as e:
                logging.error(f"Erro ao comprar: {e}")
                return None
        else:
            logging.warning("Erro ao comprar: posição já comprada.")
        return False

    def execute(self):
        self.update_all_data()

        print('__________________________________________')
        print(f'Executado ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
        print(f'Posição atual: {"Comprado" if self.actual_trade_position else "Vendido"}')
        print(f'Balanço atual: {self.last_stock_account_balance} ({self.stock_code})')

        if not self.actual_trade_position:
            self.buy_stock()

if __name__ == "__main__":
    MaTrader = BinanceTraderBot(STOCK_CODE, OPERATION_CODE, CANDLE_PERIOD)
    while True:
        MaTrader.execute()
        time.sleep(60)
