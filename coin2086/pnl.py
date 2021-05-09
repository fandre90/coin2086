import logging
import datetime as dt

from . import valuation
from .validation import check_trades

logger = logging.getLogger(__name__)


def add_portfolio_purchase_price(trades, initial_purchase_price):
    trades["portfolio_purchase_price"] = 0
    trades.loc[trades["trade_side"] == "BUY", "portfolio_purchase_price"] = (
        trades["amount"] + trades["fee"]
    )
    trades["portfolio_purchase_price"] = trades["portfolio_purchase_price"].cumsum()
    trades["portfolio_purchase_price"] += initial_purchase_price


def filter_sales_add_portfolio_value(trades, initial_portfolio):
    portfolio = valuation.valuate_portfolio(trades, initial_portfolio)
    print("Valuate done")
    value = portfolio["value", "TOTAL"]
    value = value.rename("portfolio_value").to_frame()
    sales = trades.join(value, how="inner")
    return sales


def compute_purchase_price_fraction(
    amount, value, purchase_price, purchase_price_net, fraction, fraction_sum
):
    frac_sum = 0
    for i in range(0, len(amount)):
        fraction_sum[i] = frac_sum
        # Decrease the portfolio purchase price by the sum of the fractions
        # of pruchase price aldready sold
        purchase_price_net[i] = purchase_price[i] - fraction_sum[i]
        # The percentage of the portfolio that was sold by this transaction
        percentage_sold = amount[i] / value[i]
        # Compute the fraction of the purchase price that was sold
        # by this transaction
        fraction[i] = purchase_price_net[i] * percentage_sold
        frac_sum += fraction[i]


