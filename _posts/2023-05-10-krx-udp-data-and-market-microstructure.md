---
title: KRX UDP Data and Market Microstructure
category: finance
tags:
    - market microstructure
    - krx
    - udp
mathjax: true
comments: true
layout: single
classes: wide
published: true
---

Korean Stock Exchange (KRX) is the only securities exchange in South Korea. Equities and ETPs get traded in Seoul while futures, options, and other derivatives get traded in Busan (hence, there exists an opportunity for latency arbitrage).

To gain a speed advantage, lots of firms place their trading engines near the matching engine, which is called co-location. A co-located trading engine receives its data via UDP as opposed to TCP which requires a handshake process that increases the latency. 

Going through KRX data specification sheet is not an easy task. It contains information on all types of messages sent from the KRX matching engine. In this post, I will go over messages that are most frequently used but if you're a data engineer at your company, I highly recommended that you peruse them.

## Tradable Securities
KRX securities contain equities, futures, and options.

Equities can be largely divided into three markets: KOSPI, KOSDAQ, and KONEX. 

In the Korean futures market, equity index futures exhibit the biggest volume: kospi200 futures and kosdaq150 futures. Equity futures are also traded in KRX but their volumes aren't as consistent. 

As opposed to other securities, options are least traded securities in KRX since there aren't many options contracts to trade. There are option contracts for kospi200, kosdaq150 and mini kospi200. Unlike the US market, individual stock options aren't available and are replaced by ELW. 


## IP address and port number
Each data gets received from differnet ip address and ports. For instance, messages containing kospi200 futures orderbook data are received from `233.38.231.112:10342` while those of kosdaq150 are received from `233.38.231.112:10343`. For kospi equity trade data, the ip address is `233.38.231.2` with ports ranging from `10022` to `10026`. Therefore, when receiving data, you need to make sure you are listening to the correct ip address and port.

Below is an exmaple config yaml file that maps data types to port number:
```yaml
udp_port_mappings:
  # 증권 A : KOSPI
  # 증권 B : KOSDAQ
  # 증권 C : ETF, ELW, ETN

  ## 증권 A, 유가증권수직 12M/100M 
  10001:                    "stockA"             # stock fundamental
  
  ## 증권 A, 유가증권수직 12M
  10022:                    "stockA"     # trade (group 00001) 
  10023:                    "stockA"     # trade (group 00002)
  10024:                    "stockA"     # trade (group 00003)
  10025:                    "stockA"     # trade (group 00004)
  10026:                    "stockA"     # trade (group 00005)
  10027:                    "stockA"     # orderbook 
  10028:                    "stockA"     # orderbook

  ## 증권 B, 코스닥통합 12M/100M
  10101:                    "stockB"     # stock fundamental
  10107:                    "stockB"     # 주식종목정보변경  
  10108:                    "stockB"     # 종목별 투자자별 종가 통계
  10111:                    "stockB"     # stock fundamental
  10117:                    "stockB"     # stock index

  ## 증권 B, 코스닥통합12M
  10122:                    "stockB"     # trade (group 00001)
  10123:                    "stockB"     # trade (group 00002)
  10124:                    "stockB"     # trade (group 00003)
  10125:                    "stockB"     # trade (group 00004)
  10126:                    "stockB"     # trade (group 00005)
  10127:                    "stockB"     # orderbook
  10128:                    "stockB"     # orderbook
  
  10132:                    "stockB"     # stock info
  10133:                    "stockB"     # stock info

  ## 증권 C, 증권상품 12M/100M
  10201:                    "stockC"     # stock fundamental    
  10207:                    "stockC"     # stock info
  
  ## 증권 C, 증권상품12M
  10222:                    "stockC"     # trade (group 00006)
  10223:                    "stockC"     # trade (group 00007)
  10224:                    "stockC"     # trade (group 00008)
  10225:                    "stockC"     # trade (group 00009)
  10226:                    "stockC"     # trade (group 00010)
  10227:                    "stockC"     # orderbook
  10228:                    "stockC"     # orderbook

  10231:                    "stockC"     # ETF PDF
  10232:                    "stockC"     # ETF Nav
  10233:                    "stockC"     # overseas etf nav
  10234:                    "stockC"     # ELW sensitivity
  10235:                    "stockC"     # elw
  10236:                    "stockC"     # etn IIV
  10237:                    "stockC"     # ETF NAV


  ### 파생 A, 통합선물 100M

  ## 파생 A, 통합선물 12M/100M
  10301:                    "futureA"    # stock fundamental 
  10315:                    "futureA"    # stock fundamental
  10316:                    "futureA"    # stock fundamental
  10321:                    "futureA"    # option fundamental

  ## 파생 A, 통합선물 12M
  10342:                    "futureA"    # kospi200 future 
  10343:                    "futureA"    # kosdaq150 future
  10344:                    "futureA"    # equity future
  10345:                    "futureA"    # tbill future
  10346:                    "futureA"    # gold future
  10347:                    "futureA"    # mini kospi200 future
  10348:                    "futureA"    # kospi200 volatility future
  10349:                    "futureA"    # kospi200 sector index future
  10350:                    "futureA"    # krx300 future

  10362:                    "futureA"    # kospi200 call option
  10363:                    "futureA"    # kosdaq150 call option
  10364:                    "futureA"    # equity call option
  10366:                    "futureA"    # mini kospi200 call option
  10367:                    "futureA"    # weekly kospi200 call option

  10371:                    "futureA"    # kospi200 put option
  10372:                    "futureA"    # kosdaq150 put option
  10373:                    "futureA"    # equity put option
  10375:                    "futureA"    # mini kospi200 put option
  10376:                    "futureA"    # kospi200 weekly put option
```


