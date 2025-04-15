import logging
from datetime import datetime

# Configuração de logging para garantir que os logs sejam bem formatados e salvos
logging.basicConfig(
    filename='src/logs/trading_bot.log',  # Arquivo de log
    level=logging.INFO,                   # Nível de log (INFO, DEBUG, WARNING, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def createLogOrder(order: dict):
    """
    Registra informações sobre uma ordem criada.
    
    Parâmetros:
        order (dict): Detalhes da ordem retornados pela API da Binance.
    """
    try:
        order_id = order.get("orderId", "N/A")
        symbol = order.get("symbol", "N/A")
        side = order.get("side", "N/A")
        quantity = order.get("origQty", "N/A")
        price = order.get("price", "N/A")
        timestamp = order.get("transactTime", None)
        if timestamp:
            timestamp = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp = "N/A"

        log_message = (
            f"Ordem criada:\n"
            f" - ID: {order_id}\n"
            f" - Par: {symbol}\n"
            f" - Tipo: {side}\n"
            f" - Quantidade: {quantity}\n"
            f" - Preço: {price}\n"
            f" - Data/Hora: {timestamp}\n"
        )

        # Escreve o log no arquivo
        logging.info(log_message)
        print(log_message)  # Opcional: imprime no console

    except Exception as e:
        logging.error(f"Erro ao criar log da ordem: {str(e)}")
        print(f"Erro ao criar log da ordem: {str(e)}")
