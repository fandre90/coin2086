import collections
import logging
import abc
import threading
import datetime as dt

import requests
import pandas as pd

logger = logging.getLogger(__name__)


TradingPair = collections.namedtuple("TradingPair", ["base", "quote"])


class PriceDownloader(abc.ABC):
    @abc.abstractmethod
    def download_price(self, crypto, dtime):
        pass

    @abc.abstractproperty
    def supported_crypto_list(self):
        pass


class CachedPriceDownloader(PriceDownloader):
    """Base class for crypto-currency price downloader classes.
    This class maintains a cache so that child classes can avoid
    hitting exchange or data providers  APIs too often
    """

    def __init__(self):
        self.cache = collections.defaultdict(dict)

    def _add_price_to_cache(self, crypto, dtime, price):
        crypto_cache = self.cache[crypto]
        crypto_cache[dtime] = price

    def find_price_in_cache(self, crypto, dtime):
        crypto_cache = self.cache[crypto]
        return crypto_cache.get(dtime)


def round_datetime(dtime, interval):
    return pd.to_datetime(dtime).round(interval).to_pydatetime()


FIAT_CURRENCIES = {"USD", "EUR", "CAD", "JPY", "GBP", "CHF", "AUD", "KRW"}


def is_fiat_currency(code):
    return code in FIAT_CURRENCIES


def bitstamp_download_supported_pairs():
    PAIRS_URL = "https://www.bitstamp.net/api/v2/trading-pairs-info/"
    resp = requests.get(PAIRS_URL)
    pairs = []
    for pinfo in resp.json():
        name = pinfo["name"]
        base, quote = name.split("/")
        pairs.append(TradingPair(base=base, quote=quote))
    return pairs


def bitstamp_download_minute_bins(crypto, dtime, limit=100):
    OHLC_URL = "https://www.bitstamp.net/api/v2/ohlc/{pair}/".format(
        pair=crypto.lower() + "eur"
    )
    parameters = {"start": int(dtime.timestamp()), "step": 60, "limit": limit}
    logger.info(f"Downloading prices from {OHLC_URL}, parameters: {parameters}")
    resp = requests.get(OHLC_URL, params=parameters)
    return resp.json()


class BitstampMinuteClosePriceDownloader(CachedPriceDownloader):
    TIME_INTERVAL = "min"

    def __init__(self):
        super().__init__()
        self._supported_crypto_list = self._download_supported_crypto_list()

    @property
    def supported_crypto_list(self):
        return self._supported_crypto_list

    @staticmethod
    def _download_supported_crypto_list():
        pairs = bitstamp_download_supported_pairs()
        return sorted(
            [p.base for p in pairs if p.quote == "EUR" and not is_fiat_currency(p.base)]
        )

    def download_price(self, crypto, dtime):
        dtime = round_datetime(dtime, self.TIME_INTERVAL)
        cached_price = self.find_price_in_cache(crypto, dtime)
        if cached_price is None:
            self._download_price_add_to_cache(crypto, dtime)
        cached_price = self.find_price_in_cache(crypto, dtime)
        if cached_price is None:
            raise RuntimeError(f"Could not download price for {crypto} at {dtime}")
        return cached_price

    def _download_price_add_to_cache(self, crypto, dtime):
        resp = bitstamp_download_minute_bins(crypto, dtime)
        assert resp["data"]["pair"] == crypto.upper() + "/EUR"
        bins = resp["data"]["ohlc"]
        for b in bins:
            dtime = dt.datetime.fromtimestamp(int(b["timestamp"]))
            rounded = round_datetime(dtime, self.TIME_INTERVAL)
            if not rounded == dtime:
                raise ValueError(
                    f"Bitstamp API returned a bin time that "
                    "is not rounded to {self.time_interval}: {dtime}"
                )
            self._add_price_to_cache(crypto, dtime, float(b["close"]))


KRAKEN_TO_USUAL_CODEBOOK = {
    "XDAO": "DAO",
    "XETC": "ETC",
    "XETH": "ETH",
    "XICN": "ICN",
    "XLTC": "LTC",
    "XMLN": "MLN",
    "XNMC": "NMC",
    "XREP": "REP",
    "XREPV2": "REPV2",
    "XXBT": "BTC",
    "XBT": "BTC",
    "XXDG": "DOGE",
    "XDG": "DOGE",
    "XXLM": "XLM",
    "XXMR": "XMR",
    "XXRP": "XRP",
    "XXTZ": "XTZ",
    "XXVN": "XVN",
    "XZEC": "ZEC",
    "ZAUD": "AUD",
    "ZCAD": "CAD",
    "ZCHF": "CHF",
    "ZEUR": "EUR",
    "ZGBP": "GBP",
    "ZJPY": "JPY",
    "ZKRW": "KRW",
    "ZUSD": "USD",
}


