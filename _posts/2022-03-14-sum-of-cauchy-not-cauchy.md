---
title: Sum of Cauchy sequence is not Cauchy
category: math
tags: 
    - Cauchy Sequence
    - Convergence
    - Monotone Convergence Theorem for sequences
mathjax: true
comments: true
layout: single
classes: wide
toc: false
published: true
---



Today I was asked whether sum of two convergent sequences converges. This can be trivial if we are dealing with $\mathbb{R}$ using $\|\cdot\|$ as our metric. But can we say this for every metric function? It turns out, that's not the case, and here we provide a counterexample. 

## Proof
To show that sum of Cauchy sequences is not Cauchy, we need a counterexample. The most frequently used counterexample uses the following metric function:

$$d(x,y) = | \arctan(x) - \arctan(y)|$$

This is clearly a metric (i.e. it satisfies nonnegativity, symmetry, and triangle inequality).  

Now let us define two sequences: $a_n = n$ and $b_n = (-1)^n + n$. We can clearly see that $a_n + b_n = (-1)^n$ does not convege. So if we show that $a_n = n$ and $b_n = (-1)^n + n$ converge, then we are done.  

#### Step 1: $a_n = n$ converges  
Notice that $\arctan(n)$ is an increasing sequence and $|\arctan(n)| < \pi/2$, i.e., bounded. This implies that the sequence $\arctan(n)$ is a bounded monotone sequence. Hence, by the monotone convergence theorem for real sequences, it converges to some point (and this point is in fact $\pi /2$). Since every convergent sequence is a Cauchy sequence, $a_n$ is a Cauchy sequence. 

#### Step 2: $b_n = (-1)^n + n$ converges 
Unlike $\arctan(a_n)$, $\arctan((-1)^n + n)$ is not an increasing sequence. However, we see that $b_{2n-1}$ and $b_{2n}$ are increasing sequences, and by the same logic as above, they both converge and are Cauchy sequences. Then for any arbitrary $\epsilon$, there exists $N_{1, \epsilon}$ and $N_{2, \epsilon}$ such that 

$$|b_{2n-1} - b| < \epsilon \quad \text{for } n \ge N_{1, \epsilon}\\|b_{2n} - b| < \epsilon \quad \text{for } n \ge N_{2, \epsilon}.$$

Then we see that for $n \ge \max(2N_{1, \epsilon} - 1, 2 N_{2, \epsilon})$, we get 

$$|b_n - b| < \epsilon.$$

Therefore, $b_n$ is a Cauchy sequence. Since we know that $b_n$ has subsequences that converge (by lemma 1), it also converges. $\blacksquare$


#### Lemma 1: Cauchy sequence is convergent if and only if it has a convergent subsequence

($\Rightarrow$): 

(Trivial) If Cauchy sequence is convergent, then all of its subsequence must converge to the same limit point. 

($\Leftarrow$): 

Suppose that $x_{n_k}$ is a subsequence of $x_n$ that converges to $x$. Then for some arbitrary $\epsilon > 0$ there exists $N$ such that for all $n, m > N$, $d(x_n, x_m) < \epsilon / 2$. Then for any $n > N$ and $n_k > n > N$, we have:

$$ d(x_n, x) \le d(x_n, x_{n_k}) + d(x_{n_k}, x) $$

The first term on the right is clearly less than $\epsilon$ since $x_n$ is a Cauchy sequence. The second term on the right is also less then $\epsilon$ because the subsequence converges to $x$. Therefore we get  

$$ d(x_n, x) \le d(x_n, x_{n_k}) + d(x_{n_k}, x) < \epsilon$$

Therefore, $x_n$ converges to $x$. 
