---
title: Cross Sectional Variation of Intraday Liquidity, Cross-Impact and their Effect on Portfolio Execution
category: finance
tags: 
    - portfolio execution
    - liquidity
    - optimal execution
mathjax: true
comments: true
layout: single
classes: wide
toc: false
published: false
---

In this post, I will share the results of my implementation of [Cross-Sectional Variation of Intraday Liquidity, Cross-Impact, and their effect on Portfolio Execution][1]. The paper suggests that instead of a separable execution strategies such as VWAP, it is better to execute portfolio of orders in a coupled manner due to cross-impact and intraday variation. 

## Data
The paper analyzed 459 stocks for 241 days exclusing FOMC/FED announcement days using Trade and Quote database. For our experiment, we used Nasdaq's totalviewitch data from October 2021 to December of 2021. We looked at 147 securities in the S&P500 and are primarily listed in the Nasdaq exchange.


## Preliminaries
Here we will be measuring the following intraday metrics:
$$
\begin{align*}
&\overline{{\text{DVol}}}_{it} := {1 \over D} \sum_{d=1}^D \text{DVol}_{idt}\\
&\text{VolAlloc}_{it} := {\overline{\text{DVol}}_{it} \over \sum_{s=1}^T \overline{\text{DVol}}_{is}}\\
&\text{AvgVolAlloc}_{t} := {1 \over N} \sum_{i=1}^N \text{VolAlloc}_{it}\\
&\text{Correl}_{ijt} := { \sum_{d=1}^D (\text{DVol}_{idt} - \overline{\text{DVol}}_{it}(\text{DVol}_{jdt} - \overline{\text{DVol}}_{jt}) \over \sqrt{ \sum_{d=1}^D (\text{DVol}_{idt} - \overline{\text{DVol}}_{it})^2 - \cdot \sum_{d=1}^D (\text{DVol}_{jdt} - \overline{\text{DVol}}_{jt})^2}}  \\
& \text{AvgCorrel}_t := {1 \over N(N-1)} \sum_{i \neq j} \text{Correl}_{ijt}
\end{align*}
$$

## Average Volume Allocation
Let us define the average volume allocation as 
$$
\begin{align*}
&\overline{{\text{DVol}}}_{it} := {1 \over D} \sum_{d=1}^D \text{DVol}_{idt}\\
&\text{VolAlloc}_{it} := {\overline{\text{DVol}}_{it} \over \sum_{s=1}^T \overline{\text{DVol}}_{is}}\\
&\text{AvgVolAlloc}_{t} := {1 \over N} \sum_{i=1}^N \text{VolAlloc}_{it}\\
\end{align*}
$$

<figure>
  <img src="/assets/images/cross-sectional-variation/avgvolalloc.png" style="width:100%;height: auto"/>
</figure>

### Average Correlation
Let us define Average correlation as 
$$
\begin{align*}
&\text{Correl}_{ijt} := { \sum_{d=1}^D (\text{DVol}_{idt} - \overline{\text{DVol}}_{it}(\text{DVol}_{jdt} - \overline{\text{DVol}}_{jt}) \over \sqrt{ \sum_{d=1}^D (\text{DVol}_{idt} - \overline{\text{DVol}}_{it})^2 - \cdot \sum_{d=1}^D (\text{DVol}_{jdt} - \overline{\text{DVol}}_{jt})^2}}  \\
& \text{AvgCorrel}_t := {1 \over N(N-1)} \sum_{i \neq j} \text{Correl}_{ijt}
\end{align*}
$$

<figure>
  <img src="/assets/images/cross-sectional-variation/avg_corr.png" style="width:100%;height: auto"/>
</figure>

### Decomposition of average volume allocation 
<figure>
  <img src="/assets/images/cross-sectional-variation/alpha_beta.png" style="width:100%;height: auto"/>
</figure>
<figure>
  <img src="/assets/images/cross-sectional-variation/avgvolalloc_alpha_beta.png" style="width:100%;height: auto"/>
</figure>
<figure>
  <img src="/assets/images/cross-sectional-variation/single_vs_index.png" style="width:100%;height: auto"/>
</figure>
<figure>
  <img src="/assets/images/cross-sectional-variation/single_vs_index_volume.png" style="width:100%;height: auto"/>
</figure>







[1]: https://arxiv.org/pdf/1811.05524.pdf
