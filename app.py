import streamlit as st
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt

# Nastavení Streamlitu pro zobrazení grafů
st.set_option('deprecation.showPyplotGlobalUse', False)

def fetch_data(start_date, end_date):
    bitcoin_data = yf.download("BTC-USD", start=start_date, end=end_date)
    czk_usd_rate = yf.download("CZK=X", start=start_date, end=end_date)
    return bitcoin_data, czk_usd_rate

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

def plot_bitcoin_data(bitcoin_data, start_date, end_date):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(bitcoin_data.index, bitcoin_data['Close'], label='Cena Bitcoinu (USD)', color='#FF4B4B')  # Použití hex kódu pro barvu
    ax.set_xlabel('Datum')
    ax.set_ylabel('Cena (USD)')
    ax.set_title('Historie ceny Bitcoinu')
    
    ax.legend()
    st.pyplot(fig)

# Streamlit aplikace
def main():
    st.title("Kdybych investoval, kolik bych vydělal nebo prodělal?")
    st.divider()
    st.text("Kalkulačka investic do Bitcoinu")

    start_date = st.date_input("Zadejte počáteční datum", datetime(2020, 1, 1))
    end_date = st.date_input("Zadejte koncové datum", datetime.now())
    investment_czk = st.number_input("Zadejte investovanou částku v Kč", min_value=0.0, value=10000.0)

    bitcoin_data, czk_usd_rate = fetch_data(start_date, end_date)

    if st.button("Spočítejte potenciální zisk/ztrátu"):
        profit_loss_czk, profit_loss_percentage = calculate_profit_loss(bitcoin_data, czk_usd_rate, investment_czk)
        formatted_profit_loss = "{:,.0f}".format(profit_loss_czk).replace(",", " ")  # Nahrazení čárky mezerou
        formatted_profit_loss += " Kč"  # Přidání "Kč" místo "CZK"

        if profit_loss_czk > 0:
            formatted_profit_loss_percentage = "+{:.2f}%".format(profit_loss_percentage)
            st.success(f"Potenciální zisk: {formatted_profit_loss} ({formatted_profit_loss_percentage})")
        else:
            formatted_profit_loss_percentage = "{:.2f}%".format(profit_loss_percentage)
            st.error(f"Potenciální ztráta: {formatted_profit_loss} ({formatted_profit_loss_percentage})")

    # Zobrazit graf
    st.write("")
    plot_bitcoin_data(bitcoin_data, start_date, end_date)

if __name__ == "__main__":
    main()
