Input Format
============

Trades DataFrame
----------------
Coin2086 functions take as input a pandas DataFrame of all your crypto-currency
trades (purchase and sales). You should be able to download the history of your
trades from your user porfile on the exchange you use (Bistamp, Coinbase,
Kraken etc.), however, you will need to adapt it so that it follows the format
expected by coin2086.

.. thumbnail:: ../examples/interlead_multiyear_trades.png

.. include:: ../includes/input_columns.rst

.. warning::
    **It is critically important that the trades DataFrame contains all of
    your crypto-currency trades** since your bought your very crypto-currency,
    not just the trades for the last tax year.

    In other words, before the first trade in the trades DataFrame, you should have
    been holding no crypto-currency. This is important to determine your
    portfolio purchase price, which is used in the computation of your profit
    and losses. If this is  not possible, you will have to use the
    ``initial_porfolio`` argument.

Trades Normalization
--------------------
Coin2086 provides helpers to help your normalize transaction histories downloaded
from exchanges into the Trades DataFrame format expected by coin2086. Currently
a trade normalisation function is provided for Bitstamp only, see
:py:func:`coin2086.bitstamp.normalize_bitstamp_transactions`.

If you write your own trade normalization function for another exchange,
please submit a pull request.

Initial Portfolio
-----------------

Your initial portfolio is simply the composition of your crypto-currency
portfolio *before* the first trade in the trades DataFrame. Coin2086 will
also need the purchase price for this portfolio.

For instance, suppose you have bought one Bitcoin and one Ethereum in 2017
(but you have lost the trades) for 2400 euros and 290 euros
respectively. Your intial portfolio is as follows:

.. code-block:: python

    import coin2086
    # trades is the DataFrame above
    initial_porfolio = {'BTC': 1.0, 'ETH': 1.0}
    initial_purchase_price = 2400 + 290
    sales, total_pnl = coin2086.compute_taxable_pnls(
        trades, 2020, initial_porfolio=initial_porfolio,
        initial_purchase_price=initial_purchase_price)
    sales

.. thumbnail:: ../examples/interlead_multiyear_2020_pnl_initial.png

Notice that, in this case, :py:func:`coin2086.compute_taxable_pnls` produces
very different results if you forget your intial portfolio

.. code-block:: python

    import coin2086
    sales, total_pnl = coin2086.compute_taxable_pnls(trades, 2020)
    sales

.. thumbnail:: ../examples/interlead_multiyear_2020_pnl.png