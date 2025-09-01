import ccxt
import time
import pandas as pd
import os

def run_bot():
    # Conexión a Binance
    exchange = ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_API_SECRET'),
        'enableRateLimit': True,
    })
    symbol = 'XMR/USDT'
    print("🤖 Bot de trading iniciado. Esperando señales...")

    in_position = False

    while True:
        try:
            # Obtener datos (1h)
            ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            close = df['close']

            # Medias móviles
            sma10 = close.rolling(10).mean().iloc[-1]
            sma30 = close.rolling(30).mean().iloc[-1]
            sma10_prev = close.rolling(10).mean().iloc[-2]
            sma30_prev = close.rolling(30).mean().iloc[-2]

            precio_actual = close.iloc[-1]

            # Señal de compra
            if sma10 > sma30 and sma10_prev <= sma30_prev and not in_position:
                print(f"🟢 COMPRA | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")
                in_position = True

            # Señal de venta
            elif sma10 < sma30 and sma10_prev >= sma30_prev and in_position:
                print(f"🔴 VENTA | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")
                in_position = False

            else:
                print(f"🟡 Esperando... | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(60)  # Revisa cada 60 segundos

if __name__ == "__main__":
    run_bot()
