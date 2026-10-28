import pandas as pd
import numpy as np

def generate_ananta_signals(yields_df, ma_window=20):
    """
    Implements ANANTA Signal Logic:
    1. Yield Spreads
    2. Normalized MA Deviation
    3. Median Noise Filter
    4. Net Currency Score Aggregation
    """
    currencies = list(yields_df.columns)
    sub_signals = {}

    # Step 1 & 2: Calculate Yield Differential & Normalized Deviation
    for i in range(len(currencies)):
        for j in range(i + 1, len(currencies)):
            c1, c2 = currencies[i], currencies[j]
            pair = f"{c1}/{c2}"
            
            # Differential
            diff = yields_df[c1] - yields_df[c2]
            
            # Rolling Moving Average
            ma = diff.rolling(window=ma_window).mean()
            
            # Normalized Sub-Signal
            sub_signal = (diff - ma) / ma.abs()
            sub_signals[pair] = sub_signal.iloc[-1]

    sub_sig_series = pd.Series(sub_signals).dropna()

    # Step 3: Noise Filtering (Median / 50th Percentile)
    abs_median = sub_sig_series.abs().median()
    filtered_signals = sub_sig_series[sub_sig_series.abs() >= abs_median]

    # Step 4: Aggregate Scores Across Currency Basket
    currency_scores = {c: 0 for c in currencies}
    
    for pair, val in filtered_signals.items():
        c1, c2 = pair.split('/')
        if val > 0:
            currency_scores[c1] += 1
            currency_scores[c2] -= 1
        else:
            currency_scores[c1] -= 1
            currency_scores[c2] += 1

    scores_df = pd.DataFrame(
        list(currency_scores.items()), 
        columns=['Currency', 'ANANTA_Score']
    ).sort_values(by='ANANTA_Score', ascending=False)

    return scores_df, filtered_signals
