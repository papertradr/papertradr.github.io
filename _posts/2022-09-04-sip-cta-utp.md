---
title: SIP (CTA and UTP Plan)
category: finance
tags:
    - finance
    - CTA
    - UTP
    - SIP
    - CTS
    - CQS
    - UTDF
    - UQDF
mathjax: false
comments: true
toc: false
layout: single
classes: wide
published: true
---

Terminologies:
* CTA: Consolidated Tape Association
* UTP: Unlisted Trading Privileges
* CTS: Consolidated Tape System
* CQS: Consolidated Quote System
* UTDF: UTP Trade Data Feed
* UQDF: UTP Quote Data Feed
* Tape A: NYSE listed securities
* Tape B: NYSE Arca and Amex listed securities
* Tape C: Nasdaq listed securities
* FINRA: Financial industry regulatory authority

**tl;dr** CTA distributes trade(CTS) and quote(CQS) messages for tape A (i.e. NYSE listed securities) and tape B (i.e. NYSE Arca and Amex). UTP distributes trade(UTDF) and quote(UQDF) messages for tape C (i.e. Nasdaq listed securities) 


When I first entered finance, one of the few jargons that confused me was SIP, then came CTA and UTP. These acronyms are thrown around by those who work in finance all the time and while I kind of knew what they were, I never dug deep into them until recently. Here is all you need to know about them:

## CTA (Consolidated Tape Association) 
When someone says CTA, they are referring to the **association** that oversees the consolidation and distribution of NYSE listed securities (Tape A) and NYSE Arca & Amex listed securities (Tape B). 

## UTP (Unlisted Trading Privileges) Plan
Similary, when someone says UTP, they are referring to the **association** that oversees the consolidation and distribution of Nasdaq listed securities (Tape C).

## CTS (Consolidated Tape System) and CQS (Consolidated Quote System)
CTS and CQS are data feed provided by the CTA.
CTS consolidates and distributes Tape A and Tape B trades.
CQS consolidates and distributes Tape A and Tape B quotes.

## UTDF (UTP trade data feed) and UQDF(UTP quote data feed)
UTDF and UQDF are data feed provided by the UTP Plan. 
UTDF consolidates and distributes Tape C trades.
UQDF consolidates and distributes Tape C quotes.

# SIP (securities information processor)
SIP refers to any system that consolidates and distributes market data to public. In the U.S., there are two sips: CTA and UTP Plan. 

In addition to trades and quotes, both SIPs provide additional data which include
- National best bid and offer (NBBO)
- Limit up and down (LULD) price bands
- Trading halts 
- IPOs
- Financial status

Here's a nice image from [Peter Stacho][1]:

<figure>
  <img src="/assets/images/sip.jpeg" style="width:120%;height: auto"/>
  <figcaption>source (https://polygon.io/blog/understanding-the-sips/)</figcaption>
</figure>

[1]: https://polygon.io/blog/understanding-the-sips/
