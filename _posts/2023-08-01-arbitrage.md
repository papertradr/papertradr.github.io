---
title: Arbitrage
category: finance
tags:
    - arbitrage
    - hft
    - kospi200 futures
    - mini kospi200 futures
mathjax: true
comments: true
layout: single
classes: wide
published: true
---

In our previous post, we worked with KOSDAQ150 futures. Here we will be doing the same thing with KOSPI200 futures and Mini KOSPI200 futures. 

Similar to the US market, mini futures contracts require less margin to trade. KOSPI200 contract has a multiplier of 250000 while Mini KOSPI200 contract has a multiplier of 50000. So we only need to focus on creating an aggregated orderbook with Mini KOSPI200. 

This is in fact a lot easier than converting ETPs to futures price. The major difference between the two securities is the tick size - KOSPI200 futures has a tick size of 0.05 while Mini KOSPI200 futures has a tick size of 0.02. In fact, since the tick size of Mini KOSPI200 is smaller, we can say that the real best ask and bid prices of KOSPI200 futures contracts should be calculated with Mini KOSPI200 contracts. Aggregating them is as simple as combining the two orderbooks and modifying the quantity of order in the mini kospi200 orderbook by multiplying it by ${\text{KOSPI200 Mini Multiplier} \over \text{KOSPI200 Multiplier}}$. 

Similar to the previous post on KOSDAQ150 scalping, we create an upper channel and a lower channel between KOSPI200 futures and mini KOSPI200 futures. The resulting channels are shown below:
<figure>
  <img src="/assets/images/kospi200_vs_mini_kospi200_arb.png" style="width:120%;height: auto"/>
</figure>
You can see that there aren't many overlaps between the two channels, implying that the market is quite efficient, but not perfect. Let us zoom in on some of the areas where the upper channel goes below zero and where the lower channel goes above zero.

## Example 1
<figure>
  <img src="/assets/images/arb_1.png" style="width:120%;height: auto"/>
</figure>
We see that the lower channel goes above 0; below is the aggregated orderbook:
<figure>
  <img src="/assets/images/arb_1_1.png" style="width:120%;height: auto"/>
</figure>
We see a clear arbitrage opportunity: go long on mini kospi200 futures and short on kospi200 futures, yielding us 0.03 point profit.

## Example 2
<figure>
  <img src="/assets/images/arb_2.png" style="width:120%;height: auto"/>
</figure>
We see that the upper channel going below 0. The corresponding aggregated orderbook is:
<figure>
  <img src="/assets/images/arb_2_1.png" style="width:120%;height: auto"/>
</figure>
Here we go long on kospi200 futures and short on mini kospi200 futures for a 0.02 point profit. 

