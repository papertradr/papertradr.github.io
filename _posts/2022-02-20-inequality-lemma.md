---
title: Some useful inequalities
category: math
tags: 
    - inequalities
mathjax: true
comments: true
toc: false
layout: single
classes: wide
published: false
---

There are some well known inequalities (e.g. Markov inequality, AM-GM inequality, Young's inequality, Minkowski's inequality, etc). Here we list some inequalities that don't have any names but show up more often than you'd expect.  

## inequality 1

If $0 < p < 1$ and $f, g > 0$, 

$$f^p + g^p > (f + g)^p, \tag{1}$$

(Proof)

When $f = g = 0$, it is trivial. Let $ p = 1-q$ where $ q \in [0, 1]$. Then if $f, g \ge 0$, 

$$\begin{align} (f + g)^p = (f + g)^{1-q} &= f (f + g)^{-q} + g(f + g)^{-q} \\ &={f \over (f + g)^q} + { g\over (f + g)^q} \\ &\le {f \over f^q} + {g \over g^q} \\ &(\because \text{Since $f, g \ge 0, f \le f + g$ and $g\le f + g$, and $0 \le q \le 1$}) \\ &= f^{1-q} + g^{1-q} \\ &= f^p + g^p \end{align}$$

$\blacksquare$


## inequality 2
If $p \ge 1$ and $f, g > 0$, then 

$$f^p + g^p \le (f + g)^p \tag{2}$$

(Proof)

If $f = g = 0$, it is trivial. Let $p = 1-q$ where $q < 0$. Then if $f, g \ge 0$, 

$$\begin{align} (f + g)^p = (f + g)^{1-q} &= f(f + g)^{-q} + g(f-g)^{-q} \\ &= {f \over (f + g)^q} + {g \over (f + g)^q} \\ &\ge {f \over f^q} + {g \over g^q} \\ &(\because \; q < 0 \text{, so as $f$ increases, $f \over f^q$ increases}) \\ &= f^{1-q} + g^{1-q} \\ &= f^p + g^p\end{align}$$

$\blacksquare$


## inequality 3
Given $a, b \in \mathbb{R}$ and $p > 0$, then 

$$|a + b|^p < 2^p (|a|^p + |b|^p) \tag{3}$$

(Proof)

$$\begin{align} |a + b|^p \le (|a| + |b|)^p &\le 2^p \max \{ |a|^p, |b|^p \} \\ &\le 2^{p-1} (|a|^p + |b|^p - |a^p - b^p|) \\ &\le 2^{p-1} (|a|^p + |b|^p) \\ &\le 2^p(|a|^p + |b|^p)\end{align}$$

$\blacksquare$

## inequality 4

$$1 + x \le e^x \tag{4}$$

(Proof)

Let $y = x + 1$. Then $y$ is the tangent line to $y = e^x$ when $x = 0$. Since $e^x$ is convex, $e^x$ always remains above its tangent lines.  $\blacksquare$
