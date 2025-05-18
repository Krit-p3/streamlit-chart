import streamlit as st
import time
import numpy as np
import pandas as pd

st.title("Mock Backtest Data Stream")

# Example DataFrame (for backtest data)
rows = 30
df = pd.DataFrame({
    "AssetA": np.random.randn(rows).cumsum(),
    "AssetB": np.random.randn(rows).cumsum(),
})

placeholder = st.empty()

# Step through the DataFrame, appending each row, and plot
accumulated_df = pd.DataFrame()
for i in range(rows):
    new_row = df.iloc[i]  # next row to append
    # Convert 'new_row' (Series) to a DataFrame row and concatenate
    accumulated_df = pd.concat([accumulated_df, new_row.to_frame().T], ignore_index=True)
    placeholder.line_chart(accumulated_df)
    time.sleep(0.5)