import logging
import collections
import datetime as dt

import requests
import pandas as pd

from . import pricedownload
from .validation import check_trades


logger = logging.getLogger(__name__)


def valuate_portfolio(trades, initial_portfolio=None):
    """Determines the valuation of the porfolio before each sale

    The formula used to compute your taxable PnL (profit and loss) from each
    sale requires determining the total value of your portfolio of
    crypto-currencies before each sale. This is the purpose of this function.
    This function retrieves the prices of crypto-currencies from the public
    Bitstamp API to determine the value of your portfolio. Even if you did not
    trade on Bistamp, the prices should be close enough for our purposes.
    This function returns a column multi-indexed DataFrame. The first level
    of the column index is either quantity, sell_price, public_price, ref_price
    and value. The second level of the index are the crypto-currencies. For
    instance::

                       quantity      sell_price         public_price
        cryptocurrency      BTC  ETH        BTC     ETH          BTC     ETH
        2                   1.0  5.0    8722.70     NaN      8722.70  300.84
        3                   0.5  5.0        NaN  285.07      8509.24  285.07
        6                   1.5  5.0   19531.69     NaN     19531.69  527.45

                       ref_price              value
        cryptocurrency       BTC     ETH        BTC      ETH      TOTAL
        2                8722.70  300.84   8722.700  1504.20  10226.900
        3                8509.24  285.07   4254.620  1425.35   5679.970
        6               19531.69  527.45  29297.535  2637.25  31934.785

    The meaning of each column is as follows:

    quantity
        The quantity of each crypto-currency in the porfolio
    sell_price
        The price you sold a crypto-currency at. It will be a non-null value for
        the crypto-currency you sold, and NaN for the other ones
    public_price
        The known price on Bitstamp of each crypto-currency at the moment
        of your sale trade (the close price of the minute you traded is used)
    ref_public
        The union of sell_price and public_price. For a given crypto-currency,
        if the sale price is known, it is used, otherwise public_price is used
    value
        The value of each of your crypto-currencies holdings. This is computed
        by multiplying quantity by ref_price. This column has an additional
        TOTAL sub-column that gives the total value of your portfolio

    Note that the indexes of this DataFrame are the indexes of the sales
    (trades with trade_side = SELL) of your trades DataFrame.

    Args:
        trades (pandas.DataFrame): .. include:: ../../docs/includes/arg_trades.rst
        initial_portfolio (dict):  .. include:: ../../docs/includes/arg_initial_portfolio.rst

    Returns:
        pandas.DataFrame: The DataFrame containing the composition of the
            portfolio, the valuation of the portfolio and the reference
            prices used for valuation before each sale.
    """
    check_trades(trades)
    sales = trades[trades["trade_side"] == "SELL"]
    portfolio = unstack_portfolio_composition(trades, sales, initial_portfolio)
    portfolio = add_sell_prices(portfolio, sales)
    portfolio = add_public_prices(portfolio, sales)
    portfolio = merge_rates_and_valuate(portfolio)
    return portfolio[["quantity", "sell_price", "public_price", "ref_price", "value"]]


def add_initial_portfolio(portfolio, initial_portfolio):
    if initial_portfolio is None:
        return
    for crypto, qty in initial_portfolio.items():
        if crypto not in portfolio["quantity"].columns:
            portfolio["quantity", crypto] = 0.0
        portfolio["quantity", crypto] += qty


def unstack_portfolio_composition(trades, sales, initial_portfolio):
    portfolio = trades[["cryptocurrency", "quantity", "trade_side"]].copy()
    # Compute a signed quantity for each trade by multiplying by
    # -1 for sales and 1 for purchases
    portfolio["sign"] = -1
    portfolio.loc[portfolio["trade_side"] == "BUY", "sign"] = 1
    portfolio["quantity"] = portfolio["quantity"] * portfolio["sign"]
    portfolio = portfolio.drop(columns=["sign", "trade_side"])
    # Unstack the composition of the portofolio after each transaction
    portfolio = portfolio.set_index("cryptocurrency", append=True).unstack().fillna(0)
    # We need the valuation of the portoflio *before* each transaction
    # so shift by one
    portfolio["quantity"] = portfolio["quantity"].cumsum().shift(1, fill_value=0)
    # Add the initial portfolio to the first trade
    add_initial_portfolio(portfolio, initial_portfolio)
    return portfolio.reindex(sales.index)


def merge_rates_and_valuate(portfolio):
    portfolio = portfolio.stack()
    portfolio["ref_price"] = portfolio["sell_price"].fillna(portfolio["public_price"])
    portfolio["value"] = portfolio["ref_price"] * portfolio["quantity"]
    portfolio = portfolio.unstack()
    portfolio["value", "TOTAL"] = portfolio["value"].sum(axis=1)
    return portfolio


def add_sell_prices(portfolio, sales):
    sell_prices = sales[["cryptocurrency", "price"]]
    sell_prices = sell_prices.rename(columns={"price": "sell_price"})
    sell_prices = sell_prices.set_index("cryptocurrency", append=True).unstack()
    return portfolio.join(sell_prices, how="outer")


def add_public_prices(portfolio, sales):
    pricedown = pricedownload.reference_price_downloader()
    dated_portfolio = portfolio["quantity"].join(sales["datetime"])
    price_records = []
    for rec in dated_portfolio.to_dict(orient="records"):
        dtime = rec["datetime"]
        del rec["datetime"]
        price_rec = {}
        for crypto in rec.keys():
            price_rec[crypto] = pricedown.download_price(crypto, dtime.to_pydatetime())
        price_records.append(price_rec)
    public_prices = pd.DataFrame(price_records, index=sales.index)
    public_prices.columns = pd.MultiIndex.from_product(
        [["public_price"], public_prices.columns]
    )
    return portfolio.join(public_prices, how="outer")
