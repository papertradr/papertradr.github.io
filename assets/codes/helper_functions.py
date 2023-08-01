import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import norm
from py_vollib.black_scholes_merton.implied_volatility import implied_volatility
import pandas as pd
from datetime import datetime

from IPython.display import HTML, display

from typing import List, Dict, Tuple, Optional, Union

from scipy.interpolate import griddata
from src.db.clickhouse_db import ClickHouseDB

import plotly.graph_objects as go


# global variables
port=28123
database="test"


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y%m%d")
    d2 = datetime.strptime(d2, "%Y%m%d")
    return abs((d2-d1).days)


def common_where_clause(_date_str: str, _beg_time: str, _end_time: str, tz: str):
    return f"""
        toDate(system_datetime, '{tz}')='{_date_str}' 
        AND
        toTime(system_datetime, '{tz}') BETWEEN
            toTime(parseDateTimeBestEffort('{_beg_time}', '{tz}'), '{tz}') 
            AND
            toTime(parseDateTimeBestEffort('{_end_time}', '{tz}'), '{tz}')
    """


def is_trading_date(date_str: str) -> bool:
    client = ClickHouseDB(host="localhost", port=port, database=database)
    check = client.read_sql(
        f"""
        SELECT toDate(system_datetime, 'Asia/Seoul') AS date FROM default.KrxStockBatchData
        WHERE date='{date_str}'
        LIMIT 1
        """
    )
    if check.empty:
        return False

    return True


def stock_batchdata_columns(tz):
    return [
        "isin",
        "prev_day_closing_price",
        "main_board_unit_volume",
        "abbreviated_issue_name_in_en",
        "abbreviated_issue_code",
        "listed_shares_number",
        "listed_shares_number * prev_day_closing_price AS market_capitalization",
        f"toDate(system_datetime, '{tz}') as date",
    ]



def marketdepth_columns(date_str, tz: str): 
    return [
        "isin",
        "l1askprice",
        "l1asksize",
        "l1bidprice",
        "l1bidsize",
        "(l1askprice + l1bidprice) / 2 AS midprice",  
        """(l1askprice * l1bidsize + l1bidprice * l1asksize) / (l1asksize + l1bidsize) 
            AS weighted_midprice""",
        f"toDate(system_datetime, '{tz}') as date",
        f"toTimeZone(system_datetime, '{tz}') as system_datetime",
    ]



class StockBatchData():
    def __init__(
            self, 
            isins: List[str], 
            date_str: str, 
            tz: str = "Asia/Seoul",
            debug: bool = False):
        self.isins = isins
        self.date_str = date_str
        self.client = ClickHouseDB(host="localhost", port=port, database=database)
        
        self.df = self.client.read_sql(
            f"""
            SELECT DISTINCT ON (isin) 
                {','.join(stock_batchdata_columns(tz))}
            FROM default.KrxStockBatchData
            WHERE date='{date_str}'
            AND isin IN ({",".join([f"'{isin}'" for isin in self.isins])})
            """
        )


class FuturesBatchData():
    def __init__(
            self, 
            isins: List[str], 
            date_str: str, 
            tz: str = "Asia/Seoul",
            debug: bool = False):
        self.isins = isins
        self.date_str, self.tz, self.debug = date_str, tz, debug
        self.client = ClickHouseDB(host="localhost", port=port, database=database)
        
        self.df = self.client.read_sql(
            f"""
            SELECT DISTINCT ON (isin) 
                isin
                , base_price
                , previous_day_closing_price
                , toDate(system_datetime, '{tz}') as date
            FROM default.KrxDerivativeBatchData
            WHERE 
                date='{date_str}'
                AND isin IN ({",".join([f"'{isin}'" for isin in self.isins])})
            """
        )


class EtfIntradayNav():
    def __init__(
        self,
        etf_isin: str,
        date_str: str,
        tz: str = "Asia/Seoul"):
        self.etf_isin, self.date_str, self.tz = etf_isin, date_str, tz
        self.client = ClickHouseDB(host="localhost", port=port, database=database)
        self.df = self.client.read_sql(
            f"""
            SELECT
                isin
                , previous_day_nav / 100 as prev_day_nav
                , intraday_final_nav / 100 as intraday_final_nav
                , toTimeZone(system_datetime, '{tz}') as system_datetime
            FROM default.KrxETFNAV
            WHERE isin='{etf_isin}'
            AND toDate(system_datetime, 'Asia/Seoul')='{date_str}'
            ORDER BY system_datetime ASC
            """
        )
        self.prev_day_nav = self.df['prev_day_nav'][0]
        self._iter_idx = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        self._iter_idx += 1
        if self._iter_idx >= len(self.df):
            raise StopIteration
        return self.df.iloc[self._iter_idx]



