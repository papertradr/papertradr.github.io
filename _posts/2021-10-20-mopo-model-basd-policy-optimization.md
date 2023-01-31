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
published: true
---

In this post I will provide proofs for some lemmas and theorems in [model-based offline policy optimization][1]. This post doesn't provide different proofs but rather a complete proof without omission so that readers like myself can follow the proof easily. I will assume that reader has already read the paper. Let's get started!

The paper claims that it is important for offline reinforcement learning algorithms to leave data support and learn better policy:
1. Most provided batch data are suboptimal in its state-action coverage
2. The target task can be different from the tasks performed in the batch data
Hence the paper suggests an offline reinforcement learning algorithm that can be generalized beyond the state action support of the offline dataset. 

Before we dive into the proofs, let's list some notations:
* MDP $M = (\mathcal{S}, \mathcal{A}, T, r, \mu_0, \gamma)$
* MDP $\widehat{M} = (\mathcal{S}, \mathcal{A}, \widehat{T}, r, \mu_0, \gamma)$ 
where $T$ is the ground truth dynamics of the environment and $\widehat{T}$ is the estimated dynamics from the batch dataset. 

The key idea in the paper is lemma 4.1:
> **Lemma 4.1** (Teloscoping lemma). Let $M$ and $\hat{M}$ be two MDPs with the same reward function $r$, but different dynamics $T$ and $\hat{T}$ respectively. Let $G^{\pi}_{\widehat{M}} (s,a) := \mathbb{E}_{s' \sim \widehat{T}(s,a)} [ V_M^\pi (s')] - \mathbb{E}_{s' \sim T(s,a)} [ V_M^\pi(s')]$. Then,
$$\eta_{\widehat{M}}(\pi) - \eta_M(\pi) = \gamma \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ G^\pi_{\widehat{M}} (s,a) \Big].$$
As an immediate corollary, we have
$$\eta_M(\pi) = \mathbb{E}_{(s,a)\sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma G_{\widehat{M}}^\pi (s,a) \Big] \le \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma |G^\pi_{\widehat{M}} (s,a)| \Big]$$

As the paper points out, the quantity $G_{\hat{M}}^\pi (s,a)$ plays the key role of **linking** the estimation error of the dynamics and the estimation error of the return. $G_{\hat{M}}^\pi (s,a)$ is the difference in average returns between MDP with dynamics $\widehat{T}$ and $T$. 

The proof of lemma 4.1 is outlined in the appendix which uses a very clever telescoping lemma trick; here's a simple proof of corollary for completeness:
$$
\begin{align*} 
\eta_M(\pi) &= \eta_{\widehat{M}}(\pi) - \gamma \bar{\mathbb{E}}_{(s,a) \sim \rho_{\widehat{T}}^\pi} \Big[ G_{\widehat{M}}^\pi(s,a) \Big] \\
&= \bar{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}}\Big[r(s,a) \Big] - \gamma \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ G_{\widehat{M}}^\pi (s,a) \Big] \\
&= \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[r(s,a) - \gamma  G_{\widehat{M}}^\pi (s,a)\Big] \\
&\ge \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[r(s,a) - \gamma  |G_{\widehat{M}}^\pi (s,a) |\Big]
\end{align*}$$

Later on the paper provides a lower bound on the true return in equation (7):
$$
\begin{align*} 
\eta_M(\pi) &\ge \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[r(s,a) - \gamma  |G_{\widehat{M}}^\pi (s,a) |\Big] \quad \because \text{corollary}\\
&\ge \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma c d_\mathcal{F}(\widehat{T}(s,a), T(s,a))\Big] \quad \because \text{(6)}\\
&\ge \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \gamma c \cdot \mu(s,a)\Big] \quad \because \text{assumption}\\
&= \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \lambda \cdot \mu(s,a)\Big] \quad \because \text{$\lambda = \gamma c$}\\
&= \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ \tilde{r}(s,a) \Big] \quad \because \quad \tilde{r}(s,a) = r(s,a) - \lambda \mu(s,a) \\
&=: \eta_{\tilde{M}} (\pi)
\end{align*}
$$

Now we come to the main theorem. Before proving the main part, we first need to show the following:
$$
\begin{align*} 
|\eta_{\widehat{M}}(\pi) - \eta_M(\pi) | &= \Big| \gamma \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ G^\pi_{\widehat{M}} (s,a) \Big] \Big| \quad \because \text{ lemma 4.1}\\
&\le \gamma \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ | G^\pi_{\widehat{M}} (s,a) | \Big] \\
 &\le \lambda \bar{\mathbb{E}}_{(s,a) \sim \rho^\pi_{\widehat{T}}} [\mu(s,a)] \quad \because  \text{assumption 3 and eq (6)}\\
 &= \lambda \epsilon_\mu(\pi)  \quad \because \text{definition}\\
\implies & -\lambda \epsilon_\mu(\pi) \le \eta_{\widehat{M}}(\pi) - \eta_M(\pi) \le \lambda \epsilon_\mu(\pi)\\
&\eta_M(\pi) - 2 \lambda \epsilon_\mu(\pi) \le \eta_{\widehat{M}}(\pi) - \lambda \epsilon_\mu(\pi) \tag{*}
\end{align*}
$$
Now the main part of the proof:
$$
\begin{align*}
\eta_M(\widehat{\pi}) &\ge \eta_{\widehat{M}}(\widehat{\pi}) \quad \because (7)\\
&\ge \eta_{\widehat{M}}(\pi) \quad \because \text{defn of }\widehat{\pi}\\
&= \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) - \lambda \mu(s,a) \Big]\\
&= \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[ r(s,a) \Big] - \mathbb{E}_{(s,a) \sim \rho^\pi_{\widehat{T}}} \Big[\lambda \mu(s,a) \Big]\\
&= \eta_{\widehat{M}}(\pi) - \lambda \epsilon_\mu(\pi) \quad \because \text{defn}\\
&\ge \eta_M(\pi) - 2\lambda \epsilon_\mu(\pi) \quad \because (*)\\
&\text{Since $\pi$ was arbitrary, we get}\\
\eta_M(\widehat{\pi}) &\ge \sup_\pi \{ \eta_M(\pi) - 2\lambda \epsilon_\mu(\pi) \}
\end{align*}
$$
This thoeretical result is very interesting. As mentioned in the paper, 
> one consequence of the above result is that $\eta_M(\widehat{\pi}) \ge \eta_M(\pi^B) - 2 \lambda \epsilon_\mu (\pi^B)$ so $\widehat{\pi}$ should perform at least as well as the behavioral policy $\pi^B$ since $\epsilon_\mu(\pi^B)$ is expected to be small.

Model based reinforcement learning does not get as much attention as model free reinforcement learnning. This is partly because estimating model dynamics is a challenging task. Having read mostly model free reinforcement learning papers, model based method like MOPO was very interesting. 

The paper also has a sample code available on github (link provided in the paper). If time allows, in future posts, I will try implementing MOPO on a toy dataset!


[1]: https://arxiv.org/pdf/2005.13239.pdf