import streamlit as st 

pages = {
    "Strategy": [
        st.Page("streamlit/backtest.py", title="Portfolio Optimization"),
        st.Page("streamlit/summary.py", title="Summary")
    ],
    "Test":[
        st.Page("streamlit/real_time.py", title="Realtime"),
        st.Page("streamlit/state.py",title="State")
    ]
}

pg = st.navigation(pages)
pg.run()