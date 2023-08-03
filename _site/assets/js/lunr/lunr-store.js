var store = [{
        "title": "Hahn and Jordan Decomposition Theorems",
        "excerpt":"Here’s a complete proof of Hahn decomposition theorem and Jordan Decomposition theorem.            ","categories": ["math"],
        "tags": ["measure theory","hahn decomposition theorme","jordan decomposition theorem","real analysis"],
        "url": "/math/hahn-jordan-decomposition/",
        "teaser": null
      },{
        "title": "Hausdorff's maximality theorem (zorn's lemma)",
        "excerpt":"Hausdorff’s maximality theorem (or Zorn’s lemma) is used often in graduate level real analysis course. Because the proof is a bit convoluted, most courses use it without proving it and professors usually direct us to the proof in Rudin’s real and complex analysis. There is a two page appendix that...","categories": ["math"],
        "tags": ["set theory","zorn's lemma","hausdorff's maximality theorem","real analysis"],
        "url": "/math/hausdorffs-maximality-theorem/",
        "teaser": null
      },{
        "title": "MOPO - Model-based Offline Policy Optimization",
        "excerpt":"In this post I will provide proofs for some lemmas and theorems in model-based offline policy optimization. This post doesn’t provide different proofs but rather a complete proof without omission so that readers like myself can follow the proof easily. I will assume that reader has already read the paper....","categories": ["reinforcement learning"],
        "tags": ["reinforcement learning","offline","model-based"],
        "url": "/reinforcement%20learning/mopo-model-basd-policy-optimization/",
        "teaser": null
      },{
        "title": "What is the definition of continuity?",
        "excerpt":"When I first studied real analysis, the definition of continuity was clear but there were just so many of them. I took some time to list as many definition of continuity as I could, and provide some observations on why we need so many definitions and how they are different....","categories": ["math"],
        "tags": ["continuous"],
        "url": "/math/continuity-definitions/",
        "teaser": null
      },{
        "title": "on- and off-policy? online and offline reinforcement learning?",
        "excerpt":"For those who are first learning reinforcement learning, the term on-policy and off-policy (and offline learning) can be quite daunting (and mostly annoying). Here we outline what they mean, how they are different, and how conceptually simple they are. On-policy The term on-policy, at least to me, seems to be...","categories": ["machine-learning"],
        "tags": ["reinforcement learning","on-policy","off-poliyc","online reinforcement learning","offline reinforcement learning"],
        "url": "/machine-learning/on-off-online-offline-rl/",
        "teaser": null
      },{
        "title": "What is a \"small\" set - measure theoretic and topological approach",
        "excerpt":"The notion of “smallness” in measure theory is pretty clear - when the set has measure $0$, then we can treat is as a small set, or a set with no mass. This is intuitive if we use a Lebesgue measure, but for other measures or distributions, this is not...","categories": ["math"],
        "tags": ["measure theory","topology","Baire category theorem"],
        "url": "/math/small-set-two-approaches/",
        "teaser": null
      },{
        "title": "Cross Sectional Variation of Intraday Liquidity, Cross-Impact and their Effect on Portfolio Execution",
        "excerpt":"In this post, I will share the results of my implementation of Cross-Sectional Variation of Intraday Liquidity, Cross-Impact, and their effect on Portfolio Execution. The key idea of this paper is that instead of a separable execution strategies such as VWAP, it is better to execute portfolio of orders in...","categories": ["finance"],
        "tags": ["portfolio execution","liquidity","optimal execution"],
        "url": "/finance/cross-sectional-variation-of-intraday-liquidity/",
        "teaser": null
      },{
        "title": "Sum of Cauchy sequence is not Cauchy",
        "excerpt":"Today I was asked whether sum of two convergent sequences converges. This can be trivial if we are dealing with $\\mathbb{R}$ using $|\\cdot|$ as our metric. But can we say this for every metric function? It turns out, that’s not the case, and here we provide a counterexample. Proof To...","categories": ["math"],
        "tags": ["Cauchy Sequence","Convergence","Monotone Convergence Theorem for sequences"],
        "url": "/math/sum-of-cauchy-not-cauchy/",
        "teaser": null
      },{
        "title": "SIP (CTA and UTP Plan)",
        "excerpt":"Terminologies: CTA: Consolidated Tape Association UTP: Unlisted Trading Privileges CTS: Consolidated Tape System CQS: Consolidated Quote System UTDF: UTP Trade Data Feed UQDF: UTP Quote Data Feed Tape A: NYSE listed securities Tape B: NYSE Arca and Amex listed securities Tape C: Nasdaq listed securities FINRA: Financial industry regulatory authority...","categories": ["finance"],
        "tags": ["finance","CTA","UTP","SIP","CTS","CQS","UTDF","UQDF"],
        "url": "/finance/sip-cta-utp/",
        "teaser": null
      },{
        "title": "Unique security Identifiers",
        "excerpt":"Terminologies: ISIN: international securities identification number CUSIP: Committee on Uniform Security Identification Procedures SEDOL: Stock Exchange Daily Official List RIC: Reuters Instrument Code There are many ways to uniquely identify a security but most will use ISIN (since it’s an expansion of SEDOL and CUSIP, which we will discuss more...","categories": ["finance"],
        "tags": ["isin","cusip","ticker symbol","ric","finance"],
        "url": "/finance/unique-security-identifier/",
        "teaser": null
      },{
        "title": "US Market Data (Part 1)",
        "excerpt":"Terminlogies: L1: Level 1 L2: Level 2 L3: Level 3 OLD: Order Level data LOB: Limit order book Unnormalized market data Unnormalized market data simply means that market data from different exchanges retain its original format. For instance, Nadsaq may send trade data with the following format: ____________________________ | |...","categories": ["data"],
        "tags": ["order level data","L1 data","L2 data","L3 data","limit order book"],
        "url": "/data/US-market-data-part1/",
        "teaser": null
      },{
        "title": "US Market Data (Part 2)",
        "excerpt":"US Bats (PITCH Feed handler) Bats PITCH feeds publish real-time full depth-of-book order and execution messages on primary and secondary UDP multicast channels during the trading hours. There are three types of feeds: Bats PITCH equities feed, Bats PITCH options feed, and Bats PITCH complex feed. Bats PITCH equities feed...","categories": ["data"],
        "tags": ["data science","data","finance"],
        "url": "/data/US-market-data-part2/",
        "teaser": null
      },{
        "title": "mmap RAII",
        "excerpt":"There are many ways to share data between processes. The most intuitive way is probably using a queue. In fact, I’ve used queues like ZeroMq when establishing communication between processes. They are off the shelf queue library that supports pretty much all langauges that it is almost language agnostic. If...","categories": ["c++"],
        "tags": ["mmap","raii","c++"],
        "url": "/c++/mmap-raii/",
        "teaser": null
      },{
        "title": "Snowflake and UDFTs",
        "excerpt":"Recently I had to do some analysis on a large dataset and sql couldn’t cut it. So I had to resort using user defined function. Snowflake provides user-defined table functions(UDFTs) in four different languages, of which python seemed the easiest to me. However, it turns out python UDFTs can be...","categories": ["database"],
        "tags": ["database","snowflake","python","javascript"],
        "url": "/database/snowflake-udft/",
        "teaser": null
      },{
        "title": "Managing DB with source code generator",
        "excerpt":"We often write redundant codes. I personally had to write a parser for different market data protocols. This is not only tedious but also error prone. One way to tackle this problem is to normalize all data into a single in-house protocol. However, if there is a new protocol that...","categories": ["database"],
        "tags": ["database","mako","sql","mako"],
        "url": "/database/managing-db-with-mako/",
        "teaser": null
      },{
        "title": "KRX UDP Data and Market Microstructure",
        "excerpt":"Korean Stock Exchange (KRX) is the only securities exchange in South Korea. Equities and ETPs get traded in Seoul while futures, options, and other derivatives get traded in Busan (hence, there exists an opportunity for latency arbitrage). To gain a speed advantage, lots of firms place their trading engines near...","categories": ["finance"],
        "tags": ["market microstructure","krx","udp"],
        "url": "/finance/krx-udp-data-and-market-microstructure/",
        "teaser": null
      },{
        "title": "Koscom NAV and iNAV",
        "excerpt":"The net asset value of an ETF is computed by dividing the total value of the ETF’s underlying assets by the number of outstanding shares: \\[\\text{nav} = {\\text{cash} + \\sum \\text{assets} \\over \\text{number of oustanding shares}}\\] The calculation is quite easy but getting the right data can be a hassle....","categories": ["finance"],
        "tags": ["python","etf","nav"],
        "url": "/finance/koscom-nav-and-inav/",
        "teaser": null
      },{
        "title": "ELW and implied volatility (IV)",
        "excerpt":"There are no individual stock options in the Korean stock exchange, a stark contrast to the US market. However, Korean financial firms provide a product called ELW which is almost identical to individual stock options. Hence we will treat ELW like options and generate a volatility curve from both call...","categories": ["finance"],
        "tags": ["elw","krx","implied volatility","iv","volatility"],
        "url": "/finance/krx-elw-iv-rv/",
        "teaser": null
      },{
        "title": "Scalping",
        "excerpt":"There are various types of securities that we can scalp - corporate stocks/bonds, equity futures, index futures, equity options, index options and so on. For this tutorial, we will be looking at KOSDAQ150 futures. KOSDAQ150 index is composed of 150 KOSDAQ-listed stocks where the constituents are selected based on the...","categories": ["finance"],
        "tags": ["scalping","hft","graph"],
        "url": "/finance/scalping/",
        "teaser": null
      },{
        "title": "Arbitrage",
        "excerpt":"In our previous post, we worked with KOSDAQ150 futures. Here we will be doing the same thing with KOSPI200 futures and Mini KOSPI200 futures. Similar to the US market, mini futures contracts require less margin to trade. KOSPI200 contract has a multiplier of 250000 while Mini KOSPI200 contract has a...","categories": ["finance"],
        "tags": ["arbitrage","hft","kospi200 futures","mini kospi200 futures"],
        "url": "/finance/arbitrage/",
        "teaser": null
      }]
