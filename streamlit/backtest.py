import yfinance as yf 
import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import numpy as np 
from enum import Enum
import statsmodels.formula.api as smf 



# Get data
@st.cache_data
def load_data(tickers):
    df = yf.download(tickers, start='2020-01-01', end='2024-12-31', auto_adjust=False)['Close']
    df.columns = df.columns.str.replace('-', '_', regex=False)
    return df


@st.cache_data
def volatility(data, windows):
    data = np.log(data/data.shift(1)).dropna()
    vol = data.rolling(windows).std()
    return vol



tickers = ['BTC-USD', 'SOL-USD', 'ETH-USD', 'BNB-USD', 'LTC-USD', 'LINK-USD', 'AAVE-USD', 'MKR-USD']

data = load_data(tickers)

tickers = data.columns.tolist()

@st.cache_data
def cumulative_return(data):
    ret = np.log(data/data.shift(1))
    cum_ret = ret.cumsum().apply(np.exp) - 1
    return cum_ret


# Enum for Transform Data 
class TfOption(Enum):
    Default = ""
    Normalize = "Normalize"
    Cumulative = "Cumulative"


# Selectbox 
option = st.multiselect(
    "Select Asset",
    tickers,
    default=[tickers[0]]
)

tf_data = st.selectbox(
    "Option",
    [m.value for m in TfOption],
    index=0
)


st.title("Prices")

# Slider date 
first_date = data.index.min().to_pydatetime()
latest_date = data.index.max().to_pydatetime()

time_interval = st.slider(
    'Select time range',
    min_value=first_date,
    max_value=latest_date,
    value= (first_date, latest_date),
    format="MM/DD/YY"
)

@st.fragment
def plot_chart():
    if option:
        start_date, end_date = time_interval 
        _data = data.loc[start_date:end_date]
        chart_data =  _data[option]
        st.session_state.data = chart_data
        if tf_data:
            if tf_data == "Cumulative":
                chart_data = cumulative_return(chart_data)
    
            if tf_data == "Normalize":
                chart_data = chart_data / chart_data.iloc[0]
        
        st.line_chart(chart_data)



@st.fragment
def plot_vol():

    windows= st.selectbox(
        "Time windows",
        [5,10,15,20,30],
        index=0
    )
    vol = volatility(st.session_state.data, windows)
    st.line_chart(vol
                  #color=["#FF0000"]
                  )

plot_chart()


plot_vol()

tab1, tab2 = st.tabs(["Tab1", "Tab2"])

tab1.table(st.session_state.data.describe())

@st.fragment
def ols():
    all_tickers = st.session_state.data.columns.tolist()

    if 'BTC_USD' in all_tickers:
        all_tickers.remove('BTC_USD')
        formula = "BTC_USD ~ " + " + ".join(all_tickers)
        # Fit OLS model
        model = smf.ols(formula, data=st.session_state.data).fit()
    else: 
        formula = "BTC_USD ~ " +  " + ".join(all_tickers)
        start_date, end_date = time_interval 
        _data = data.loc[start_date:end_date]
        _data = _data[['BTC_USD']]
        df = pd.concat([st.session_state.data, _data['BTC_USD']],axis=1)
        model = smf.ols(formula, data=df).fit()
    return model.summary2().tables[1]

tab2.table(ols())