class EtfPdf():
    def __init__(
            self, 
            etf_isin: str, 
            date_str: str,
            etf_cu: int,
            tz: str="Asia/Seoul"):
        # get components
        self.etf_isin, self.date_str, self.tz = etf_isin, date_str, tz
        self.etf_cu = etf_cu
        self.client = ClickHouseDB(host="localhost", port=port, database=database)

        self.df = self.client.read_sql(
            f"""
            SELECT DISTINCT ON (component_isin)
                component_isin
                , securities_per_1_cu_or_contract_units_or_korean_won_cash
                , par_value_or_initial_cash_amount
                , valuation_amount
                , toTimeZone(system_datetime, '{tz}') as system_datetime
            FROM default.KrxETFPDF
            WHERE isin='{etf_isin}' AND toDate(system_datetime, 'Asia/Seoul')='{date_str}'
            ORDER BY component_isin
            """
        )
        assert not self.df.empty, f"component df is empty"
        print(np.sum(self.df["valuation_amount"])/ 50000)

        self.component_isins = list(self.df["component_isin"].to_numpy())

        self.df = self.client.read_sql(
            f"""
            WITH pdf as (SELECT DISTINCT ON (component_isin)
                component_isin
                , securities_per_1_cu_or_contract_units_or_korean_won_cash
                , par_value_or_initial_cash_amount
                , valuation_amount
                , toTimeZone(system_datetime, '{tz}') as system_datetime
            FROM default.KrxETFPDF
            WHERE isin='{etf_isin}' AND toDate(system_datetime, 'Asia/Seoul')='{date_str}'
            ORDER BY component_isin)
            , batchdata as (SELECT DISTINCT ON (isin) 
                {','.join(stock_batchdata_columns(tz))}
            FROM default.KrxStockBatchData
            WHERE date='{date_str}'
            AND isin IN ({",".join([f"'{isin}'" for isin in self.component_isins])}))
            SELECT
                pdf.component_isin AS isin
                , IF(isin='KRD010010001',
                     'CASH',
                     batchdata.abbreviated_issue_name_in_en)
                    as abbreviated_issue_name_in_en
                , batchdata.abbreviated_issue_code
                , batchdata.prev_day_closing_price
                , pdf.securities_per_1_cu_or_contract_units_or_korean_won_cash
                , pdf.par_value_or_initial_cash_amount
                , pdf.valuation_amount
                , IF(isin='KRD010010001', 
                    valuation_amount,
                    pdf.securities_per_1_cu_or_contract_units_or_korean_won_cash
                    * prev_day_closing_price / 100)
                      as calculated_valuation_amount
                , pdf.system_datetime
            FROM pdf 
            LEFT JOIN batchdata
            ON pdf.component_isin=batchdata.isin
            ORDER BY component_isin
            """
        )

        self.pdf_state = {}
        for row in self.df.itertuples():
            self.pdf_state[row.isin] = {
                "price": row.prev_day_closing_price,
                "quantity": row.securities_per_1_cu_or_contract_units_or_korean_won_cash, 
                "valuation_amount": row.valuation_amount,
                "system_datetime": row.system_datetime
            }
            self.updated_datetime = row.system_datetime
        
        self.update_nav()
        self.koscom_nav = self.nav 


    def update_state(self, isin, price, koscom_nav, system_datetime):
        self.pdf_state[isin]["price"] = price
        self.pdf_state[isin]["valuation_amount"] = self.pdf_state[isin]["quantity"] * price / 100
        self.pdf_state[isin]["system_datetime"] = system_datetime
        self.updated_datetime = system_datetime
        self.koscom_nav = koscom_nav
        self.update_nav() 


    def update_nav(self):
        nav = 0
        for _, data in self.pdf_state.items():
            nav += data["valuation_amount"]
        self.nav = nav / self.etf_cu        


class MarketdepthWithNavData():
    def __init__(
            self, 
            isins: List[str], 
            etf_isin: str,
            date_str: str, 
            beg_time: str, 
            end_time: str,
            tz: str = "Asia/Seoul",):
        self.isins = isins
        self.date_str = date_str
        self.etf_isin = etf_isin
        self.client = ClickHouseDB(host="localhost", port=port, database=database)

        self.stock_marketdepth_df = self.client.read_sql(
            f"""
            WITH stock_marketdepth AS (
                SELECT 
                    {','.join(marketdepth_columns(date_str, tz))}
                    , '{etf_isin}' as etf_isin
                FROM default.KrxStockMarketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.isins])})
                ORDER BY system_datetime
            )
            , nav AS (
                SELECT
                    isin
                    , previous_day_nav / 100 as prev_day_nav
                    , intraday_final_nav / 100 as intraday_final_nav
                    , toTimeZone(system_datetime, '{tz}') as system_datetime
                FROM default.KrxETFNAV
                WHERE isin='{etf_isin}'
                AND toDate(system_datetime, 'Asia/Seoul')='{date_str}'
                ORDER BY system_datetime ASC
            )
            SELECT 
                stock_marketdepth.*
                , nav.prev_day_nav
                , nav.intraday_final_nav
            FROM stock_marketdepth
            ASOF LEFT JOIN nav
            ON stock_marketdepth.etf_isin = nav.isin
            AND stock_marketdepth.system_datetime >= nav.system_datetime
            ORDER BY system_datetime 
            """
        )
        # order by system_datetime
        self.stock_marketdepth_df = self.stock_marketdepth_df.sort_values(by=["system_datetime"])

        self._iter_idx = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        self._iter_idx += 1
        if self._iter_idx >= len(self.stock_marketdepth_df):
            raise StopIteration
        return self.stock_marketdepth_df.iloc[self._iter_idx]



