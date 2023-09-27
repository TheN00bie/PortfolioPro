import datetime as dt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots
from streamlit_extras.app_logo import add_logo
from PIL import Image
import QuantFunctions as qf
import mapmfunctions as mapm


#Page configs:


st.sidebar.image("logo/logo.png", width=220,
                 use_column_width=False)  

#page configs ends


st.markdown('''
# `PortfolioPro` : ***Personal Stock Portfolio Analytical Tool***
''')
st.sidebar.header('Select Stocks: ')

ticker = st.sidebar.text_input('Enter a ticker:')

today = dt.datetime.today()
start_date = st.sidebar.date_input('Start date:',
                                   today - dt.timedelta(days=365*1), 
                                   min_value=today - dt.timedelta(days=365*4),
                                   max_value=today - dt.timedelta(days=31*2))
end_date = st.sidebar.date_input('End date:',
                                 min_value=start_date +
                                 dt.timedelta(days=31*2),
                                 max_value=today)

if ticker:
    df = qf.get_price(ticker, start_date, end_date)

    
    if df.shape[0] == 0:
        st.error('Invalid Ticker')

    else:
        info_df = qf.get_info_df(ticker)

        st.header(info_df.loc['Name'][0])

        st.markdown('''
        ## Company Snapshot: ''')
        st.dataframe(info_df.drop(['Summary']).astype(str))

        closed_dates_list = qf.get_closed_dates(df)

        df = qf.get_MACD(df)
        df = qf.get_RSI(df)

        df = qf.get_trading_strategy(df)

        # Plot the four plots.
        fig = make_subplots(rows=4,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.005,
                            row_width=[0.2, 0.3, 0.3, 0.8])

        fig = qf.plot_candlestick_chart(fig,
                                               df,
                                               row=1,
                                               plot_EMAs=True,
                                               plot_strategy=True)

        fig = qf.plot_MACD(fig, df, row=2)
        fig = qf.plot_RSI(fig, df, row=3)
        fig = qf.plot_volume(fig, df, row=4)

        fig.update_xaxes(rangebreaks=[dict(values=closed_dates_list)],
                         range=[df['Date'].iloc[0] - dt.timedelta(days=3), df['Date'].iloc[-1] + dt.timedelta(days=3)])

        fig.update_layout(width=800,
                          height=800,
                          plot_bgcolor='#000000',
                          paper_bgcolor='#050505',
                          title={
                              'text': '{} - Dashboard'.format(ticker),
                              'y': 0.98
                          },
                          hovermode='x unified',
                          legend=dict(orientation='h',
                                      xanchor='left',
                                      x=0.05,
                                      yanchor='bottom',
                                      y=1.003))
        
        axis_lw, axis_color = 2, 'white'
        fig.update_layout(xaxis1=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis1=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis2=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis2=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis3=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis3=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis4=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis4=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        st.markdown('## Analytical Indicators: ')


        st.plotly_chart(fig)
        

        cagr1 = mapm.cagrfn(df)
        var1 = mapm.var(df)
        sortino1 = mapm.sortinoratio(df)
        bestyear = mapm.best_year(df)

        mapmdf = {
            'CAGR': cagr1*100,
            'Value at Risk': var1,
            'Sortino': sortino1,
            'Best Year': str(bestyear[0]),
            'Return in Best Year': bestyear[1]
         }
        
        st.markdown('## Key Performance Metrics: ')
        st.dataframe(mapmdf)
        st.markdown('## Final Manipulated Dataframe: ')
        st.dataframe(df)
        st.write('Still a lot to do , a lot to learn : )')
    
    
    
    
        
        
    

    



        
    
    
    
    
    
         



           
   


    
    
    


