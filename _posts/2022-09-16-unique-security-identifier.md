---
title: Unique security Identifiers
category: finance
tags:
    - isin
    - cusip
    - ticker symbol
    - ric
    - finance
mathjax: false
comments: true
toc: false
layout: single
classes: wide
published: true
---

**Terminologies:**
- ISIN: international securities identification number 
- CUSIP: Committee on Uniform Security Identification Procedures
- SEDOL: Stock Exchange Daily Official List
- RIC: Reuters Instrument Code

There are many ways to uniquely identify a security but most will use ISIN (since it's an expansion of SEDOL and CUSIP, which we will discuss more in this post). Here we list a few well known identifiers:

## Ticker
The most naive way to identify a security is by the ticker symbol – this is used to identify publicly traded shares of a particular stock on a given exchange.  
Most won't use the ticker symbol since it doesn't contain any information on where it is traded and what type of security it is. For instance, `AAPL` doesn't tell us whether we are referring to `AAPL` that is being traded in the U.S. or U.K. Additionally, we don't know if we are referring to `AAPL` stock or `AAPL` bond. 

## RIC
**Reuters instrument code** used in Refinitiv services to identify companies. Only Refinitiv products use it and no one else, but since Refinitiv is such a huge data service provider, you'll probably uses it at some point if you're in finance.

## SEDOL 
SEDOL stands for **Stock Exchange Daily Official List** – they are 7 characters in length, a 6 place alphanumeric code and a trailing check digit. 
These numbers are used to identify securities by the **London Stock Exchange**. 
SEDOLs serve as the **National Securities Identifying Number** for all securities in the U.K. therefore it is part of security's ISIN as well. 


## CUSIP
Similarly, CUSIP stands for **Committee on Uniform Security Identification Procedures** and contains 6, 8 or 9 digit alphanumeric code which identifies a North American equity. 
They are created by the American Banking Association and are operated by S&P Capital IQ.
Since CUSIPs are unique identifiers for U.S. securities, they are used as part of security's ISIN as well.

## ISIN
ISIN stands for **international securities identification number** and it is a **12-digit alphanumeric code that uniquely identifies a specific security globally**.
There are three parts to ISIN: (i) country code, (ii) numbers, and (iii) checksum. 
For securities in U.K., the number would be SEDOL while for U.S. securities, it is CUSIP.

Here's a simple diagram on how ISIN is generated from CUSIP:

<figure>
  <img src="/assets/images/cusip-to-isin.png" style="width:100%;height: auto"/>
  <figcaption>source (https://heald.ca/converting-cusip-6-cusip-8-and-cusip-9-to-isin-in-php/)</figcaption>
</figure>


 Most financial data providers, e.g. Thomson Reuters, Bloomberg, BvD, usually include an ISIN number.
