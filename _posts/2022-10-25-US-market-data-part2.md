---
title: US Market Data (Part 2)
category: data
tags:
    - data science
    - data
    - finance
mathjax: false
comments: true
toc: false
layout: single
classes: wide
published: true
---

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

## Montreal Exchange (MX) feed handler
MX publish data via MX's SOLA HSVF UDP Multicast feed. 

## OTC market



# Europe
## Aquis Stock Exchange (AQSE)
Aquis operates an exchange for the trading of European equities. 
It seems comparatively smaller than other exchanges.

## Eurex and Xetra (EOBI(Enhanced Order book interface) handler)
Eurex is owned by Deutsche Borse AG(German Bourse), Xetra is operated by the Frankfurt Stock Exchange, and its underlying trading technology was based on that of the Eurex exchange. Xetra data is used to calculate the DAX, the German share index.

# Asia

## FLEX Full feed handler (Japan)
The FLEX Full feed pubish real time data which includes complete book market data from the Tokyo Stock Exchange (TSE), Sapporo Stock Exchange (SSE), Nagoya Stock Exchange (NSE), and the Fukuoka Stock Exchange (FSE). The TSE group is part of the larger Japan Exchange Group (JPX). 

## HKFE (Hong Kong Futures Exchange feed handler)

## Hong Kong Securities Exchange (HKSE feed handler)

## TAIFEX feed handler (TAIWAN)
TAIFEX publish real-time market data.

[1]: https://www.nyse.com/publicdocs/nyse/data/NYSE_Symbology_Spec_v1.0c.pdf
