from typing import Dict, Tuple, List
from notebooks.orderbook import *

from src.db.clickhouse_db import ClickHouseDB

# global variables
port=18123
database="test"


class Relation():
    def __init__(self, weight: float):
        self.weight = weight

    def __repr__(self):
        return f"""
            weight: {self.weight}
        """


# 1. create nodes
class Node():
    def __init__(
        self,
        isin: str,  
        date_str: str,
        name: str,
        sectype: str,
        secsubtype: str,
        multiplier: float,
        tick_size: float,
        creation_unit: int,
        leverage: int,
        tz: str = "Asia/Seoul",
        debug: bool = False, 
    ):
        self.neighbors_out: Dict['Node', Relation] = {}
        self.neighbors_in: Dict['Node', Relation] = {}

        self.isin, self.name = isin, name
        self.sectype, self.secsubtype = sectype, secsubtype
        self.multiplier = multiplier
        self.tick_size = tick_size
        self.creation_unit = creation_unit
        self.leverage = leverage
        self.tz, self.debug = tz, debug

        self.client = ClickHouseDB(host="localhost", port=port, database=database)
        iv_data = self.client.read_sql(
            f"""
            WITH iv AS (SELECT DISTINCT ON (isin, date) 
                previous_day_IV / 100. AS prev_day_iv_nav
                , toDate(system_datetime, '{tz}') AS date
            FROM default.KrxETNIIV
            WHERE isin='{isin}' AND date = '{date_str}')
            , nav AS (SELECT DISTINCT ON (isin, date)
                previous_day_nav / 100. AS prev_day_iv_nav
                , toDate(system_datetime, '{tz}') AS date
            FROM default.KrxETFNAV
            WHERE isin='{isin}' and date='{date_str}'
            LIMIT 1
            )
            SELECT * FROM iv
            UNION ALL
            SELECT * FROM nav
           """
        )
        self.prev_day_iv_nav = iv_data["prev_day_iv_nav"][0] if not iv_data.empty else None

        batch_data = self.client.read_sql(
            f"""
            WITH derivative_batch_data AS (SELECT DISTINCT ON (isin) 
                isin
                , base_price
                , previous_day_closing_price
                , toDate(system_datetime, '{tz}') as date
            FROM default.KrxDerivativeBatchData
            WHERE isin='{isin}' AND date='{date_str}')
            , stock_batch_data AS (
                SELECT DISTINCT ON (isin)
                isin
                , base_price
                , prev_day_closing_price
                , toDate(system_datetime, '{tz}') AS date
            FROM default.KrxStockBatchData
            WHERE isin='{isin}' AND date='{date_str}'
            ORDER BY isin
            )
            SELECT * FROM derivative_batch_data
            UNION ALL
            SELECT * FROM stock_batch_data
            ORDER BY isin
            """
        )
        self.prev_day_closing_price = batch_data["previous_day_closing_price"][0]
        self.base_price = batch_data["base_price"][0]

        self.orderbook = Orderbook(
            name, 
            isin,
        )


    def __repr__(self):
        neighbors_out_repr = "\n\t\t".join(
            [f"({node.isin}, {relation.weight}, {node.name})" for node, relation in self.neighbors_out.items()]) 
        neighbors_in_repr = "\n\t\t".join(
            [f"({node.isin}, {relation.weight}, {node.name})" for node, relation in self.neighbors_in.items()])
        return f"""
            security isin: {self.isin} 
            security prev closing price: {self.prev_day_closing_price}
            security prev iv/nav: {self.prev_day_iv_nav}
            security name: {self.name}
            security type: {self.sectype}
            neighbors out: \n\t\t{neighbors_out_repr}
            neighbors in: \n\t\t{neighbors_in_repr}
        """


    def update_neighbor_out(
            self, 
            neighbor: 'Node', 
            relation: Relation):
        self.neighbors_out[neighbor] = relation


    def update_neighbor_in(
            self, 
            neighbor: 'Node', 
            relation: Relation):
        self.neighbors_in[neighbor] = relation


# 2. create graph
class Graph():
    def __init__(self):
        self.nodes: Dict[str, Node] = {}


    def get(self, isin: str) -> Node:
        return self.nodes[isin]


    def update_node(self, node: Node) -> bool:
        assert(isinstance(node, Node))
        self.nodes[node.isin] = node


    def remove_edge(
            self, 
            start: Node, 
            end: Node):
        assert(start.isin in self.nodes 
               and end.isin in self.nodes)
        del self.nodes[start.isin].neighbors_out[end]
        del self.nodes[end.isin].neighbors_in[start]


    def update_edge(
            self, 
            start: Node, 
            end: Node, 
            relation: Relation):
        assert(start.isin in self.nodes 
               and end.isin in self.nodes)
        self.nodes[start.isin].update_neighbor_out(end, relation)
        self.nodes[end.isin].update_neighbor_in(start, relation)


    def __repr__(self):
        return "Graph({})".format(self.nodes)

