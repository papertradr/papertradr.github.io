---
title: US Market Data
category: data
tags:
    - order level data
    - L1 data
    - L2 data
    - L3 data
    - limit order book
mathjax: false
comments: true
toc: false
layout: single
classes: wide
published: true
---

**Terminlogies**:
- L1: Level 1
- L2: Level 2
- L3: Level 3
- OLD: Order Level data
- LOB: Limit order book


## Unnormalized market data
Unnormalized market data simply means that market data from different exchanges retain its original format. 
For instance, Nadsaq may send trade data with the following format:
```
 ____________________________
|        |       |          |
| ticker | price |  volume  |
|________|_______|__________|
```
while NYSE sends trade data as:
```
 _________________________
|        |        |       |
| ticker | volume | price |
|________|________|_______|
```

## Normalized market data
Normalized data will take data from different exchanges and make sure all of them have the same format. 
Using the above example, we can normalize the Nasdaq and NYSE data as follows:
```
 _________________________________________
|        |       |          |             |
| ticker | price |  volume  | exchange id |
|________|_______|__________|_____________|
```

## L1 Data 
**L1 data displays the best bid-offer-volume quotes**. This is often the national best bid and offer (NBBO). 
If we want L1 data from, for instance, Nasdaq, then we can subscribe to their service called Nasdaq Basic which consolidates and distributes best bid and offer (BBO) from all Nasdaq exchanges. 
If we want the national best bid and best offer (NBBO), then we can subscribe to the SIPs which will consolidate and distribute L1 data from all exchanges. 
Note that since SIPs need to consolidate from all exchanges as opposed to Nasdaq Basic which consolidates from Nasdaq exchanges only, there will be some discrepancy in latency. 


## L2 and L3 Data
**L2 and L3 data displays multiple bid-offer-volume prices**. 
This could be the top 5 best bid-offer-volume to full bid-offer-volume.
Unlike L1 data, each exchange distributes its own L2/L3 data, therefore, if we need a consolidated L2/L3 data, we need to subscribe to all exchanges and do the conslidation and normalization ourself. 
There are third party vendors (ICE, etc) that provide both normalized and unnormalized consolidated L2/L3 data.



## Order Level Data (OLD)
**Order level data contains every order messages - add order, cancel order, modify order, replace order - that can be used to construct a full depth orderbook and more**.
Similar to L2/L3 data, individual exchanges distribute its own order level data and if we wish to construct a consolidated orderbook, we need to get feed from all exchanges. Note that unlike L2/L3 data, not all exchanges have order level data. The big exchanges (e.g. Nasdaq, NYSE) provide order level data (e.g. totalview, openbook ultra)
There are third party vendors (e.g. Maystreet, Refinitiv, etc) that provide both normalized and unnormalized consolidated order level data.


# US
## Bats (PITCH Feed handler)
Bats PITCH feeds publish real-time full depth-of-book order and execution messages on primary and secondary UDP multicast channels during the trading hours. There are three types of feeds: Bats PITCH equities feed, Bats PITCH options feed, and Bats PITCH complex feed. 
- Bats PITCH equities feed supports **BZX, BYZ, EDGA and EDGX** exchanges 
- Bats PITCH options feed supports **BZX, EDGX, C1, and C2** option exchanges. 
- Bats PITCH complex feed supports the copmlex feed on **EDGX, C1, and C2** option exchanges.

## XDP feed (NYSE, ARCA, AMEX, National and Chicago exchanges)
The XDP feed handlers support **NYSE, NYSE Arca, NYSE National, and NYSE Chicago**. The feed publishes real-time full depth of book order and execution messages.

## Totalview (ITCH Feed handler)
The totalview feed handlers support **Nasdaq ITCH(total view), PSX ITCH(total view psx) and BX ITCH (total view bx)**. The feed publisehs real-time full depth of book order and execution messages on primary and secondary UDP multicast channels durin gtrading hours. The Nasdaq Totalview feeds provide information on NYSE, NYSE MKT, NYSE ARCA, BATS and NASDAQ listed symbols.