## KRX Message
Each message can be identified with a message type code and a message type subcode. As an example, the Korean exchange sends out a stock directory message (aka stock batch data) that contains information about the stock. This informaton includes the isin, number of listed shares, ipo date, tradability, previous day closing price, and so on. As you can see, it contains vital information for traders. Putting everything together, we can summarize the message into a yaml file as shown below:

```yaml
messages:
  IFMSBTD0001:
    name: StockBatchDataMessage
    code: A0
    subcodes:
      - 01S
      - 02S
      - 03S
      - 04S
      - 01Q
      - 01X
    fields:
      data_category:
        size: 2
        datatype_py: str
        datatype_rs: String
      information_category:
        size: 3
        datatype_py: str
        datatype_rs: String
      message_sequence_number:
        size: 8
        datatype_py: str
        datatype_rs: String 
      contract_instruments_total_number:
        size: 6
        datatype_py: int
        datatype_rs: i32
      business_date:
        size: 8
        datatype_py: str
        datatype_rs: String
      isin:
        size: 12
        datatype_py: str
        datatype_rs: String
      designated_issue_number:
        size: 6
        datatype_py: str
        datatype_rs: String
      
      ...
      
      ...

      ...
      
     upper_limit_quantity:
        size: 23
        datatype_py: float
      investment_warning_issue:
        size: 1
        datatype_py: str
        datatype_rs: String
      insufficient_number_of_listed_shares:
        size: 1
        datatype_py: str
        datatype_rs: String
      spac_merger:
        size: 1
        datatype_py: str
        datatype_rs: String
      segment_type_code:
        size: 1
        datatype_py: str
        datatype_rs: String
      system_datetime:      # created by our system!
        size: 19
        datatype_py: int
        datatype_rs: i64
```

Let's go over the yaml file line by line. Every message has its own unique interface id, and the above stock batch data message has an interface id of `IFMSBTD0001`. The `code` field is used by the parser to determine the message type and the `subcodes` field contains information about security types and markets (e.g. `04F` subcode indicates equity futures).

Some messages contain exchange datetime field which has a microsecond precision. To get a better precision, our trading engine inserts a nanosecond timestamp after every message and we denote it as `system_datetime`.

The `size` field indicates the byte length of the field, `datatype_py` field is the type we wish to convert the bytes into when using python, and `datatype_rs` for rust programming language. 

I attached a yaml file that summarized most frequently used KRX messages. 


