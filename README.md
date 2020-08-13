[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dwIXHirrgodGLoR5pcNJXvXxiyfKVu5W?usp=sharing)

# Binance trading performance
Trading profit/loss calculation on Binance spot market via API.<br>

Better to open in Google Colab notebook (link above) - it allows to calculate performance without the need to install any software.
Alternatively download .ipynb file and open it in Jupyter Notebook or download binance_api.py and binance_trading_performance.py files and run them in your favotite python IDE.

How to use in Google Colab:
1. Open Colab link
2. Save a copy to your account (login to your google account if needed):
File -> Save a copy in Drive
3. Make changes to your saved copy only (To avoid mistakes close the tab with the shared version)
4. Check that your notebook is not visible to anyone:
Find Share button at the top right -> Restricted (Only people added can open with this link)
4. Change API_key, API_secret to yours. Use **read-only** keys.
5. Change market and dates to the one you need.
6. Run the code:
Runtime -> Run all (or Ctrl + F9)

This calculation is based upon hummingbot performance measuring:<br>
https://hummingbot.io/blog/2019-07-measure-performance-crypto-trading/

Credits to [@Bablofil](https://github.com/Bablofil/binance-api) for Binance api.
