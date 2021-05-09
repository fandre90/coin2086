Basic usage
===========

Coin2086 takes as input a pandas DataFrame of all your crypto-currency trades
(purchase and sales), as illustrated below:

.. code-block:: python

   import pandas as pd
   trades = pd.read_csv('trades.csv')
   trades

.. thumbnail:: ../examples/interlead_multiyear_trades.png

This DataFrame should follow the :ref:`Input Format`

You may then simply use coin2086 to generate all the information you need to
report on form 2086

.. code-block:: python

   import coin2086
   sales, total_pnl = coin2086.compute_taxable_pnls(trades, 2020)
   sales

.. thumbnail:: ../examples/interlead_multiyear_2020_pnl.png

The columns of the above DataFrame can directly be copied in the corresponding
cells of form 2086.

.. thumbnail:: ../examples/form2086_excerpt.png