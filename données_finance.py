import yfinance as yf

title = "BTC-EUR"
fichier = yf.download(
    title, start="2019-02-01", end="2025-11-26", interval="1d", threads=False
)
fichier.to_csv("cour-bitcoin-2019-2025.csv")
