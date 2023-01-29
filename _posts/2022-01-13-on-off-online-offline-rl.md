---
title: on- and off-policy? online and offline reinforcement learning?
category: machine-learning
tags: 
    - reinforcement learning
    - on-policy
    - off-poliyc
    - online reinforcement learning
    - offline reinforcement learning
comments: true
mathjax: true
layout: single
classes: wide
toc: false
published: true
---

For those who are first learning reinforcement learning, the term on-policy and off-policy (and offline learning) can be quite daunting (and mostly annoying). Here we outline what they mean, how they are different, and how conceptually simple they are. 

## On-policy

The term on-policy, at least to me, seems to be created simply due to the fact that policy gradient theorem relies on the gradient of the current policy. More specifically, let the reward function be defined as 

$$J(\theta) = \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) V^{\pi_\theta}(s) = \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} \pi_\theta(a \mid s) Q^{\pi_\theta}(s,a) \tag{1}$$

where $d_{\pi}(s)$ is the stationary distribution of Markov chain for $\pi$. The gradient $\nabla_\theta J(\theta)$ is difficult to compute since both $d_{\pi_\theta}$ and $\pi_\theta$ are dependent on $\theta$. The key idea of policy gradient is that there is a way to reformulate the derivative of $\nabla_\theta J(\theta)$ such that we do not have to solve $\nabla_\theta d_{\pi_\theta}$ and get the following gradient:

$$\begin{align*}\nabla_\theta J(\theta) &= \nabla_\theta \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} Q^{\pi_\theta}(s,a) \pi_\theta(a \mid s)\\&\propto \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} Q^{\pi_\theta}(s,a) \nabla_\theta \pi_\theta(a \mid s)\end{align*} \tag{2}$$

If you listen to someone working on reinforcement learning, you often hear them say on-policy reinforcement learning is not data efficient. Again, this is due to the fact that policy gradient requires the gradient of the current policy (observing the equation above, one can easily see that the gradient $\nabla_\theta J(\theta)$ is a function of $\pi_\theta$). Once we update the policy, we can’t use the same policy for our next update. That’s why on every update, we throw away the collected dataset and collect a new one from our newly updated policy.

## Off-policy

If we use trajectories from both current policy and past policies, then it’s called off-policy. Technically, it should be called “on- and off-policy” since we are using both current policy data and past policy data. But that’s too long to write so we just say off-policy. 

## Offline

Offline is a newly introduced terminology in the reinforcement learning literature. It literally just means we have a set of collected trajectories that we can use to train our agent but we don’t have a simulator to create more trajectories. 

## Online

If you have a simulator where your agent can try all possible actions, it is online. 

(**Remark**: No one really says online reinforcement learning since we always assume that there is a simulator but with the advent of offline reinforcement learning, some people have started to use the term online to make it clear to their readers that it is not offline).

## Online/Offline $\perp$ On-policy/Off-policy

Online/offline and on-policy/off-policy are orthogonal concepts. So you can have a reinforcement learning algorithm that is “online off-policy” or “offline on-policy.”
