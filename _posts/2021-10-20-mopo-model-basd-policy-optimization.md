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

In this post I will be discussing [model-based offline policy optimization][1], and fill in the missing proofs. I will assume that the reader has already perused the paper beforehand. 

The paper claims that it is important for offline reinforcement learning algorithms to leave data support and learn better policy:
1. Most provided batch data are suboptimal in its state-action coverage
2. The target task can be different from the tasks performed in the batch data
Hence the paper suggests an offline reinforcement learning algorithm that can be generalized beyond the state action support of the offline dataset. 

Before we dive into the proofs, let's list some notations:
* MDP $M = (\mathcal{S}, \mathcal{A}, T, r, \mu_0, \gamma)$
* MDP $\widehat{M} = (\mathcal{S}, \mathcal{A}, \widehat{T}, r, \mu_0, \gamma)$ 

The key idea in the paper is lemma 4.1:
> **Lemma 4.1** (Teloscoping lemma). Let $M$ and $\hat{M}$ be two MDPs with the same reward function $r$, but different dynamics $T$ and $\hat{T}$ respectively. Let $G^{\pi}_{\widehat{M}} (s,a) := \mathbb{E}_{s' \sim \widehat{T}(s,a)} [ V_M^\pi (s')] - \mathbb{E}_{s' \sim T(s,a)} [ V_M^\pi(s')]$. Then,
$$\eta_{\widehat{M}}(\pi) - \eta_M(\pi) = \gamma \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ G^\pi_{\widehat{M}} (s,a) \Big].$$
As an immediate corollary, we have
$$\eta_M(\pi) = \mathbb{E}_{(s,a)\sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma G_{\widehat{M}}^\pi (s,a) \Big] \le \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma |G^\pi_{\widehat{M}} (s,a)| \Big]$$

As the paper points out, the quantity $G_{\hat{M}}^\pi (s,a)$ plays the key role of **linking** the estimation error of the dynamics and the estimation error of the return. $G_{\hat{M}}^\pi (s,a)$ is the difference in average returns between MDP with dynamics $\widehat{T}$ and $T$. 

The proof of lemma 4.1 is outlined in the appendix; here we 

[1]: https://arxiv.org/pdf/2005.13239.pdf