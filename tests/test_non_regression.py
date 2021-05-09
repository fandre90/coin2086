import pathlib

import pytest
import pandas as pd

import coin2086


def make_ref_path(trades_fname, wanted_suffix):
    ref_dir = pathlib.Path(__file__).parent.absolute() / "reference_data"
    trades_path = ref_dir / trades_fname
    stem = trades_path.stem
    return ref_dir / (stem + wanted_suffix)


def make_reference_data_paths(trades_fname):
    trades_path = make_ref_path(trades_fname, ".csv")
    valuation_path = make_ref_path(trades_fname, "_valuation.csv")
    pnl_path = make_ref_path(trades_fname, "_detailed_pnl.csv")
    return trades_path, valuation_path, pnl_path


def load_trades(csv_path):
    trades = pd.read_csv(csv_path, index_col=0)
    trades["datetime"] = pd.to_datetime(trades["datetime"])
    return trades


def update_reference_dataframes(trades_fname):
    trades_path, valuation_path, pnl_path = make_reference_data_paths(trades_fname)
    trades = load_trades(trades_path)
    valuation = coin2086.valuate_portfolio(trades)
    pnl = coin2086.compute_taxable_pnls_detailed(trades)
    valuation.to_csv(valuation_path)
    pnl.to_csv(pnl_path)


def load_reference_dataframes(trades_fname):
    trades_path, valuation_path, pnl_path = make_reference_data_paths(trades_fname)
    trades = load_trades(trades_path)
    valuation = pd.read_csv(valuation_path, header=[0, 1], index_col=0)
    pnl = pd.read_csv(pnl_path, index_col=0)
    pnl["datetime"] = pd.to_datetime(pnl["datetime"])
    return trades, valuation, pnl


@pytest.mark.parametrize(
    "trades_fname",
    [
        "real_world.csv",
        "form_2086_notice.csv",
        "interleaved_trades.csv",
        "interleaved_multiyear_trades.csv",
    ],
)
def test_trades_against_reference(trades_fname):
    trades, valuation_ref, pnl_ref = load_reference_dataframes(trades_fname)
    valuation = coin2086.valuate_portfolio(trades)
    pnl = coin2086.compute_taxable_pnls_detailed(trades)
    pd.testing.assert_frame_equal(valuation, valuation_ref)
    pd.testing.assert_frame_equal(pnl, pnl_ref)


def test_compute_pnl():
    trades = load_trades(make_ref_path("interleaved_multiyear_trades.csv", ".csv"))
    pnl_declare_path = make_ref_path(
        "interleaved_multiyear_trades.csv", "_2020_pnl.csv"
    )
    pnl_declare_ref = pd.read_csv(pnl_declare_path, index_col=0)
    # Convert 2nd columns (Date de la cession to datetime64s)
    pnl_declare_ref.iloc[:, 1] = pd.to_datetime(pnl_declare_ref.iloc[:, 1])
    pnl_declare, total_pnl = coin2086.compute_taxable_pnls(trades, 2020)
    print(pnl_declare)
    pd.testing.assert_frame_equal(pnl_declare, pnl_declare_ref)
