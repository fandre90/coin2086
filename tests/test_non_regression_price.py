import pathlib
import datetime as dt
import pandas as pd

from coin2086.validation import SUPPORTED_CRYPTOS
from coin2086.pricedownload import reference_price_downloader


def make_ref_path(dtime, wanted_suffix):
    strtime = str(dtime).replace(" ", "T").replace(":", "")
    ref_dir = pathlib.Path(__file__).parent.absolute() / "reference_data_price"
    trades_path = ref_dir / strtime
    stem = trades_path.stem
    return ref_dir / (stem + wanted_suffix)


def load_reference_dataframe(dtime):
    path = make_ref_path(dtime, "_prices.csv")
    return pd.read_csv(path)


def price_all_supported_cryptos(dtime):
    data = []
    price_downloader = reference_price_downloader()
    for crypto in SUPPORTED_CRYPTOS:
        price = price_downloader.download_price(crypto, dtime)
        data.append([crypto, price])
    prices = pd.DataFrame(data, columns=["cryptocurrency", "price"])
    return prices.sort_values("cryptocurrency").reset_index(drop=True)


def update_reference_dataframe(dtime):
    path = make_ref_path(dtime, "_prices.csv")
    prices = price_all_supported_cryptos(dtime)
    prices.to_csv(path, index=False)


TEST_DTIME = dt.datetime(2021, 5, 12, 11, 32, 54)


def test_reference_price_downloader():
    prices = price_all_supported_cryptos(TEST_DTIME)
    prices_ref = load_reference_dataframe(TEST_DTIME)
    pd.testing.assert_frame_equal(prices, prices_ref)
