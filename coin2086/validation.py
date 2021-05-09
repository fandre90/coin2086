import pandas as pd

SUPPORTED_CRYPTOS = [
    "BTC",
    "ETH",
    "XRP",
    "UNI",
    "LTC",
    "LINK",
    "XLM",
    "BCH",
    "AAVE",
    "SNX",
    "BAT",
    "MKR",
    "ZRX",
    "YFI",
    "UMA",
    "OMG",
    "KNC",
    "SDC",
    "PAX",
]


def check_trades(trades):
    mandatory_columns = set(
        [
            "datetime",
            "trade_side",
            "cryptocurrency",
            "quantity",
            "price",
            "base_currency",
            "amount",
            "fee",
        ]
    )
    missing = mandatory_columns - set(trades.columns)
    if len(missing) > 0:
        raise ValueError(f"Missing columns from trades dataframe {missing}")
    currencies = set(trades["base_currency"].drop_duplicates())
    if currencies != set(["EUR"]):
        raise ValueError("Base currency (base_currency) must be EUR for all trades")
    sides = set(trades["trade_side"].drop_duplicates())
    if sides != set(["SELL", "BUY"]):
        raise ValueError("Trade side (trade_side) must be either BUY or SELL")
    sorted_supported = ",".join(sorted(SUPPORTED_CRYPTOS))
    supported = set(SUPPORTED_CRYPTOS)
    cryptos = set(trades["cryptocurrency"].drop_duplicates())
    unsupported = cryptos - supported
    if len(unsupported) > 0:
        unsupported_sorted = ",".join(sorted(list(unsupported)))
        raise ValueError(
            f"Unsupported cryptocurrencies: {unsupported_sorted} "
            + f"supported currencies are: {sorted_supported}"
        )
    unsigned_cols = ["quantity", "price", "amount", "fee"]
    subset = trades[unsigned_cols]
    any_negative = (subset < 0).any(axis=None)
    if any_negative:
        cols = ",".join(unsigned_cols)
        raise ValueError(
            f"The columns {cols} are unsigned. All values MUST be positive."
        )
    sorted_trades = trades.sort_values("datetime").reset_index()
    sorted_trades = sorted_trades.drop(columns="index")
    if not sorted_trades.equals(trades):
        raise ValueError(
            f"It looks like your trades are not sorted by increasing datetime "
            f"with a monotic index. This can usually be fixed with "
            f"trades.sort_values('datetime').reset_index().drop(columns='index')"
        )
    trades["datetime"] = pd.to_datetime(trades["datetime"])