## IEX (IEX feed handler)
IEX exchange publishes real-time equities market data by the Investors Exchange(IEX) 

## CTA Data - CQS (consolidated quote system) and CTS (consolidated tape system)
Consolidated Tape Association (CTA) is reponsible disseminating level 1 trade and quote information in New York Stock Exchange (Tape A), NYSE Arca and NYSE Amex (Tape B). Unlisted Trading Privileges (UTP) plan is responsible for disseminating level 1 trade and quote information in Nasdaq (Tape C) listed securities traded on participating U.S. exchanges.
CQS (consolidated quote system) publishes real-time top-of-the-book quotes on multicast channels during tradin ghours of the exchanges contributing to the CTS/CQS feed. CQS publishes following information:
- **BBOQUOTE**
- **Feed Status**
- **LULD**
- **Market status**
- **NBBOQuote**
- **Product Status**

CTS (consolidated tape system) publishes trade/execution messages on multicast channels during trading hours of the exchanges contributing to the CTS/CQS feed.
- **Auction summary**
- **Feed Status**
- **Index Update**
- **LULD**
- **Market Status**
- **Product Statistics**
- **Product Status**
- **Trade**
- **Trade break**
- **Trade correction**

## UTP - UQDF (UTP Qutation data feed) and UTDF (UTP Trade data feed)
UTDF (UTP Trade data feed) contains
- **Auction Summary**
- **Feed Status**
- **Market Status**
- **Product Statistics**
- **Trade**
- **Trade Break**
- **Trade Correction**

UQDF (UTP Quote data feed) contains
- **BBQuote**
- **Feed Status**
- **Market Status**
- **NBBO Quote**
- **Product Status**

More about CTA and UTP can be found [here][1]

## Cboe Global Indices Feed (formerly CSMI)
Cboe Global indices feed market data delivers real-time index values on over 400 products. Featured values from CBOE include SPX and the VIX spot, Standard & Poor's / Down Jones, FTSE Russell, Ameribor, Gemini, Merrill Lynch, MIller Howard, MSCI, and Societe Generale.

## ICE iMpact (Intercontenental Exchange (ICE))
ICE iMpact feed handler publishes derivatives market data on the Intercontenental Exchange (ICE)'s iMpact multicast feed.

## MIAX Equities feed handler
MIAX's parent holding company, Miami International Holdings, Inc. (MIH), operates and manages Miami International Securities exchange, MIAX PEARL, MIAX Emerald, etc.

<!-- ## Montreal Exchange (MX) feed handler
MX publish data via MX's SOLA HSVF UDP Multicast feed. 
-->
<!-- ## OTC market -->

<!--
# Europe
## Aquis Stock Exchange (AQSE)
Aquis operates an exchange for the trading of European equities. 
It seems comparatively smaller than other exchanges.

## Eurex and Xetra (EOBI(Enhanced Order book interface) handler)
Eurex is owned by Deutsche Borse AG(German Bourse), Xetra is operated by the Frankfurt Stock Exchange, and its underlying trading technology was based on that of the Eurex exchange. Xetra data is used to calculate the DAX, the German share index.

# Asia

## FLEX Full feed handler (Japan)
The FLEX Full feed pubish real time data which includes complete book market data from the Tokyo Stock Exchange (TSE), Sapporo Stock Exchange (SSE), Nagoya Stock Exchange (NSE), and the Fukuoka Stock Exchange (FSE). The TSE group is part of the larger Japan Exchange Group (JPX). 
-->
<!-- ## HKFE (Hong Kong Futures Exchange feed handler)
<!--
## TAIFEX feed handler (TAIWAN)
TAIFEX publish real-time market data.
## Hong Kong Securities Exchange (HKSE feed handler) -->
-->

[1]: https://www.nyse.com/publicdocs/nyse/data/NYSE_Symbology_Spec_v1.0c.pdf