### Opening and Closing Auction
```yaml
messages:
  IFMSRPD0004:
    name: StockTradeMessage
    contains: stock_trade
    code: A3
    subcodes:
      - 01S
      - 01Q
      - 01X
      - 02S
      - 03S
      - 04S
    fields:
      data_category:
        size: 2
        datatype_py: str
        datatype_rs: String
      information_category:
        size: 3
        datatype_py: str
        datatype_rs: String
      message_sequence_number:
        size: 8
        datatype_py: str
        datatype_rs: String 
      board_id:
        size: 2
        datatype_py: str
        datatype_rs: String
      session_id:
        size: 2
        datatype_py: str
        datatype_rs: String
      isin:
        size: 12
        datatype_py: str
        datatype_rs: String
      designated_issue_number:
        size: 6
        datatype_py: str
        datatype_rs: String
      datetime:
        size: 12
        datatype_py: chrono.krx_time_to_timestamp
        datatype_rs: i64
      price_change_since_previous_day_code:
        size: 1
        datatype_py: str
        datatype_rs: String
      price_change_since_previous_day_price:
        size: 11
        datatype_py: float
        datatype_rs: double
      trade_price:
        size: 11
        datatype_py: float
        datatype_rs: double
      trade_volume:
        size: 10
        datatype_py: int
      opening_price:
        size: 11
        datatype_py: float
        datatype_rs: double
      high_price:
        size: 11
        datatype_py: float
        datatype_rs: double
      low_price:
        size: 11
        datatype_py: float
        datatype_rs: double
      accumulated_trade_volume:
        size: 12
        datatype_py: int
        datatype_rs: i32
      accumulated_trade_value:
        size: 22
        datatype_py: float
        datatype_rs: double
      trade_type:
        size: 1
        datatype_py: decode_side
        datatype_rs: String
      lp_holding_quantity:
        size: 15
        datatype_py: int
        datatype_rs: i64
      l1askprice:
        size: 11
        datatype_py: float
        datatype_rs: double
      l1bidprice:
        size: 11
        datatype_py: float
        datatype_rs: double
      system_datetime:
        size: 19
        datatype_py: int
        datatype_rs: i64
```
Each trade message contains `trade_type` field which can be a `BUY`, `SELL`, or `AUCTION`. When running our trading system, it is imperative that our algorithm check opening trae `AUCTION` message since the regular trading hour begins after that message. These messages do not come exactly at `09:00:00` in the morning but rather at any time between `09:00:00.0` and `09:00:01.0`. All messages received before the opening trade message pertain to the opening cross, therefore, should not be used after the opening cross. 


### Trade, Marketdepth, Trade&Marketdepth, and Board&Marketdepth Messages
KRX UDP realtime data provides orderbook of depth 5 and 10. ETP and equity orderbooks have depth of 10, and derivative orderbooks have depth of 5. However, equity futures have orderbook depth of 10. Derivative orderbooks contain number of orders at a given price and ETP orderbook data contains the quantity of sitting orders made by liquidity providers(LP) in addition to the total quantity. 

Furthermore, there are four differnet types of messages that contain trade or marketdepth data: trade message (code **A3**), marketdepth message (code **B6** and **B7**), trade&marketdepth message (code **G7**) and board&marketdepth message (code **R1**). These messages are crucial to traders who rely on price movement and trade statistics. Below is a brief summary of these messages:
* Trade Message (**A3**): contains trade price and trade volume of a given security
* Marketdepth Message (**B6** and **B7**): contains orderbok of depth 5 or 10 depending on the type of security. LP quantity is also provided for ETPs. 
* Trade & Marketdepth (**G7**): contains trade price and trade volume data in addition to orderbook data
* Board & Marketdepth (**R1**): contains board event and orderbook data. Board event contains information about the market hours (e.g. regular trading hours, post-market trading hours, etc). 


### Koscom Messages
Koscom is a financial IT company whose parent company is the Korean stock exchange (KRX). Koscom also disseminates messages pertaining to exchange traded products (ETPs). Below are some messages that are often used by traders:
* ETN IIV message
* ETN Divergence message
* ETF PDF message

Specifications of Koscom messages are also included in the attached file.

[Attached file](/assets/codes/krx.yaml) 