class MarketdepthData():
    def __init__(
            self, 
            isins: List[str], 
            date_str: str, 
            beg_time: str, 
            end_time: str,
            tz: str = "Asia/Seoul",):
        self.isins = isins
        self.date_str = date_str
        self.client = ClickHouseDB(host="localhost", port=port, database=database)

        self.stock_marketdepth_df = self.client.read_sql(
            f"""
            WITH stock_marketdepth AS (
                SELECT {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxStockMarketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.isins])})
                ORDER BY system_datetime
            )
            , stock_with_lp_marketdepth AS (
                SELECT {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxStockWithLPMarketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.isins])})
                ORDER BY system_datetime
            )
            , derivative_l5marketdepth AS (
                SELECT {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxDerivativeL5Marketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.isins])})
                ORDER BY system_datetime
            )
            , derivative_l10_marketdepth AS (
                SELECT {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxDerivativeL10Marketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.isins])})
                ORDER BY system_datetime
            )
            , marketdepth AS (
                SELECT * FROM stock_marketdepth
                UNION ALL
                SELECT * FROM stock_with_lp_marketdepth
                UNION ALL
                SELECT * FROM derivative_l5marketdepth
                UNION ALL
                SELECT * FROM derivative_l10_marketdepth
                ORDER BY system_datetime
            )
            SELECT * FROM marketdepth
            """
        )
        # order by system_datetime
        self.stock_marketdepth_df = self.stock_marketdepth_df.sort_values(by=["system_datetime"])

        self._iter_idx = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        self._iter_idx += 1
        if self._iter_idx >= len(self.stock_marketdepth_df):
            raise StopIteration
        return self.stock_marketdepth_df.iloc[self._iter_idx]


def elw_batchdata_columns(date_str: str, tz: str): 
    return [
        "isin",
        "underlying_asset_code1",
        "asset_composition_ratio1",
        "intrinsic_price",
        "conversion_rate",
        "lp_holding_quantity",
        f"toDate(system_datetime, '{tz}') as date",
    ]


def stock_elw_batchdata_columns(date_str: str, tz: str): 
    return [
        "isin",
        "base_price",
        "prev_day_closing_price",
        "prev_day_accumulated_trading_amount",
        "main_board_unit_volume",
        "abbreviated_issue_name_in_en",
        "abbreviated_issue_code",
        "exercising_period",
        "elw_bw_exercise_price",
        f"""date_diff('d', 
            toDate(system_datetime, '{tz}'),
            toDate(exercising_period, '{tz}') 
            ) AS days_to_maturity
        """,
        f"toDate(system_datetime, '{tz}') as date",
    ]


class ELWMarketdepthData():
    def __init__(
        self,
        date_str: str,
        elw_isins: List[str],
        underlying_isins: List[str],
        beg_time: str,
        end_time: str,
        tz: str = "Asia/Seoul",
        debug: bool = False
    ):
        self.date_str, self.elw_isins = date_str, elw_isins
        self.debug = debug
        self.underlying_isins = underlying_isins
        self.client = ClickHouseDB(host="localhost", port=port, database=database)

        self.df = self.client.read_sql(
            f"""
            WITH elw_marketdepth AS (
                SELECT 
                    {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxStockWithLPMarketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.elw_isins])})
                ORDER BY system_datetime
            )
            , underlying_derivative_marketdepth AS (
                SELECT 
                    {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxDerivativeL5Marketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.underlying_isins])})
                ORDER BY system_datetime            
            )
            , underlying_stock_marketdepth AS (
                SELECT 
                    {','.join(marketdepth_columns(date_str, tz))}
                FROM default.KrxStockMarketdepth
                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
                AND isin in ({",".join([f"'{isin}'" for isin in self.underlying_isins])})
                ORDER BY system_datetime
            )
            SELECT * FROM elw_marketdepth
            UNION ALL 
            SELECT * FROM underlying_derivative_marketdepth
            UNION ALL 
            SELECT * FROM underlying_stock_marketdepth
            ORDER BY system_datetime 
            """
        )
        # order by system_datetime
        self.df = self.df.sort_values(by=["system_datetime"])
        self._iter_idx = -1


    def __iter__(self):
        return self


    def __next__(self):
        self._iter_idx += 1
        if self._iter_idx >= len(self.df):
            raise StopIteration
        return self.df.iloc[self._iter_idx]


