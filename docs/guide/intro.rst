Introduction
============

What is coin2086 ?
------------------

The purpose of coin2086 is to help French tax residents to fill their
crypto-currency tax returns (`Formulaire n°2086 <https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques>`_).

The French tax law,
(`CGI art. 150 VH bis <https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038612228/2019-05-24>`_) requires tax residents to report their profit and losses (PnL) arising from
each of their crypto-currency sale. Each sale should be reported on `Formulaire n°2086 <https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques>`_,
or in the web version of this form.

The formula to compute your profit and losses, detailed on `Formulaire n°2086 <https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques>`_, requires you to valuate your whole crypto-currency portfolio every time you sell, and keep track of the amount of initial investment capital that was sold. This accounting is tedious to do by hand.

Coin2086 does all of that automatically for you. It takes your trades as input, valuates your cryptocurrency portfolio, computes your taxable profit and outputs the exact information you need to fill on Formulaire n°2086.

See :ref:`Installation` and :ref:`Basic usage` to get started.

Limitations
-----------

* Coin2086 only supports purchases of crypto-currency for Euros, and sales of
  crypto-currency for Euros. **Trades in dollar are not supported, and**
  **crypto-crypto (e.g. ETHBTC or DOGEBTC) trades are not supported**
* The supported crypto-currencies are: AAVE, BAT, BCH, BTC, ETH, KNC, LINK, LTC,
  MKR, OMG, PAX, SNX, UMA, UNI, USDC, XLM, XRP, YFI, ZRX, ADA, ALGO, ANT, ATOM,
  BAL, COMP, CRV, DAI, DASH, DOGE, DOT, EOS, ETC, EWT, FIL, FLOW, GNO, GRT, ICX,
  KAVA, KEEP, KSM, LSK, MANA, MLN, NANO, OCEAN, OXT, PAXG, QTUM, REP, REPV2, SC,
  STORJ, TBTC, TRX, USDT, WAVES, XMR, XTZ, ZEC
* Short sales are not supported
