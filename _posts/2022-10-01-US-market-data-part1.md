---
title: US Market Data (Part 1)
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
