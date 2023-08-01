from typing import Dict
import copy

class Orderbook():
    def __init__(
            self, 
            name, 
            isin, 
            level: int=5):
        self.name = name
        self.isin = isin
        self.level = level
        self.book = {"ask": {}, "bid": {}}
        self.system_datetime = None
        self.converted_book = None


    def get(self):
        return self.book
    

    def laskprice(self, level: int):
        return sorted(self.book["ask"].keys())[level-1]
    

    def lbidprice(self, level: int):
        return sorted(self.book["bid"].keys(), reverse=True)[level-1]


    def __repr__(self):
        ask = "\n".join([f"{price}\t|\t{size}" for price, size in sorted(self.book["ask"].items(), reverse=True)])
        bid = "\n".join([f"{price}\t|\t{size}" for price, size in sorted(self.book["bid"].items(), reverse=True)])
        orderbook_str = f"""
{self.name}, {self.isin}
{ask}
-----------------------------
{bid}
        """
        if self.converted_book:
            converted_ask = "\n".join([f"{price}\t|\t{size}" for price, size in sorted(self.converted_book["ask"].items(), reverse=True)])
            converted_bid = "\n".join([f"{price}\t|\t{size}" for price, size in sorted(self.converted_book["bid"].items(), reverse=True)])
            orderbook_str += f"""\n
converted book
{converted_ask}
-----------------------------
{converted_bid}
            """
        return orderbook_str


    def convert(
            self,
            leverage: int,
            previous_day_price: float,
            target_isin: str,
            target_l1askprice: float,
            target_l1bidprice: float,
            target_multiplier: float,
            target_prev_day_closing: float):
        self.converted_book = {"ask": {}, "bid": {}}
        if self.isin == target_isin:
            self.converted_book = copy.deepcopy(self.book)
            return

        for side in ["ask", "bid"]:
            opp_side = "bid" if side == "ask" else "ask"
            for price, size in self.book[side].items():
                converted_price = round(
                    target_prev_day_closing * (1 + ((price / previous_day_price) - 1) / leverage),
                    1)
                if side == "bid":
                    converted_size = round(
                        size / (target_l1bidprice * target_multiplier / (price * abs(leverage)))
                        , 2)
                else:
                    converted_size = round(
                        size / (target_l1askprice * target_multiplier / (price * abs(leverage)))
                        , 2)
                if leverage < 0:
                    self.converted_book[opp_side][converted_price] = converted_size
                else:
                    self.converted_book[side][converted_price] = converted_size


    def update(self, row):
        self.book = {"ask": {}, "bid": {}}
        self.system_datetime = row["system_datetime"]
        for l in range(1, self.level+1):
            lbidprice = row[f"l{l}bidprice"]
            lbidsize = row[f"l{l}bidsize"]
            laskprice = row[f"l{l}askprice"]
            lasksize = row[f"l{l}asksize"]

            if lbidprice > 0:
                self.book["bid"][lbidprice] = lbidsize
            if laskprice > 0:
                self.book["ask"][laskprice] = lasksize