USUAL_TO_KRAKEN_CODEBOOK = {v: k for k, v in KRAKEN_TO_USUAL_CODEBOOK.items()}


def convert_ususal_to_kraken_code(code):
    return USUAL_TO_KRAKEN_CODEBOOK.get(code, code)


def convert_kraken_to_usual_code(code):
    return KRAKEN_TO_USUAL_CODEBOOK.get(code, code)


def kraken_download_supported_pairs():
    PAIRS_URL = "https://api.kraken.com/0/public/AssetPairs"
    resp = requests.get(PAIRS_URL)
    pairs = []
    result = resp.json()["result"]
    for _, pinfo in result.items():
        base = convert_kraken_to_usual_code(pinfo["base"])
        quote = convert_kraken_to_usual_code(pinfo["quote"])
        pairs.append(TradingPair(base=base, quote=quote))
    return list(set(pairs))


def kraken_download_next_trade_price(crypto, dtime):
    TRADES_URL = "https://api.kraken.com/0/public/Trades"
    pair = crypto + "EUR"
    since = int(dtime.timestamp())
    params = {"pair": pair, "since": since}
    logger.info(f"Downloading prices from {TRADES_URL}, parameters: {params}")
    resp = requests.get(TRADES_URL, params=params)
    result = resp.json()["result"]
    trades = list(result.items())[0][1]
    next_trade = trades[0]
    price = next_trade[0]
    return float(price)


class KrakenNextTradePriceDownloader(CachedPriceDownloader):
    def __init__(self):
        super().__init__()
        self._supported_crypto_list = self._download_supported_crypto_list()

    @property
    def supported_crypto_list(self):
        return self._supported_crypto_list

    @staticmethod
    def _download_supported_crypto_list():
        pairs = kraken_download_supported_pairs()
        return sorted(
            [p.base for p in pairs if p.quote == "EUR" and not is_fiat_currency(p.base)]
        )

    def download_price(self, crypto, dtime):
        cached_price = self.find_price_in_cache(crypto, dtime)
        if cached_price is None:
            self._download_price_add_to_cache(crypto, dtime)
        cached_price = self.find_price_in_cache(crypto, dtime)
        if cached_price is None:
            raise RuntimeError(f"Could not download price for {crypto} at {dtime}")
        return cached_price

    def _download_price_add_to_cache(self, crypto, dtime):
        price = kraken_download_next_trade_price(crypto, dtime)
        self._add_price_to_cache(crypto, dtime, price)


class MultiSourceFirstPriceDownloader(PriceDownloader):
    def __init__(self, price_downloaders):
        self.price_downloaders = price_downloaders
        self._supported_crypto_list = self._make_supported_crypto_list()

    @property
    def supported_crypto_list(self):
        return self._supported_crypto_list

    def _make_supported_crypto_list(self):
        supported_cryptos = set()
        for source in self.price_downloaders:
            source_pairs = source.supported_crypto_list
            print(source_pairs)
            supported_cryptos.update(source_pairs)
        return sorted(list(supported_cryptos))

    def download_price(self, crypto, dtime):
        for source in self.price_downloaders:
            if crypto in source.supported_crypto_list:
                try:
                    price = source.download_price(crypto, dtime)
                    return price
                except:
                    pass
        raise RuntimeError(f"Could not download price for {crypto} at {dtime}")


__price_downloader = threading.local()


def reference_price_downloader():
    price_downloader = None
    try:
        price_downloader = __price_downloader.instance
    except AttributeError:
        __price_downloader.instance = instantiate_reference_price_downloader()
        price_downloader = __price_downloader.instance
    return price_downloader


def instantiate_reference_price_downloader():
    bstamp = BitstampMinuteClosePriceDownloader()
    kraken = KrakenNextTradePriceDownloader()
    multi = MultiSourceFirstPriceDownloader([bstamp, kraken])
    return multi
