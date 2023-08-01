from notebooks.orderbook import *
from typing import List

class AggregatedOrderbook():
    def __init__(self):
        self.orderbooks: Dict[str, Orderbook] = {}
        self.consolidated_book = {"ask": {}, "bid": {}}
        self.system_datetime = None


    def get(self):
        return self.consolidated_book


    def update(self, orderbook: Orderbook, system_datetime):
        self.orderbooks[orderbook.isin] = orderbook  
        self.system_datetime = system_datetime
        self.aggregate()


    def agg_l1askprice(self, isins: List[str]):
        avg_price = 0
        remaining_size = 1
        for price, q in sorted(self.consolidated_book["ask"].items()):
            for isin, size in q:
                if isin in isins:
                    avg_price += min(remaining_size, size) * price
                    remaining_size = max(0, remaining_size - size)
                
                if remaining_size <= 0:
                    return avg_price




    def agg_l1bidprice(self, isins: List[str]):
        avg_price = 0
        remaining_size = 1
        for price, q in sorted(self.consolidated_book["bid"].items(), reverse=True):
            for isin, size in q:
                if isin in isins:
                    avg_price += min(remaining_size, size) * price
                    remaining_size = max(0, remaining_size - size)
                
                if remaining_size <= 0:
                    return avg_price


    def aggregate(self):
        self.consolidated_book = {"ask": {}, "bid": {}}
        orderbook: Orderbook
        for orderbook in self.orderbooks.values():
            converted_orderbook = orderbook.converted_book
            if converted_orderbook is None:
                continue
            for side in ["ask", "bid"]:
                for price, size in converted_orderbook[side].items():
                    if price not in self.consolidated_book[side]:
                        self.consolidated_book[side][price] = []
                    self.consolidated_book[side][price].append((orderbook.isin, size))


    def __repr__(self):
        prices = sorted(list(
            set(self.consolidated_book["ask"].keys()).union(
            set(self.consolidated_book["bid"].keys()))), reverse=True)
        askbid = "\n".join(
[(f"{price}"
  f"\t{str(self.consolidated_book['ask'][price]).strip('[]') if price in self.consolidated_book['ask'] else '': <85}"
  f"||{str(self.consolidated_book['bid'][price]).strip('[]') if price in self.consolidated_book['bid'] else '': <85}")
 for price in prices])
        return f"""
Aggregated orderbook {self.system_datetime}
{askbid}
"""