def compute_taxable_pnls_detailed(
    trades, initial_portfolio=None, initial_purchase_price=0.0
):
    """Computes your taxable PnL for each sale in the trades DataFrame

    In the french tax law (CGI art. 150 VH), taxable events are sales of
    crypto-currencies for official (fiat) currencies such as Euro. The PnL
    (profit and loss) arising from each sale must be reported in the form 2086
    (Formulaire n°2086).

    This function computes the PnL to be reported for each sale on form 2086, and
    other information that also needs to be reported on form 2086. It returns
    a DataFrame such as::

                     datetime trade_side cryptocurrency  quantity    amount       fee
        2 2020-09-05 16:50:00       SELL            BTC       0.5   4361.35  21.80675
        3 2020-09-08 12:40:00       SELL            ETH       5.0   1425.35   7.12675
        6 2020-12-21 09:30:00       SELL            BTC       1.0  19531.69  97.65845

            amount_net  portfolio_value  portfolio_purchase_price
        2   4339.54325        10226.900                11286.4716
        3   1418.22325         5679.970                11286.4716
        6  19434.03155        31934.785                22507.6584

        purchase_price_fraction  purchase_price_fraction_sum
        2              4813.213477                     0.000000
        3              1624.420281                  4813.213477
        6              9828.616024                  6437.633759

           portfolio_purchase_price_net          pnl
        2                  11286.471600  -473.670227
        3                   6473.258123  -206.197031
        6                  16070.024641  9605.415526

    The meaning of each column is as follows:

    .. |reportable| replace:: **[!]** This information has to be reported on form 2086
        (see :py:func:`coin2086.compute_taxable_pnls` to known in which cell).

    datetime
        The date and time of your trade, copied from the input ``trades`` DataFrame.

        |reportable|
    trade_side
        The side (BUY or SELL) of your trade, copied from the input ``trades``
        DataFrame
    cryptocurrency
        The crypto currency you sold, copied from the input ``trades`` DataFrame
    quantity
        The quantity of crypto-currency you sold, copied from the input ``trades``
        DataFrame
    amount
        The amount in euro you received in exchange for you sale of
        crypto-currencies, copied from the input ``trades`` DataFrame.

        |reportable|
    fee
        The fees in euro you paid for your trade, copied from the input trades
        DataFrame.

        |reportable|
    amount_net
        The amount, net of fees, your received in exchange for your sale
        of crypto-currencies. This is amount - fee.
    portfolio_value
        The total value of your portfolio of crypto-currencies before the sale,
        as computed by :py:func:`coin2086.valuate_portfolio`

        |reportable|
    portfolio_purchase_price
        The total purchase price of your porfolio, net of fees, but not
        accouting for sales.

        |reportable|
    purchase_price_fraction
        The fraction of the purchase price that was sold (Fractions de capital
        initial, see Notice du formulaire n°2086). For instance, if : (1) your
        portfolio is worth 10226.90 Euros, (2) you receive 4339.54 Euros for a
        crypto-currency sale and (3) the total purchase price for your portfolio
        was 11286.4716, it will be considered that of have sold
        4339.54 / 10226.90 = 42.6458% of your portfolio. The purchase price for
        these 42.43% of your porfolio (purchase_price_fraction) is 42.6458%
        of 11286.4716 = 4813.213477.
    purchase_price_fraction_sum
        The cumulative sum of the purchase_price_fraction column

        |reportable|
    portfolio_purchase_price_net
        The total purchase price of your porfolio, net of fees, and net of the
        cumulative sum of the purchase price fractions. This is
        portfolio_purchase_price - purchase_price_fraction_sum.

        |reportable|
    pnl
        The PnL (profit and loss) for this sale. You will pay 30% of the
        ``sum()`` of this column as taxes, only if this is a positive number (no
        taxes if this is a negative number)

        |reportable|

    .. note::
        Note that the indexes of this DataFrame are the indexes of the sales
        (trades with trade_side = SELL) of your ``trades`` DataFrame.

    The input trades DataFrame must have one line per trade, as follows::

                     datetime trade_side cryptocurrency  quantity     price
        0 2020-07-28 10:20:00        BUY            BTC       1.0   9262.42
        1 2020-09-01 12:20:00        BUY            ETH       5.0    393.58
        2 2020-09-05 16:50:00       SELL            BTC       0.5   8722.70
        3 2020-09-08 12:40:00       SELL            ETH       5.0    285.07
        4 2020-09-16 17:10:00        BUY            BTC       1.0   9247.51
        5 2020-11-07 15:40:00        BUY            ETH       5.0    383.57
        6 2020-12-21 09:30:00       SELL            BTC       1.0  19531.69

        base_currency    amount       fee
        0           EUR   9262.42  46.31210
        1           EUR   1967.90   9.83950
        2           EUR   4361.35  21.80675
        3           EUR   1425.35   7.12675
        4           EUR   9247.51  46.23755
        5           EUR   1917.85   9.58925
        6           EUR  19531.69  97.65845

    .. include:: ../../docs/includes/input_columns.rst

    Args:
        trades (pandas.DataFrame): .. include:: ../../docs/includes/arg_trades.rst
        initial_portfolio (dict):  .. include:: ../../docs/includes/arg_initial_portfolio.rst
        initial_purchase_price (float): The purchase price of the initial_portfolio

    Returns:
        pandas.DataFrame: The DataFrame containing the information to be reported
        on form 2086 for each sale in the trades DataFrame.
    """

    check_trades(trades)
    trades = trades.copy()
    add_portfolio_purchase_price(trades, initial_purchase_price)
    sales = filter_sales_add_portfolio_value(trades, initial_portfolio)
    sales = sales[
        [
            "datetime",
            "trade_side",
            "cryptocurrency",
            "quantity",
            "amount",
            "fee",
            "portfolio_purchase_price",
            "portfolio_value",
        ]
    ]
    sales["portfolio_purchase_price_net"] = 0.0
    sales["purchase_price_fraction_sum"] = 0.0
    sales["purchase_price_fraction"] = 0.0
    compute_purchase_price_fraction(
        sales["amount"].values,
        sales["portfolio_value"].values,
        sales["portfolio_purchase_price"].values,
        sales["portfolio_purchase_price_net"].values,
        sales["purchase_price_fraction"].values,
        sales["purchase_price_fraction_sum"].values,
    )
    sales["amount_net"] = sales["amount"] - sales["fee"]
    sales["pnl"] = sales["amount_net"] - sales["purchase_price_fraction"]
    sales = sales[
        [
            "datetime",
            "trade_side",
            "cryptocurrency",
            "quantity",
            "amount",
            "fee",
            "amount_net",
            "portfolio_value",
            "portfolio_purchase_price",
            "purchase_price_fraction",
            "purchase_price_fraction_sum",
            "portfolio_purchase_price_net",
            "pnl",
        ]
    ]
    return sales


