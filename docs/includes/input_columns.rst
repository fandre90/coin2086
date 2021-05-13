.. warning::
    The ``trades`` must be sorted by increasing datetime, this can be achieved
    as follows ``trades.sort_values('datetime').reset_index(drop=True)``.

The columns must follow the following specification:

datetime
    The date and time of your trades **in the UTC timezone**. If the time
    is not in the UTC timezone, the computed valuation of your portfolio
    will be wrong.
trade_side
    The side of your trade, either BUY or SELL (uppercase)
cryptocurrency
    The crypto-currency you bought or sold
quantity
    The quantity of crypto-currency you bought or sold
price
    The price at which you bought or sold the crypto-currency
base_currency
    The base currency you bought or sold the crypto-currency for.
    For now, it must be EUR (uppercase)
amount
    The amount of base_currency you received or spent, respectively for selling
    or buying a crypto-currency.
fee
    The exchange fee for the trade. Must be expressed in base_currency.