class ELWData():
    def __init__(
            self, 
            date_str: str, 
            elw_issue_name: str, 
            issuer_prefix: str,
            r: float,       # continuously compounded risk-free interest rate
            q: float,       # continuously compounded dividend yield
            underlying_asset_isin: str=None,
            tz: str = "Asia/Seoul",
            debug: bool = False):
        self.date_str = date_str
        self.r, self.q = r, q
        self.elw_issue_name, self.issuer_prefix = elw_issue_name, issuer_prefix
        self.client = ClickHouseDB(host="localhost", port=port, database=database)

        ################################################################
        ## ELW call/put 
        ################################################################
        self.call_df = self.client.read_sql(
            f"""
            SELECT DISTINCT ON (abbreviated_issue_code, exercising_period) 
                isin
                , base_price
                , prev_day_closing_price
                , prev_day_accumulated_trading_amount
                , main_board_unit_volume
                , abbreviated_issue_name_in_en
                , abbreviated_issue_code
                , exercising_period
                , elw_bw_exercise_price
                , date_diff('d', 
                    toDate(system_datetime, '{tz}'),
                    toDate(exercising_period, '{tz}') 
                ) AS days_to_maturity
                , toDate(system_datetime, '{tz}') as date
            FROM default.KrxStockBatchData 
            WHERE date='{date_str}'
                AND abbreviated_issue_name_in_en like '{issuer_prefix}%{elw_issue_name}%C'
                AND prev_day_closing_price > 0
                AND elw_bw_exercise_price > 0
                AND security_group_id='EW'
            ORDER BY elw_bw_exercise_price, prev_day_accumulated_trading_amount DESC
            """
        )

        self.put_df = self.client.read_sql(
            f"""
            SELECT DISTINCT ON (abbreviated_issue_code, exercising_period) 
                isin
                , base_price
                , prev_day_closing_price
                , prev_day_accumulated_trading_amount
                , main_board_unit_volume
                , abbreviated_issue_name_in_en
                , abbreviated_issue_code
                , exercising_period
                , elw_bw_exercise_price
                , date_diff('d', 
                    toDate(system_datetime, '{tz}'),
                    toDate(exercising_period, '{tz}') 
                ) AS days_to_maturity
                , toDate(system_datetime, '{tz}') as date
            FROM default.KrxStockBatchData 
            WHERE 
            date='{date_str}'
                AND abbreviated_issue_name_in_en like '{issuer_prefix}%{elw_issue_name}%P'
                AND prev_day_closing_price > 0
                AND elw_bw_exercise_price > 0
                AND security_group_id='EW'
            ORDER BY elw_bw_exercise_price, prev_day_accumulated_trading_amount DESC 
            """
        )
        #if debug:
        #    display(self.call_df)
        #    display(self.put_df)
  
        self.call_isins = self.call_df["isin"].tolist()
        self.put_isins = self.put_df["isin"].tolist()


        ################################################################
        ## Underlying data
        ################################################################
        self.underlying_df=self.client.read_sql(
            f"""
            SELECT DISTINCT ON (isin)
                isin
                , underlying_asset_code1
                , underlying_asset_code2
                , underlying_asset_code3
                , underlying_asset_code4
                , asset_composition_ratio1
                , asset_composition_ratio2
                , asset_composition_ratio3
                , asset_composition_ratio4
                , intrinsic_price
                , conversion_rate
                , lp_holding_quantity
                , toDate(system_datetime, '{tz}') as date
            FROM default.KrxELWBatchData
            WHERE isin='{self.call_isins[0]}'
                AND date='{date_str}'
            """
        )
        if self.underlying_df.empty:
            raise ValueError("underlying df is empty")
        if ("KR" not in self.underlying_df["underlying_asset_code1"][0]):
            # this most likely means that it tracks an index 
            assert underlying_asset_isin is not None, \
                f"ELW probably tracks an index, so need to provide an underlying asset isin"
            self.underlying_asset_isin = underlying_asset_isin
        else:
            self.underlying_asset_isin = self.underlying_df["underlying_asset_code1"][0]
        self.conversion_rate = self.underlying_df["conversion_rate"][0]
        self.lp_hoding_quantity = self.underlying_df["lp_holding_quantity"][0]

        ## get underlying previous close price
        self.underlying_df = self.client.read_sql(
            f"""
            WITH bd1 AS (
                SELECT DISTINCT ON (isin)
                    isin
                    , base_price
                    , previous_day_closing_price as prev_day_closing_price
                    , abbreviated_issue_name_in_en
                    , toDate(system_datetime, '{tz}') as date
                FROM default.KrxDerivativeBatchData
                WHERE
                    isin='{self.underlying_asset_isin}'
                    AND date='{date_str}'
            )
            , bd2 AS (
                SELECT DISTINCT ON (isin)
                    isin
                    , base_price
                    , prev_day_closing_price
                    , abbreviated_issue_name_in_en
                    , toDate(system_datetime, '{tz}') as date
                FROM default.KrxStockBatchData
                WHERE
                    isin='{self.underlying_asset_isin}'
                    AND date='{date_str}'
            )
            SELECT * FROM bd1 UNION ALL SELECT * FROM bd2
            """
        )
        display(self.underlying_df)
        self.underlying_prev_closing_price = self.underlying_df["prev_day_closing_price"][0]
        self.underlying_base_price = self.underlying_df["base_price"][0]
        self.underlying_asset_price = self.underlying_prev_closing_price
        
        ####################################################################
        # initialize elw vol surface
        ####################################################################
        self.updated_datetime = None
        self.call_vol_surface = {}
        for i, row in enumerate(self.call_df.itertuples()):
            maturity = days_between(
                            row.date.strftime("%Y%m%d"), 
                            row.exercising_period)
            moneyness = row.elw_bw_exercise_price / self.underlying_asset_price
            try:
                sigma = implied_volatility(row.prev_day_closing_price, 
                                           self.underlying_asset_price*self.conversion_rate, 
                                           row.elw_bw_exercise_price * 100, 
                                           maturity / 365,
                                           self.r, self.q, 'c')
            except:
                sigma = 0
            if np.isnan(sigma):
                sigma = 0
 
            self.call_vol_surface[row.isin] = {
                "price": row.prev_day_closing_price,
                "exercise_price": row.elw_bw_exercise_price,
                "moneyness": moneyness, 
                "maturity": maturity, 
                "sigma": sigma
            }


        self.put_vol_surface = {}
        for i, row in enumerate(self.put_df.itertuples()):
            maturity = days_between(
                            row.date.strftime("%Y%m%d"), 
                            row.exercising_period
                        )
            moneyness = row.elw_bw_exercise_price / self.underlying_asset_price
            try:
                sigma = implied_volatility(row.prev_day_closing_price, 
                                            self.underlying_asset_price*self.conversion_rate, 
                                            row.elw_bw_exercise_price * 100, 
                                            maturity / 365, 
                                            self.r, self.q, 'p')
            except:
                sigma = 0
            if np.isnan(sigma):
                sigma = 0
 
            self.put_vol_surface[row.isin] = {
                "price": row.prev_day_closing_price,
                "exercise_price": row.elw_bw_exercise_price,
                "moneyness": moneyness, 
                "maturity": maturity, 
                "sigma": sigma
            }


    def update_elw(self, isin: str, price: float, system_datetime: pd.Timestamp):
        if price <= 0:
            # this means that the orderbook is empty or one sided, so we return
            return
        
        self.updated_datetime = system_datetime

        if isin in self.call_vol_surface:
            self.call_vol_surface[isin]["price"] = price 
            self.update_vol_surface([isin], [])
        elif isin in self.put_vol_surface:
            self.put_vol_surface[isin]["price"] = price
            self.update_vol_surface([], [isin])
        else:
            raise ValueError(f"isin({isin}) not found")


    def update_underlying_price(self, isin: str, price: float, system_datetime: pd.Timestamp):
        assert isin == self.underlying_asset_isin, f"underlying asset isin != {isin}"
        if price <= 0:
            # this means that the orderbook is empty or one sided, so we return
            return
        
        self.updated_datetime = system_datetime

        self.underlying_asset_price = price
        self.update_vol_surface(
            self.call_isins,
            self.put_isins
        )


    def update_vol_surface(self, call_isins, put_isins):
        for n, isin in enumerate(call_isins):
            try:
                sigma = implied_volatility(self.call_vol_surface[isin]["price"],
                                           self.underlying_asset_price*self.conversion_rate, 
                                           self.call_vol_surface[isin]["exercise_price"] * 100, 
                                           self.call_vol_surface[isin]["maturity"] / 365,
                                           self.r, self.q, 'c')
            except:
                sigma = 0
            if np.isnan(sigma):
                sigma = 0
            self.call_vol_surface[isin]["sigma"] = sigma

        for n, isin in enumerate(put_isins):
            try:
                sigma = implied_volatility(self.put_vol_surface[isin]["price"],
                                            self.underlying_asset_price*self.conversion_rate, 
                                            self.put_vol_surface[isin]["exercise_price"] * 100,
                                            self.put_vol_surface[isin]["maturity"] / 365,
                                            self.r, self.q, 'p')
            except:
                sigma = 0
            if np.isnan(sigma):
                sigma = 0
            self.put_vol_surface[isin]["sigma"] = sigma


    @staticmethod
    def vol_surface_plot(call_vol_surface, put_vol_surface, ts: pd.Timestamp):
        #call_data = np.array(
        call_data = np.array(
            [(vol["moneyness"], vol["maturity"], vol["sigma"]) 
             for vol in call_vol_surface.values()]
        )

        #put_data = np.array(
        put_data = np.array(
            [(vol["moneyness"], vol["maturity"], vol["sigma"]) 
             for vol in put_vol_surface.values()]
        )

        cmin = min(call_data[:, 2].min(), put_data[:, 2].min())
        cmax = max(call_data[:, 2].max(), put_data[:, 2].max())
        print(cmin, cmax)
        print(call_data[:, 2].min(), put_data[:, 2].min())
        print(call_data[:, 2].max(), put_data[:, 2].max())

        # Extract X, Y, and Z coordinates from the data
        x_coords1, y_coords1, z_coords1 = call_data[:, 0], call_data[:, 1], call_data[:, 2]
        x_coords2, y_coords2, z_coords2 = put_data[:, 0], put_data[:, 1], put_data[:, 2]

        # Define the grid for the surface plots
        x_range1, y_range1 = np.linspace(min(x_coords1), max(x_coords1), 100), np.linspace(min(y_coords1), max(y_coords1), 100)
        x_grid1, y_grid1 = np.meshgrid(x_range1, y_range1)

        x_range2, y_range2 = np.linspace(min(x_coords2), max(x_coords2), 100), np.linspace(min(y_coords2), max(y_coords2), 100)
        x_grid2, y_grid2 = np.meshgrid(x_range2, y_range2)

        # Interpolate the Z values to create smooth surfaces
        z_grid1 = griddata((x_coords1, y_coords1), z_coords1, (x_grid1, y_grid1), method='linear')
        z_grid2 = griddata((x_coords2, y_coords2), z_coords2, (x_grid2, y_grid2), method='linear')

        # Create the 3D surface plots
        fig = go.Figure()

        # Add the first surface to the figure
        fig.add_trace(go.Surface(z=z_grid1, x=x_range1, y=y_range1, name='Call ELW', cmin=cmin, cmax=cmax))

        # Add the second surface to the figure
        fig.add_trace(go.Surface(z=z_grid2, 
                                 x=x_range2,
                                 y=y_range2, 
                                 name='Put ELW', 
                                 cmin=cmin, 
                                 cmax=cmax, showscale=False))

        # Add axis labels and a title
        fig.update_layout(scene=dict(
                            xaxis_title='moneyness',
                            yaxis_title='maturity',
                            zaxis_title='IV'),
                          width=800,
                          height=600,
                          title=f"ELW Call and Put IV @ {ts}")

        # Show the plot
        fig.show()


    @staticmethod
    def vol_scatter_plot(call_vol_surface, put_vol_surface, ts: pd.Timestamp):
        #call_data = np.array(
        call_data = np.array(
            [(vol["moneyness"], vol["maturity"], vol["sigma"]) 
             for vol in call_vol_surface.values()]
        )

        #put_data = np.array(
        put_data = np.array(
            [(vol["moneyness"], vol["maturity"], vol["sigma"]) 
             for vol in put_vol_surface.values()]
        )

        # Extract X, Y, and Z coordinates from the data
        x_coords1, y_coords1, z_coords1 = call_data[:, 0], call_data[:, 1], call_data[:, 2]
        x_coords2, y_coords2, z_coords2 = put_data[:, 0], put_data[:, 1], put_data[:, 2]

        # Create the 3D scatter plots using go.Scatter3d
        fig = go.Figure()

        # Add the second scatter plot to the figure
        fig.add_trace(go.Scatter3d(x=x_coords2, y=y_coords2, z=z_coords2, mode='markers', name='Put ELW'))

        # Add the first scatter plot to the figure
        fig.add_trace(go.Scatter3d(x=x_coords1, y=y_coords1, z=z_coords1, mode='markers', name='Call ELW',))

        # Add axis labels and a title
        fig.update_layout(scene=dict(
                            xaxis_title='moneyness',
                            yaxis_title='maturity',
                            zaxis_title='IV'),
                          width=800,
                          height=600,
                          title=f"ELW Call and Put IV @ {ts}")

        # Show the plot
        fig.show()


