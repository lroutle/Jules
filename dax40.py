# dax40_recommendations_with_performance.py
import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import DateOffset

# DAX 40 tickers with company names
dax40 = [
    ("ADS.DE", "Adidas AG"), ("AIR.DE", "Airbus SE"), ("ALV.DE", "Allianz SE"),
    ("BAS.DE", "BASF SE"), ("BAYN.DE", "Bayer AG"), ("BEI.DE", "Beiersdorf AG"),
    ("BNR.DE", "Brenntag SE"), ("BMW.DE", "BMW AG"), ("CON.DE", "Continental AG"),
    ("1COV.DE", "Covestro AG"), ("DTG.DE", "Daimler Truck Holding AG"),
    ("DHER.DE", "Delivery Hero SE"), ("DBK.DE", "Deutsche Bank AG"),
    ("DB1.DE", "Deutsche Börse AG"), ("DHL.DE", "DHL Group (Deutsche Post)"),
    ("DTE.DE", "Deutsche Telekom AG"), ("EOAN.DE", "E.ON SE"),
    ("FRE.DE", "Fresenius SE & Co. KGaA"), ("FME.DE", "Fresenius Medical Care AG"),
    ("HEI.DE", "Heidelberg Materials AG"), ("HFG.DE", "HelloFresh SE"),
    ("HEN3.DE", "Henkel AG & Co. KGaA"), ("IFX.DE", "Infineon Technologies AG"),
    ("LIN.DE", "Linde plc"), ("MBG.DE", "Mercedes‑Benz Group AG"),
    ("MRK.DE", "Merck KGaA"), ("MTX.DE", "MTU Aero Engines AG"),
    ("MUV2.DE", "Munich Reinsurance"), ("P911.DE", "Porsche AG"),
    ("PAH3.DE", "Porsche Automobil Holding SE"), ("PUM.DE", "Puma SE"),
    ("QIA.DE", "Qiagen N.V."), ("RWE.DE", "RWE AG"), ("SAP.DE", "SAP SE"),
    ("SRT3.DE", "Sartorius AG"), ("SIE.DE", "Siemens AG"),
    ("ENR.DE", "Siemens Energy AG"), ("SHL.DE", "Siemens Healthineers AG"),
    ("SY1.DE", "Symrise AG"), ("VOW3.DE", "Volkswagen AG"),
    ("VNA.DE", "Vonovia SE"), ("ZAL.DE", "Zalando SE"),
    ("HNR1.DE", "Hannover Rück SE"), ("CBK.DE", "Commerzbank AG"),
    ("RHM.DE", "Rheinmetall AG"), ("WCH.DE", "Wacker Chemie AG")
]

def compute_performance(hist):
    if hist is None or hist.empty:
        return "N/A", "N/A", "N/A"
    adj = hist["Adj Close"].dropna()
    if adj.empty:
        return "N/A", "N/A", "N/A"
    current = adj.iloc[-1]

    def perf(offset):
        target_date = adj.index[-1] - offset
        if target_date < adj.index[0]:
            return "N/A"
        past_date = adj.index.asof(target_date)
        if pd.isna(past_date):
            return "N/A"
        past = adj.loc[past_date]
        return round((current - past) / past * 100, 2)

    p6 = perf(DateOffset(months=6))
    p12 = perf(DateOffset(years=1))
    p5 = perf(DateOffset(years=5)) if len(adj) > 250*5 else "N/A"
    return p6, p12, p5

results = []

for ticker, company in dax40:
    stock = yf.Ticker(ticker)

    # Current price
    try:
        last_day = stock.history(period="1d", auto_adjust=True)
        if not last_day.empty:
            price = round(float(last_day["Close"].iloc[-1]), 2)
        else:
            price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice") or "N/A"
    except Exception:
        price = "N/A"

    # Performance
    try:
        hist = stock.history(period="max", auto_adjust=True)
        perf_6m, perf_12m, perf_5y = compute_performance(hist)
    except Exception:
        perf_6m = perf_12m = perf_5y = "N/A"

    # Analyst recommendations
    strong_buy = buy = hold = sell = strong_sell = total = 0
    pct = "N/A"
    classification = "No Data"
    try:
        recs = stock.recommendations_summary
        if recs is not None and not recs.empty:
            latest = recs.iloc[0]
            strong_buy = int(latest.get("strongBuy", 0) or 0)
            buy = int(latest.get("buy", 0) or 0)
            hold = int(latest.get("hold", 0) or 0)
            sell = int(latest.get("sell", 0) or 0)
            strong_sell = int(latest.get("strongSell", 0) or 0)
            total = strong_buy + buy + hold + sell + strong_sell
            if total > 0:
                pct = round((strong_buy + buy) / total * 100, 2)
                classification = "Strong Buy" if pct >= 60 else "Buy" if pct >= 40 else "Hold"
    except Exception:
        pass

    results.append({
        "Ticker": ticker, "Company": company,
        "Current Price": price,
        "6M %": perf_6m, "12M %": perf_12m, "5Y %": perf_5y,
        "Strong Buy": strong_buy, "Buy": buy, "Hold": hold,
        "Sell": sell, "Strong Sell": strong_sell,
        "Total Analysts": total,
        "Buy+StrongBuy %": pct,
        "Classification": classification
    })

df = pd.DataFrame(results)
df.to_csv("dax40_recommendations_with_performance.csv", index=False)
print(df)
