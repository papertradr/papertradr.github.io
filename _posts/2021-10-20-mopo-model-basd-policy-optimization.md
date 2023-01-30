---
title: MOPO - Model-based Offline Policy Optimization
category: reinforcement learning
tags: 
    - reinforcement learning
    - offline
    - model-based
mathjax: true
comments: true
layout: single
classes: wide
toc: false
published: false
---


In this post I will be discussing model-based offline policy optimization, and fill in the missing proofs. 

The paper claims that it is importnat for offline reinforcement learning algorithms to leave data support and learn better policy:
1. Most provided batch data are suboptimal in its state-action coverage
2. The target task can be different from the tasks performed in the batch data
So the paper addresses an offline reinforcement learning algorithm that generalized beyond the state action support of the offline dataset. 
