import pandas as pd


def split_column_get_value(col):
    return col.str.split().str[0].astype(float)


def split_column_get_unit(col):
    return col.str.split().str[1]


def normalize_bitstamp_transactions(trans, start_date):
    """
    Take a DataFrame of transactions as exported by Bitstamp, and
    return a DataFrame of *normalized* trades, that can be used by the functions
    of the public API of coin2086. Transactions exported from Bitstamp may include
    deposits, withdrawals or other operations that are not used for the
    computation of the PnL. These operations will be filtered out, and only
    crypto-currencies purchase and sales will be kept.

    Args:
        trans (pandas.DataFrame): A DataFrame of transactions, as exported from your
            Bitstamp profile. This is usually exported as csv from Bitstamp, and
            read with `pandas.read_csv()`.
        start_date(timestamp, str or datetime): The start date at which to
            start parsing transations from. Transactions before start_date will
            be ignored. This will be converted into a pandas datetime using
            `pandas.to_datetime()`.

    Returns:
        pandas.DataFrame: A DataFrame of normalized crypto-currency buy and sell
        trades, that can be used by coin2086 public API functions.
    """
    # Select only trade (Market) transaction and ignore Deposits, Withdrawals etc.
    trades = trans[trans["Type"] == "Market"].copy()
    trades["datetime"] = pd.to_datetime(trades["Datetime"])
    trades["quantity"] = split_column_get_value(trades["Amount"])
    trades["cryptocurrency"] = split_column_get_unit(trades["Amount"])
    trades["price"] = split_column_get_value(trades["Rate"])
    trades["rate_unit"] = split_column_get_unit(trades["Rate"])
    trades["amount"] = split_column_get_value(trades["Value"])
    trades["base_currency"] = split_column_get_unit(trades["Value"])
    trades["fee"] = split_column_get_value(trades["Fee"])
    trades["fee_unit"] = split_column_get_unit(trades["Fee"])
    trades["trade_side"] = trades["Sub Type"].str.upper()
    cols = [
        "datetime",
        "trade_side",
        "cryptocurrency",
        "quantity",
        "price",
        "base_currency",
        "amount",
        "fee",
    ]
    trades = trades[trades["datetime"] > pd.to_datetime(start_date)].reset_index()
    return trades[cols]
