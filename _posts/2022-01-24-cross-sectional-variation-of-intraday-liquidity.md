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

## Setting up Parameters

```python
from enum import Enum

class NasdaqMessageType(Enum):
    ADD = 0
    DEL = 1
    CANCEL = 2
    REPLACE = 3
    EXEC = 4
    EXEC_PRICE = 5
    CROSS_TRADE = 6
    NON_CROSS_TRADE = 7

"""
We set start time to 9:30, end time to 16:00.
Each interval is 5 minutes
"""
_min_to_ns = lambda x: int(x * 60 * 1e9)

INTERVAL_MIN = 5
INTERVAL_NS = _min_to_ns(INTERVAL_MIN)
START_TIME_MIN = 9 * 60 + 35 # 9:35
START_TIME_NS = _min_to_ns(START_TIME_MIN)
END_TIME_MIN = 16 * 60 # 16:00 or 4pm
END_TIME_NS = _min_to_ns(END_TIME_MIN)
T = (END_TIME_NS - START_TIME_NS) // INTERVAL_NS 
interval_tuples = [(START_TIME_NS + i*INTERVAL_NS, START_TIME_NS + (i+1)*INTERVAL_NS) 
                   for i in range(T)]

TICKER_SYM = lambda x: x.split('.')[-3].split('/')[-1]
DATE_FROM_PATH = lambda x: x.split('/')[2]

MONTHS = ["10", "11", "12"]
YEARS = ["21"]
itch_data_dirs = []
for year in YEARS:
    for month in MONTHS:
        pattern = re.compile(f"S{month}[0-9][0-9]{year}-v50$")
        itch_data_dirs += sorted(["./data/" + x + "/"
                                 for x in os.listdir("./data") if x and pattern.match(x)])
itch_data_dirs.remove("./data/S112621-v50/")
D = len(itch_data_dirs)
print(f"\tNumber of days: {D}")
print(itch_data_dirs)
```


## Data
The paper analyzed 459 stocks for 241 days exclusing FOMC/FED announcement days using Trade and Quote database. For our experiment, we used Nasdaq's totalviewitch data from October 2021 to December of 2021. We looked at 147 securities in the S&P500 and are primarily listed in the Nasdaq exchange.

```python
def get_daily_vol_alloc(data_dir, stock_symbols):
    zst_paths = [f"{data_dir}{sym}.bin.zst" for sym in stock_symbols]
    dvols_day = np.zeros((N, T))
    for i, zst_path in enumerate(zst_paths):
        messages = load_actions(Path(zst_path))
        
        # find the trade volume at each interval
        interval_volumes = np.zeros((1, T))
        for j, (interval_start_ns, interval_end_ns) in enumerate(interval_tuples):
            interval_messages = messages[
                # get messages inside the interval
                (messages[:, 1] < interval_end_ns) & (messages[:, 1] >= interval_start_ns)
                # get execute (execute with price) messages only
                & ((messages[:, 0]==NasdaqMessageType.EXEC.value) 
                       | (messages[:, 0]==NasdaqMessageType.EXEC_PRICE.value))]
            interval_volumes[:, j] = (np.sum(interval_messages[:, 3]))

        dvols_day[i, :] = interval_volumes
        assert np.sum(interval_volumes) > 0, \
                f"{TICKER_SYM(zst_path)}'s total volume is 0! {interval_volumes}"
    
    return dvols_day


dvols = np.zeros((D, N, T))
print(dvols.shape)
for i, data_dir in enumerate(itch_data_dirs):
    print(f"parsing {data_dir}")
    pkl_filename = f"./data/{DATE_FROM_PATH(data_dir)}_{MARKET_CAP}.pkl"
    if Path(pkl_filename).exists():
        print(f"{pkl_filename} exists, moving onto next date")
        with open(pkl_filename, "rb") as pf:
            data = pickle.load(pf)
            dvols[i, :, :] = data["dvols_day"]
        continue

    dvols_day = get_daily_vol_alloc(data_dir, stock_symbols)
    dvols[i, :, :] = dvols_day

    with open(pkl_filename, "wb") as pf:
        pickle.dump({"dvols_day": dvols_day}, pf)
```

## Average Volume Allocation

```python
bar_dvol = np.mean(dvols, axis=0)
vol_alloc = bar_dvol / np.sum(bar_dvol, axis=1, keepdims=True)
avg_vol_alloc = np.mean(vol_alloc, axis=0)
```

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

```python
print((dvols-bar_dvol).shape)
correl = np.zeros((T, N, N))
for t in range(T):
    correl_num_t = np.array([(dvols[d, :, t] - bar_dvol[:, t]).reshape(-1, 1) 
                             @
                             (dvols[d, :, t] - bar_dvol[:, t]).reshape(-1, 1).T
                            for d in range(D)])
    correl_num_t = np.sum(correl_num_t, axis=0)
    
    var = np.array([np.square(((dvols[d, :, t]+1e-15)-bar_dvol[:, t]).reshape(-1, 1)) 
                           for d in range(D)])
    
    var = np.sum(var, axis=0)
    correl_denom_t = np.sqrt(var @ var.T)
    correl_t = correl_num_t / (correl_denom_t)
    correl[t, :, :] = correl_t
    
avg_correl = (1 / (N * (N-1))) * np.sum(correl, axis=(1, 2))
```

<figure>
  <img src="/assets/images/cross-sectional-variation/avg_corr.png" style="width:100%;height: auto"/>
</figure>

### Decomposition of average volume allocation 

```python
from scipy.optimize import root, least_squares 
import functools
def func(p):
    theta = p[0]
    print(theta)
    # all RHS have to be 0
    e = [(1-avg_correl[i]) * avg_vol_alloc[i] / ((1-2*avg_correl[i])*theta + avg_correl[i])\
        for i in range(T)]
    s = functools.reduce(lambda a, b: a + b, e)
    f = theta / (1 - theta) * s - 1
    return f

params = [0.25] # theta
sol = root(func, params)
theta = sol.x
print(f"theta: {theta}")
alpha = (1/(1-theta))* (1-avg_correl) * avg_vol_alloc * theta /\
            ((1-2*avg_correl)*theta + avg_correl)
beta = (avg_vol_alloc - (1-theta) * alpha) / theta
```

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
