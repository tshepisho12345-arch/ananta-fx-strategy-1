from data_loader import fetch_bond_yields
from signal_generator import generate_ananta_signals

def run_pipeline():
    print("--- ANANTA FX STRATEGY PIPELINE ---")
    print("Fetching bond yield data...")
    yields = fetch_bond_yields()
    
    print("Generating signals...")
    scores, active_signals = generate_ananta_signals(yields)
    
    print("\n--- ACTIVE PAIR SUB-SIGNALS (Above Median Filter) ---")
    print(active_signals)
    
    print("\n--- FINAL CURRENCY RANKINGS ---")
    print(scores.to_string(index=False))
    
    longs = scores[scores['ANANTA_Score'] > 0]['Currency'].tolist()
    shorts = scores[scores['ANANTA_Score'] < 0]['Currency'].tolist()
    
    print("\n--- TRADING SUMMARY ---")
    print(f"LONG Candidates  (Strong Yield Spreads): {', '.join(longs)}")
    print(f"SHORT Candidates (Weak Yield Spreads)  : {', '.join(shorts)}")

if __name__ == "__main__":
    run_pipeline()