class ETNBatchData():
    def __init__(
            self, 
            isins: List[str], 
            date_str: str, 
            tz: str = "Asia/Seoul",
            debug: bool = False):
        self.isins = isins
        self.date_str, self.tz, self.debug = date_str, tz, debug
        self.client = ClickHouseDB(host="localhost", port=port, database=database)
        
        self.df = self.client.read_sql(
            f"""
            WITH iv_data as (SELECT DISTINCT ON (isin, date) 
                isin
                , previous_day_IV / 100. AS prev_day_iv
                , toDate(system_datetime, '{tz}') AS date
                , toTimeZone(system_datetime, '{tz}') AS system_datetime
            FROM default.KrxETNIIV
            WHERE 
                isin in ({",".join([f"'{isin}'" for isin in isins])})
                AND date = '{date_str}'
            )
            , batch_data AS (
                SELECT DISTINCT ON (isin)
                    {','.join(stock_batchdata_columns(tz))}
                FROM default.KrxStockBatchData
                WHERE 
                isin in ({",".join([f"'{isin}'" for isin in isins])})
                AND date = '{date_str}'
            )
            SELECT * FROM batch_data 
            INNER JOIN iv_data
            ON batch_data.isin = iv_data.isin
            ORDER BY isin
            """
        )


"""
Vanilla put option implied volatility
"""
def put_option_iv(P, S, E, r, t, sigma, q, tol=1e-3, max_iter=2500):
    # Newton Raphson with dividend
    for i in range(max_iter):
        d1 = (np.log(S/E) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)
        P_new = E * np.exp(-r * t) * norm.cdf(-d2) - S * np.exp(-q * t) * norm.cdf(-d1)
        vega = S * np.exp(-q * t) * norm.pdf(d1) * np.sqrt(t) 
        diff = P - P_new
        if abs(diff) < tol:
            return sigma
        if vega <= 0:
            return 0
        sigma = sigma + diff/vega/100
    return sigma


