# Coin2086 #

> Crypto Taxes Made Easy ! 📒

[![PyPI Version][pypi-image]][pypi-url]
[![PyPI Python Version][pypi-version-image]][pypi-url]
[![PyPI License][pypi-license-image]][pypi-url]
[![Documentation Status][rtd-image]](https://coin2086.readthedocs.io/en/latest/?badge=latest)
[![Binder][binder-img]][binder-url]

Coin2086 is a Python module that makes it easy for French tax residents to
fill their crypto-currency tax return.

Tax autorities requires French tax residents to report their profit and losses
(PnL) on each of their cryto-currency sales of the previous year on
[Formulaire n°2086][form2086-url].

The formula to compute your profit and losses, detailed on [Formulaire n°2086][form2086-url],
requires you to valuate your *whole* crypto-currency portfolio every time you sell,
and keep track of the amount of initial investment capital that was sold. This
accounting is tedious to do by hand.

Coin2086 does all of that automatically for you. It takes your trades as input,
valuates your cryptocurrency portfolio, computes your taxable profit and outputs
the *exact* information you need to fill on [Formulaire n°2086][form2086-url].

It's that simple !

📖  Documentation: https://coin2086.readthedocs.io/  
📦  PyPI Package: https://pypi.org/project/coin2086/  
📝  Example Jupyter Notebook: [Launch on Binder][binder-url]  
💻  GitHub Project: https://github.com/fandre90/coin2086  

[form2086-url]: https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques
[binder-img]: https://mybinder.org/badge_logo.svg
[binder-url]: https://mybinder.org/v2/gh/fandre90/coin2086/HEAD?filepath=notebooks%2FCoin2086%20Example%20Use.ipynb
[pypi-image]: https://img.shields.io/pypi/v/coin2086
[pypi-version-image]: https://img.shields.io/pypi/pyversions/coin2086
[pypi-license-image]: https://img.shields.io/pypi/l/coin2086
[pypi-url]: https://pypi.org/project/coin2086/
[rtd-image]: https://readthedocs.org/projects/coin2086/badge/?version=latest

## Installation ##

```sh
pip install coin2086
```

Alternatively, you may use the [Binder Notebook][binder-url] directly in your browser

## Basic Usage ##

```python
>>> import pandas as pd
>>> import coin2086
>>> trades = pd.read_csv('trades.csv')
>>> trades
             datetime trade_side cryptocurrency  quantity     price base_currency      amount        fee
0 2019-10-19 11:10:00        BUY            BTC      1.00   7149.38           EUR   7149.3800  35.746900
1 2019-11-14 19:50:00       SELL            BTC      0.50   7844.88           EUR   3922.4400  19.612200
2 2020-07-28 10:20:00        BUY            BTC      2.00   9262.42           EUR  18524.8400  92.624200
3 2020-09-01 12:20:00        BUY            ETH      5.00    393.58           EUR   1967.9000   9.839500
4 2020-09-05 16:50:00       SELL            BTC      1.00   8722.70           EUR   8722.7000  43.613500
5 2020-09-08 12:40:00       SELL            ETH      5.00    285.07           EUR   1425.3500   7.126750
6 2020-12-20 09:10:00       SELL            BTC      0.25  19223.90           EUR   4805.9750  24.029875
7 2021-03-13 23:40:00       SELL            BTC      0.25  50025.17           EUR  12506.2925  62.531463

>>> year = 2020
>>> form2086, taxable_profit = coin2086.compute_taxable_pnls(trades, year=year)
>>> print(f"Total taxable profit for year {year}: {taxable_profit:.2f} euros")
Total taxable profit for year 2020: 2038.50 euros
>>> form2086
     Description  ... Plus-values et moins-values [pnl]
4  SELL 1.00 BTC  ...                       -371.708792
5  SELL 5.00 ETH  ...                       -102.332358
6  SELL 0.25 BTC  ...                       2512.542417

[3 rows x 10 columns]
```

For more information, check out the 
[documentation](https://coin2086.readthedocs.io/) or the
[example notebook][binder-url]
