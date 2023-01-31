---
title: Nasdaq Totalviewitch Fundamentals
category: finance
tags: 
    - nasdaq
    - totalviewitch
mathjax: true
comments: true
layout: single
classes: wide
toc: false
published: false
---

# Nasdaq Orders

## Order Life cycle in Nasdaq

Nasdaq provides its historical trading data through its proprietary ITCH direct data-feed protocol. These messages come in binary format and need to be parsed accordingly. The details of the format are specified in their documentation. There are many different types of messages but we are primarily interested in the following types: add order messages (A), add order with MPID messages (F), replace order messages (U), execution messages (E), execution with price messages (C), partial cancellation messages (X), and delete order messages (D).


##Order Priorities in Nasdaq Exchange

Order priorities goes like this: Price -> Time -> Displayabilty. 

## Price

Price priority is pretty straightforward conceptually - any order with a better price will get executed first. For instance, an limit order to sell at $14.00 is obviously going to get matched first than a limit order to see at $14.10. However, there are some different order types that make price priority a bit confusing.

**Post-only orders** Post-Only Orders are evaluated at the time of entry with respect to locking or crossing other orders as follows: if a Post-Only Order would lock or cross an order on the System, the order will be re-priced to $.01 below the current low offer (for bids) or above the current best bid (for offers) and displayed by the System at one minimum price increment below the current low offer (for bids) or above the current best bid (for offers).

For instance, if the current best offer is $14.00, a post-only buy order at $14.00 will be displayed as $13.99. When it gets executed, the seller will sell at $13.99 but the buyer will get $14.00. The motivation behind this is to give post-only orders priority for reducing the spread and creating liquidity in the market. The $.01 is often called the maker fee (or market maker rebate).

One thing to note is that when a new limit order comes in at $13.99, then that limit order gets priority over the post only order (as shown in the figure). It seems that the rationale behind this is that post-only orders cost Nasdaq $0.01 per share while the limit order doesn't cost Nasdaq anything. Hence, the limit order gets the priority. 

## Time


## Displayability

NASDAQ order types can be separated into two major types: displayable and non-displayable. Within displayable orders, some orders get disseminated (i.e. we know that order was submitted via ITCH messages) and some orders do not get disseminated (i.e. we do not know if the order was submitted even though it is displayable).

Displayable

Disseminated: these are orders that we can track via NASDAQ ITCH messages (i.e. limit orders)

Non-disseminated: these are orders that we cannot track even though they are technically” displayable orders. All cross-type orders are non-disseminated displayable orders (also called auction orders). We can access these orders via NOII messages which come in 1(?) second interval before the cross. Note that since they are technically displayable, when they get disseminated after the cross, they are placed based on their order reference number (assuming that the order reference number is given in incrementally)

Non-displayable: these are orders that we cannot track. However, they have less priority than displayed orders.

Note that if one wishes to convert non-displayable order to displayable, one has to cancel it and then submit a new displayable order.


## Classification of Security on Nasdaq

There are more than 3,300 company listings on Nasdaq but in the Nasdaq ITCH dataset, there are 11,238 listings. The discrepancy is due to other derivatives that are traded on the Nasdaq exchange. For instance, ETFs or REITs are also traded on Nasdaq exchange.

Fortunately, Nasdaq stock screener, we can get a list of stocks by their market cap, analyst rating, sector, etc. Different types of stocks may behave differently due to the liquidity and market participants - for instance, the way people trade a mega cap stock like Apple (AAPL) can differ significantly from a medium cap stock such as DraftKings (DKNG). Additionally, different types of securities may exhibit different properties - a leveraged ETF may be traded differently from common stocks.

Here we list some ways to classify stock types:

Market cap (e.g. Nano, Micro, Small, Medium, Large, Mega)

Nasdaq Stock Market Tier

Security type (e.g. common stock, ETFs, leveraged ETFs, etc)

Price range (e.g. < $10, <$100, <$200, <$500, <$1000, etc)

Sector (e.g. Basic industries, Capital goods, Technology, etc)

Volume (e.g. low volume stock, high volume stock)

We will focus on common stocks only and classify them by the market cap (since that data is easily available via Nasdaq stock screener). In the future, we may further classify the stocks by their price or sector.


## Nasdaq Stock Market Tiers Classification

(This is Nasdaq’s internal classification method which may be of no use to us. However, since it is an official way Nasdaq classifies their company listings, we explain what it is for the sake of completeness.)

The Nasdaq Stock Market has three distinctive tiers: The Nasdaq Global Select Market, The Nasdaq Global Market and The Nasdaq Capital Market. Applicants must satisfy certain financial, liquidity and corporate governance requirements to be approved for listing on any of these market tiers.

Nasdaq Global Select Market: The Nasdaq Global Select Market has the highest initial listing standards of any exchange in the world. It is a mark of achievement and stature for qualified companies.

Nasdaq Global Market: The Nasdaq Global Market lists companies with an overall global leadership and international reach with their products or services.

Nasdaq Capital Market: Nasdaq Capital Markets are focused on its core purpose for those companies listed -- capital raising.