"""
Vanilla call option implied volatility
"""
def call_option_iv(C, S, E, r, t, sigma, q, tol=1e-3, max_iter=2500):
    # Newton Raphson with dividend
    for i in range(max_iter):
        d1 = (np.log(S/E) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)
        C_new = S * np.exp(-q * t) * norm.cdf(d1) - E * np.exp(-r * t) * norm.cdf(d2)
        vega = S * np.exp(-q * t) * norm.pdf(d1) * np.sqrt(t)
        diff = C - C_new
        if abs(diff) < tol:
            return sigma
        if vega <= 0:
            return 0
        sigma = sigma + diff/vega/100
    return sigma



#class StockTradeAndMarketdepthData():
#    def __init__(
#        self,
#        isin: str,
#        prev_day_closing_price: float,
#        date_str: str,
#        beg_time: str,
#        end_time: str,
#        vol_interval_sec: int = 300,
#        tz: str = "Asia/Seoul",
#    ):
#        self.isin, self.date_str, self.beg_time, self.end_time, self.tz = isin, date_str, beg_time, end_time, tz
#        self.vol_interval_sec = vol_interval_sec
#        self.prev_day_closing_price = prev_day_closing_price
#        self.client = ClickHouseDB(host="localhost", port=port, database=database)
#
#
#        def marketdepth_columns(date_str): 
#            return [
#                "isin",
#                "l1askprice",
#                "l1asksize",
#                "l1bidprice",
#                "l1bidsize",
#                "l2askprice",
#                "l2asksize",
#                "l2bidprice",
#                "l2bidsize",
#                "(l1askprice + l1bidprice) / 2 AS midprice",
#                "l1askprice - l1bidprice AS spread",
#                """(l1askprice * l1bidsize + l1bidprice * l1asksize) / (l1asksize + l1bidsize) 
#                    AS weighted_midprice""",
#                f"""100*(midprice - {prev_day_closing_price}) / {prev_day_closing_price} AS midprice_return""",
#                f"""100*(weighted_midprice - {prev_day_closing_price}) / {prev_day_closing_price} AS weighted_midprice_return""",
#                f"toDate(system_datetime, '{tz}') as date",
#                f"toTimeZone(system_datetime, '{tz}') as system_datetime",
#            ]
#
#        def trade_columns(date_str):
#            return [
#                "isin",
#                "trade_price",
#                "trade_volume",
#                "trade_price * trade_volume AS trade_value",
#                "sum(if(trade_type='BUY', trade_value, 0)) OVER acc_wndw AS acc_bid_value",
#                "sum(if(trade_type='SELL', trade_value, 0)) OVER acc_wndw AS acc_ask_value",
#                "sum(if(trade_type='BUY', trade_volume, 0)) OVER acc_wndw AS acc_bid_volume",
#                "sum(if(trade_type='SELL', trade_volume, 0)) OVER acc_wndw AS acc_ask_volume",
#                "acc_bid_value - acc_ask_value AS trade_value_imbalance",
#                "acc_bid_volume - acc_ask_volume AS trade_volume_imbalance",
#                "accumulated_trade_volume",
#                "trade_type",
#                "max(trade_price) OVER wndw AS high_price",
#                "min(trade_price) OVER wndw AS low_price",
#                "first_value(trade_price) OVER wndw AS open_price",
#                "last_value(trade_price) OVER wndw AS close_price",
#                "100*sqrt(0.5 * pow(log(high_price) - log(low_price), 2) - (2 * log(2) - 1)*pow(log(close_price) - log(open_price), 2)) AS gk_rv",
#                #"stddevPopStable(trade_price) OVER wndw AS rv",
#                f"toTimeZone(system_datetime, '{tz}') as system_datetime",
#            ]
#
#
#        self.df = self.client.read_sql(
#            f"""
#            WITH stock_trade AS (
#                SELECT {','.join(trade_columns(date_str))}
#                FROM default.KrxStockTrade
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin='{isin}'
#                WINDOW wndw AS (
#                    PARTITION BY isin
#                    ORDER BY toUnixTimestamp(system_datetime)
#                    RANGE BETWEEN {vol_interval_sec} PRECEDING AND CURRENT ROW
#                )
#                , acc_wndw AS (
#                    PARTITION BY isin
#                    ORDER BY system_datetime
#                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
#                )
#                ORDER BY system_datetime
#            )
#            , derivative_trade AS (
#                SELECT {','.join(trade_columns(date_str))}
#                FROM default.KrxDerivativeTrade
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin='{isin}'
#                WINDOW wndw AS (
#                    PARTITION BY isin
#                    ORDER BY toUnixTimestamp(system_datetime)
#                    RANGE BETWEEN {vol_interval_sec} PRECEDING AND CURRENT ROW
#                )
#                , acc_wndw AS (
#                    PARTITION BY isin
#                    ORDER BY system_datetime
#                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
#                )
#                ORDER BY system_datetime   
#            )
#            , trade AS (
#                SELECT * FROM stock_trade
#                UNION ALL
#                SELECT * FROM derivative_trade
#                ORDER BY system_datetime
#            )
#            , stock_marketdepth AS (
#                SELECT {','.join(marketdepth_columns(date_str))}
#                FROM default.KrxStockMarketdepth
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin = '{isin}'
#                AND (l1askprice > 0 AND l1bidprice > 0)
#                ORDER BY system_datetime
#            )
#            , stock_with_lp_marketdepth AS (
#                SELECT {','.join(marketdepth_columns(date_str))}
#                FROM default.KrxStockWithLPMarketdepth
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin = '{isin}'
#                AND (l1askprice > 0 AND l1bidprice > 0)
#                ORDER BY system_datetime
#            )
#            , derivative_l5marketdepth AS (
#                SELECT {','.join(marketdepth_columns(date_str))}
#                FROM default.KrxDerivativeL5Marketdepth
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin = '{isin}'
#                AND (l1askprice > 0 AND l1bidprice > 0)
#                ORDER BY system_datetime
#            )
#            , derivative_l10_marketdepth AS (
#                SELECT {','.join(marketdepth_columns(date_str))}
#                FROM default.KrxDerivativeL10Marketdepth
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin = '{isin}'
#                AND (l1askprice > 0 AND l1bidprice > 0)
#                ORDER BY system_datetime
#            )
#            , marketdepth AS (
#                SELECT * FROM stock_marketdepth
#                UNION ALL
#                SELECT * FROM stock_with_lp_marketdepth
#                UNION ALL
#                SELECT * FROM derivative_l5marketdepth
#                UNION ALL
#                SELECT * FROM derivative_l10_marketdepth
#                ORDER BY system_datetime
#            )
#            , trade_and_marketdepth AS (
#                SELECT 
#                      trade.isin
#                    , trade.trade_price
#                    , trade.trade_volume
#                    , trade.acc_bid_volume
#                    , trade.acc_ask_volume
#                    , trade.acc_bid_value
#                    , trade.acc_ask_value
#                    , trade.trade_value_imbalance
#                    , trade.trade_volume_imbalance
#                    , trade.accumulated_trade_volume
#                    , trade.trade_type
#                    , trade.gk_rv
#                    , marketdepth.midprice_return
#                    , marketdepth.weighted_midprice_return
#                    , marketdepth.l1askprice
#                    , marketdepth.l1asksize
#                    , marketdepth.l1bidprice
#                    , marketdepth.l1bidsize
#                    , marketdepth.weighted_midprice
#                    , marketdepth.midprice
#                    , marketdepth.spread
#                    , toTimeZone(trade.system_datetime, '{tz}') as system_datetime
#                FROM trade
#                ASOF LEFT JOIN marketdepth
#                ON trade.isin = marketdepth.isin 
#                AND trade.system_datetime >= marketdepth.system_datetime
#                ORDER BY trade.system_datetime
#            )
#            SELECT 
#                *,
#                trade_volume_imbalance - last_value(trade_volume_imbalance) OVER lag_wndw AS trade_volume_imbalance_diff
#            FROM trade_and_marketdepth
#            WHERE (l1askprice > 0 AND l1bidprice > 0)
#            WINDOW lag_wndw AS (
#                    PARTITION BY isin
#                    ORDER BY system_datetime
#                    ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
#                )
#            ORDER BY system_datetime
#            """
#        )
#
#
#        self._iter_idx = -1
#
#    def __iter__(self):
#        return self
#    
#    def __next__(self):
#        self._iter_idx += 1
#        if self._iter_idx >= len(self.df):
#            raise StopIteration
#        return self.df.iloc[self._iter_idx]


