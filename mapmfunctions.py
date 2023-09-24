import numpy as np

# var function

def var(df, confidence_level=0.95):
        # Calculate daily returns
        df['Daily_Returns'] = df['Adj Close'].pct_change()

        # Calculate the VaR
        returns = df['Daily_Returns'].dropna()
        var = np.percentile(returns, (1 - confidence_level) * 100)

        return var
    
# cagr function 

def cagrfn(df):
        if 'Date' not in df.columns or 'Adj Close' not in df.columns:
            return "Error: DataFrame must have 'Date' and 'Adj Close' columns."
        start_date = df['Date'].iloc[0]
        end_date = df['Date'].iloc[-1]
        num_years = (end_date - start_date).days / 365.0
        initial_price = df['Adj Close'].iloc[0]
        final_price = df['Adj Close'].iloc[-1]
        cagr = (final_price / initial_price) ** (1 / num_years) - 1

        return cagr

# sortino function

def sortinoratio(df, risk_free_rate=0.0):
        if 'Daily_Returns' not in df.columns:
            return "Error: DataFrame must have a 'Daily_Returns' column."
        downside_returns = df['Daily_Returns'][df['Daily_Returns'] < 0]
        downside_deviation = np.std(downside_returns, ddof=1)
        expected_return = df['Daily_Returns'].mean()
        sortino_ratio = (expected_return - risk_free_rate) / downside_deviation

        return sortino_ratio

 # best year & return   
def best_year(df):
        if 'Date' not in df.columns or 'Daily_Returns' not in df.columns:
            return "Error: DataFrame must have 'Date' and 'Daily_Returns' columns."
        df['Year'] = df['Date'].dt.year
        annual_returns = df.groupby('Year')['Daily_Returns'].sum()
        best_year = annual_returns.idxmax()
        best_return = annual_returns.max()

        return best_year ,  best_return*100



