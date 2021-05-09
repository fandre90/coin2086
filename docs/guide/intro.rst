Introduction
============

What is coin2086 ?
------------------

The purpose of coin2086 is to help French tax residents to fill their 
crypto-currency tax returns (`Formulaire n°2086 <https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques>`_).

According to the French tax law, every sale of crypto-currency is a taxable event
(`CGI art. 150 VH bis <https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038612228/2019-05-24>`_).
Each sale should be reported on form 2086 (`Formulaire n°2086 <https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques>`_),
or in the web version of this form.

Form 2086 requires that you provide the following information for each sale:

* *Date de la cession* (Sale date): The date at which your sale occured
*  *Valeur globale du protefeuile* (Total portfolio value): The total value of your crypto-currency portfolio at the moment your sale occured
* *Prix de cession* (Amount received from the sale): The amount of money your received from the sale, **gross of fees**.
* *Frais de cession* (Fees paid for the sale): The amount of money you paid to the broker or exchange to sell your crypto-currency.
* *Prix total d'acquisition* (Portfolio purchase price): The *total* amount of money you spent to purchase your crypto-currencies
* *Fractions de capital initial*: Fraction of the portfolio purchase price that were sold
* *Prix total d'acquisition net* (Net purchase price): This the *Prix total d'acquisition* minus the *Fractions de capital initial*
* *Plus et moins values* (Profit and losses) The profit and losses you will be taxed on. This is *Prix de cession* minus *Prix total d'acquisition net*.

The sum of *Plus et moins values* of all your crypto-currency sales in the last 
tax year is your taxable base. The tax rate is currently 30%.

**The coin2086 python module takes care of all these complex caculations. It
provides you with all these values for each sale that occured in a given
tax year, your will just need to copy them into the Formulaire n°2086**

Limitations
-----------

* Coin2086 only supports purchases of crypto-currency for Euros, and sales of
  crypto-currency for Euros. **Trades in dollar are not supported, and**
  **crypto-crypto (e.g. ETHBTC or DOGEBTC) trades are not supported**
* The supported crypto-currencies are: AAVE, BAT, BCH, BTC, ETH, KNC, LINK, 
  LTC, MKR, OMG, PAX, SDC, SNX, UMA, UNI, XLM, XRP, YFI, ZRX
