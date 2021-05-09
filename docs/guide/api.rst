API Introduction
================

The main entry point of coin2086 is :py:func:`coin2086.compute_taxable_pnls`
that returns a DataFrame with all your sales for a given tax year, and the
information your need to report on form 2086 (see :ref:`Basic usage`).

Internally, this function uses :py:func:`coin2086.compute_taxable_pnls_detailed`
and simply remaps the symbolic column names to their French equivalent. You
may inspect the output of :py:func:`coin2086.compute_taxable_pnls_detailed`:

.. code-block:: python

    import coin2086
    sales = coin2086.compute_taxable_pnls_detailed(trades)
    sales

.. thumbnail:: ../examples/interlead_multiyear_pnl_detailed.png

To determine you PnL :py:func:`coin2086.compute_taxable_pnls_detailed` needs to
compute the valuation of your portfolio before each sale. This is done by 
calling the Bitstamp public API to obtain the publicly known prices of the 
crypto-currencies you held at the moment of the sale. The function 
:py:func:`coin2086.valuate_portfolio` takes care of valuating your portfolio
before each sale:

.. code-block:: python

    import coin2086
    sales = coin2086.valuate_portfolio(trades)
    sales

.. thumbnail:: ../examples/interlead_multiyear_valuation.png