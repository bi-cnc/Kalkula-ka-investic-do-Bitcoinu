import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Nastavení Streamlitu pro zobrazení grafů
st.set_option('deprecation.showPyplotGlobalUse', False)

from datetime import timedelta

def fetch_data(start_date, end_date):
    # Přidání jednoho dne k end_date
    end_date_plus_one = end_date + timedelta(days=1)
    
    bitcoin_data = yf.download("BTC-USD", start=start_date, end=end_date_plus_one)
    czk_usd_rate = yf.download("CZK=X", start=start_date, end=end_date_plus_one)
    return bitcoin_data, czk_usd_rate

# start_date = datetime(2021, 1, 1)
# end_date = datetime(2021, 2, 1)

# data = fetch_data(start_date, end_date)


# Výpočet zisku/ztráty a procentuální změny
def calculate_profit_loss(bitcoin_data, czk_usd_rate, investment_czk):
    starting_price = bitcoin_data['Close'].iloc[0]
    ending_price = bitcoin_data['Close'].iloc[-1]
    starting_rate = czk_usd_rate['Close'].iloc[0]
    ending_rate = czk_usd_rate['Close'].iloc[-1]

    investment_usd = investment_czk / starting_rate
    bitcoins_purchased = investment_usd / starting_price
    final_value_usd = bitcoins_purchased * ending_price

    final_value_czk = final_value_usd * ending_rate
    profit_loss_czk = final_value_czk - investment_czk

    # Výpočet procentuální změny
    profit_loss_percentage = (profit_loss_czk / investment_czk) * 100

    return profit_loss_czk, profit_loss_percentage

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def thousands_separator(x, pos):
    """Pomocná funkce pro formátování s mezerou jako oddělovačem tisíců."""
    return f'{x:,.0f}'.replace(',', ' ')

def plot_bitcoin_data(bitcoin_data, start_date, end_date):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(bitcoin_data.index, bitcoin_data['Close'], label='Cena bitcoinu (USD)', color='#FF4B4B')

    # Nastavení formátu popisků na ose Y
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_separator))

    ax.set_xlabel('Datum',fontweight='bold')
    ax.set_ylabel('Cena (USD)',fontweight='bold')
    ax.set_title('Historie ceny Bitcoinu',fontweight='bold',pad=10)
    
    ax.legend()
    st.pyplot(fig)


# Streamlit aplikace
def main():
    st.title("Kdybych investoval, kolik bych vydělal nebo prodělal?")
    large_font = "<h2 style='font-size:16px; color: black;'>Kalkulačka investic do bitcoinu 🚀</h2>"
    st.markdown(large_font, unsafe_allow_html=True)
    max_start_date = datetime.now() - timedelta(days=7)

    start_date = st.date_input("Den investice", datetime(2020, 1, 1),max_value=max_start_date)
    end_date = st.date_input("Den výběru peněz", datetime.now())
    investment_czk = st.number_input("Zadejte investovanou částku v Kč", min_value=0.0, value=10000.0)

    # Kontrola, zda start_date není po end_date a nejsou stejná
    if start_date >= end_date:
        st.error("Datum investice nemůže být později než datum výběru peněz. Prosím, upravte data.")
        bitcoin_data, czk_usd_rate = fetch_data(start_date, end_date)
    else:
        # Pokud jsou data v pořádku, zobrazit tlačítko
        bitcoin_data, czk_usd_rate = fetch_data(start_date, end_date)
        if st.button("Spočítejte potenciální zisk/ztrátu"):
            profit_loss_czk, profit_loss_percentage = calculate_profit_loss(bitcoin_data, czk_usd_rate, investment_czk)
            bitcoin_data, czk_usd_rate = fetch_data(start_date, end_date)
            formatted_profit_loss = "{:,.0f}".format(profit_loss_czk).replace(",", " ")  # Nahrazení čárky mezerou
            formatted_profit_loss += " Kč"  # Přidání "Kč" místo "CZK"


            if profit_loss_czk > 0:
                formatted_profit_loss_percentage = "+{:.2f} %".format(profit_loss_percentage)
                st.success(f"Potenciální zisk: {formatted_profit_loss} ({formatted_profit_loss_percentage})")
            else:
                formatted_profit_loss_percentage = "{:.2f} %".format(profit_loss_percentage)
                st.error(f"Potenciální ztráta: {formatted_profit_loss} ({formatted_profit_loss_percentage})")

    # Zobrazit graf
    st.write("")
    plot_bitcoin_data(bitcoin_data, start_date, end_date)

if __name__ == "__main__":
    main()