def compute_taxable_pnls(
    trades, year, initial_portfolio=None, initial_purchase_price=0.0
):
    """
    Computes your taxable PnL for each sale in the trades DataFrame

    In the french tax law (CGI art. 150 VH), taxable events are sales of
    crypto-currencies for official (fiat) currencies such as Euro. The PnL
    (profit and loss) arising from each sale must be reported in the form 2086
    (Formulaire n°2086).

    This function computes the PnL to be reported for each sale on form 2086, and
    other information that also needs to be reported on form 2086. It returns
    a DataFrame such as::

              Description Date de la cession [datetime]
        2  SELL 0.50 BTC           2020-09-05 16:50:00
        3  SELL 5.00 ETH           2020-09-08 12:40:00
        6  SELL 1.00 BTC           2020-12-21 09:30:00

           Valeur globale portefeuille [portfolio_value]  Prix de cession [amount]
        2                                      10226.900                   4361.35
        3                                       5679.970                   1425.35
        6                                      31934.785                  19531.69

           Frais de cession [fee]  Prix de cession net des frais [amount_net]
        2                21.80675                                  4339.54325
        3                 7.12675                                  1418.22325
        6                97.65845                                 19434.03155

          Prix total d'acquistion [portfolio_purchase_price]
        2                                         11286.4716
        3                                         11286.4716
        6                                         22507.6584

        Fractions de capital initial [purchase_price_fraction_sum]
        2                                           0.000000
        3                                        4813.213477
        6                                        6437.633759

        Prix total d'acquistion net [portfolio_purchase_price_net]
        2                                       11286.471600
        3                                        6473.258123
        6                                       16070.024641

           Plus-values et moins-values [pnl]
        2                        -473.670227
        3                        -206.197031
        6                        9605.415526

    You may copy directly the value of each cell (Date de la cession,
    Valeur globale portefeuille etc.) direcly in the form 2086
    (Formulaire n°2086). Internally, this

    The input trades DataFrame must have one line per trade, as follows::

                     datetime trade_side cryptocurrency  quantity     price
        0 2020-07-28 10:20:00        BUY            BTC       1.0   9262.42
        1 2020-09-01 12:20:00        BUY            ETH       5.0    393.58
        2 2020-09-05 16:50:00       SELL            BTC       0.5   8722.70
        3 2020-09-08 12:40:00       SELL            ETH       5.0    285.07
        4 2020-09-16 17:10:00        BUY            BTC       1.0   9247.51
        5 2020-11-07 15:40:00        BUY            ETH       5.0    383.57
        6 2020-12-21 09:30:00       SELL            BTC       1.0  19531.69

        base_currency    amount       fee
        0           EUR   9262.42  46.31210
        1           EUR   1967.90   9.83950
        2           EUR   4361.35  21.80675
        3           EUR   1425.35   7.12675
        4           EUR   9247.51  46.23755
        5           EUR   1917.85   9.58925
        6           EUR  19531.69  97.65845

    .. include:: ../../docs/includes/input_columns.rst

    Args:
        trades (pandas.DataFrame): .. include:: ../../docs/includes/arg_trades.rst
        year (int): The year to report your trades for. Usually, this is the
            last year.
        initial_portfolio (dict): .. include:: ../../docs/includes/arg_initial_portfolio.rst
        initial_purchase_price (float): The purchase price of the initial_portfolio

    Returns:
        (pandas.DataFrame, float): The DataFrame containing the information
        to be reported on form 2086 for each sale in the ``trades`` DataFrame,
        with the sum of the PnLs (Plus et moins values)
    """
    check_trades(trades)
    sales = compute_taxable_pnls_detailed(
        trades, initial_portfolio, initial_purchase_price
    )
    start_date = dt.datetime.combine(dt.date(year, 1, 1), dt.time.min)
    end_date = dt.datetime.combine(dt.date(year, 12, 31), dt.time.max)
    sales = sales[(sales["datetime"] >= start_date) & (sales["datetime"] <= end_date)]
    total_pnl = sales["pnl"].sum()
    sales["Description"] = sales["description"] = (
        sales["trade_side"]
        + " "
        + sales["quantity"].map("{:.2f}".format)
        + " "
        + sales["cryptocurrency"]
    )
    names = {
        "datetime": "Date de la cession [datetime]",
        "portfolio_value": "Valeur globale portefeuille [portfolio_value]",
        "amount": "Prix de cession [amount]",
        "fee": "Frais de cession [fee]",
        "amount_net": "Prix de cession net des frais [amount_net]",
        "portfolio_purchase_price": "Prix total d'acquistion [portfolio_purchase_price]",
        "purchase_price_fraction_sum": "Fractions de capital initial [purchase_price_fraction_sum]",
        "portfolio_purchase_price_net": "Prix total d'acquistion net [portfolio_purchase_price_net]",
        "pnl": "Plus-values et moins-values [pnl]",
    }
    columns = ["Description"] + list(names.keys())
    sales = sales[columns]
    sales = sales.rename(columns=names)
    return sales, total_pnl
