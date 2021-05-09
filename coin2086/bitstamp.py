import pandas as pd


def split_column_get_value(col):
    return col.str.split().str[0].astype(float)


def split_column_get_unit(col):
    return col.str.split().str[1]


def normalize_bitstamp_transactions(trans, start_date):
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
