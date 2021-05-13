Basic usage
===========

Coin2086 takes as input a pandas DataFrame of all your crypto-currency trades
(purchase and sales), as illustrated below. You will be able to download an
history of your trades from the exchange you usage. Your may have to rework
the column names so that the DataFrame follows the :ref:`Input Format`
expected by coin2086.

.. code-block:: python

   import pandas as pd
   trades = pd.read_csv('trades.csv')
   trades

.. thumbnail:: ../examples/interlead_multiyear_trades.png

You may then use coin2086 to generate all the information you need to
report on form 2086:

.. code-block:: python

   import coin2086
   form2086, taxable_profit = coin2086.compute_taxable_pnls(trades, 2020)
   form2086

.. thumbnail:: ../examples/interlead_multiyear_2020_pnl.png

The above DataFrame containes the exact infor,at. The variable `taxable_profit` holds the sum of your profit and losses of the year, this will your taxable basis. The meaning of the columns is as follows:

* *Date de la cession* (Sale date): The date at which your sale occured
*  *Valeur globale du protefeuile* (Total portfolio value): The total value of your crypto-currency portfolio at the moment your sale occured
* *Prix de cession* (Amount received from the sale): The amount of money your received from the sale, **gross of fees**.
* *Frais de cession* (Fees paid for the sale): The amount of money you paid to the broker or exchange to sell your crypto-currency.
* *Prix total d'acquisition* (Portfolio purchase price): The *total* amount of money you spent to purchase your crypto-currencies
* *Fractions de capital initial*: Fraction of the portfolio purchase price that were sold
* *Prix total d'acquisition net* (Net purchase price): This the *Prix total d'acquisition* minus the *Fractions de capital initial*
* *Plus et moins values* (Profit and losses) The profit and losses you will be taxed on. This is *Prix de cession* minus *Prix total d'acquisition net*.

You can direcly copy the information in the corresponding
cells of form 2086:

.. thumbnail:: ../examples/form2086_excerpt.png