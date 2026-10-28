ananta-fx-strategy/
│
├── .github/
│   └── workflows/
│       └── daily_signal.yml     # Automated workflow configuration
│
├── src/
│   ├── data_loader.py          # Fetches bond yields & FX prices
│   ├── signal_generator.py     # Calculates spreads, noise filter, & scores
│   └── main.py                 # Core execution script
│
├── requirements.txt            # Python dependencies
└── README.md
