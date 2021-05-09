# Coin2086: French Crypto Tax Return for Humans #

Coin2086 is as Python module that helps French tax residents to fill their
crypto-currency tax return ([Formulaire n°2086](https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques)).

French tax authorities requires tax residents to provide a lot of information
for each crypto-currency sale they performed during the last tax year.
Coin2086 simply takes your trades as input, and returns a DataFrame with all
the information you need to report on [Formulaire n°2086](https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques).

It's that easy !

[Documentation on Read The Docs](https://coin2086.readthedocs.io)

## Installation ##

```sh
pip install coin2086
```

## Basic Usage ##

```python
    import pandas as pd
    import coin2086
    trades = pd.read_csv('trades.csv')
    form2086, tax_base = coin2086.compute_taxable_pnls(trades, 2020)
    expected_tax = 0.3 * tax_base
    print(f"Taxable base for 2020 crypto-currency sales: {tax_base:.2f}")
    print(f"Expected tax amount: {expected_tax:.2f}")
    print("Information that needs to be reported on Formulaire n°2086")
    print(form2086)
```