#class RealizedVolatilityData():
#    def __init__(
#        self,
#        isin: str,
#        date_str: str,
#        beg_time: str,
#        end_time: str,
#        interval_sec: int = 300,   # 5 minute
#        tz: str = "Asia/Seoul",
#    ):
#        self.isin = isin
#        self.date_str = date_str
#        self.beg_time = beg_time
#        self.end_time = end_time
#        self.tz = tz
#        self.client = ClickHouseDB(host="localhost", port=port, database=database)
#
#        self.rv = self.client.read_sql(
#            f"""
#            WITH derivative_trade AS (
#                SELECT 
#                    isin
#                    , trade_price
#                    , trade_volume
#                    , max(trade_price) OVER wndw AS high_price
#                    , min(trade_price) OVER wndw AS low_price
#                    , first_value(trade_price) OVER wndw AS open_price
#                    , last_value(trade_price) OVER wndw AS close_price
#                    , 100*sqrt(0.5 * pow(log(high_price) - log(low_price), 2) - (2 * log(2) - 1)*pow(log(close_price) - log(open_price), 2)) AS gk_rv
#                    , stddevPopStable(trade_price) OVER wndw AS rv
#                    , toTimeZone(system_datetime, '{tz}') as system_datetime
#                FROM default.KrxDerivativeTrade
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin='{isin}'
#                WINDOW wndw AS (
#                    PARTITION BY isin
#                    ORDER BY toUnixTimestamp(system_datetime)
#                    RANGE BETWEEN {interval_sec} PRECEDING AND CURRENT ROW
#                )
#                ORDER BY system_datetime
#            )
#            , stock_trade AS (
#                SELECT
#                    isin
#                    , trade_price
#                    , trade_volume
#                    , max(trade_price) OVER wndw AS high_price
#                    , min(trade_price) OVER wndw AS low_price
#                    , first_value(trade_price) OVER wndw AS open_price
#                    , last_value(trade_price) OVER wndw AS close_price
#                    , 100*sqrt(0.5 * pow(log(high_price) - log(low_price), 2) - (2 * log(2) - 1)*pow(log(close_price) - log(open_price), 2)) AS gk_rv
#                    , stddevPopStable(trade_price) OVER wndw AS rv
#                    , toTimeZone(system_datetime, '{tz}') as system_datetime
#                FROM default.KrxStockTrade
#                WHERE {common_where_clause(date_str, beg_time, end_time, tz)}
#                AND isin='{isin}'
#                WINDOW wndw AS (
#                    PARTITION BY isin
#                    ORDER BY toUnixTimestamp(system_datetime)
#                    RANGE BETWEEN {interval_sec} PRECEDING AND CURRENT ROW
#                )
#                ORDER BY system_datetime
#            )
#            SELECT * FROM derivative_trade
#            UNION ALL
#            SELECT * FROM stock_trade
#            ORDER BY system_datetime
#            """
#        )
#        
#        self._iter_idx = -1
#
#    def __iter__(self):
#        return self
#    
#    def __next__(self):
#        self._iter_idx += 1
#        if self._iter_idx >= len(self.rv):
#            raise StopIteration
#        return self.rv.iloc[self._iter_idx]
#
#


"""
Vanilla Black Scholes Merton model
"""
def vanilla_bsm_test():
    # Test
    C = 1.875   # call option price
    S = 21      # underlying price
    E = 20      # strike price
    r = 0.1     # continuously compounded risk-free interest rate
    t = 0.25    # time to expiration
    q = 0       # continuously compounded dividend yield

    sigma = call_option_iv(C, S, E, r, t, 0.5, q)
    print(sigma)
    assert(abs(sigma  - 0.2345) < 1e-3)

    C = 1.9174
    S = 10
    E = 12
    r = 0.05
    t = 2
    q = 0

    sigma = call_option_iv(C, S, E, r, t, 0.5, q)
    assert(abs(sigma - 0.4) < 1e-3)
    print(sigma)

