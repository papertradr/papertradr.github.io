---
title: What is the definition of continuity?
category: math
tags:
    - continuous
mathjax: true
comments: true
layout: single
classes: wide
toc: false
published: true
---
When I first studied real analysis, the definition of continuity was clear but there were just so many of them. I took some time to list as many definition of continuity as I could, and provide some observations on why we need so many definitions and how they are different. 

## Topological Definition of Continuity

The topological definition of continuity is as follows:

### Open set Continuity

> **(Open set continuity)** Given a topological space $X$ and $Y$, a function $f : X \to Y$ is continuous if for every open set $\mathcal{O} \in Y$ the inverse image $f^{-1}(\mathcal{O}) = \{ x \in X : f(x) \in \mathcal{O}\}$ is an open subset of $X$
> 

This rather general definition of continuity can be quite baffling. There’s another topological definition of continuity:

### Sequential Continuity

> **(Sequential continuity)** Given a topological space $X$ and $Y$, a function $f : X \to Y$ is sequentially continuous $f(x_n) \to f(x)$ whenever $x_n \to x$. 
(**Remark:** Note that ***sequential continuity does NOT imply continuity*** but ***continuity does imply sequential continuity.)***
> 

However, in **a metric space**, the above two definitions are **equivalent**. 

## Metric space Definition of Continuity

One can easily see that metric space definitions require a distance function (obviously) instead of open sets or sequences. Here we introduce some of the most fundamental definitions of continuity:

### Point-wise continuity

> **(Point-wise continuity)** Given a metric space $(X, d_1)$ and $(Y, d_2)$, a function $f: X \to Y$ is continuous at point $x \in X$ if for every $\epsilon > 0$ there exists $\delta > 0$ such that $d_2(f(x), f(y)) < \epsilon$  whenever $d_1(x,y) < \delta$ 
**(Remark: note that point-wise continuity is clearly a local property)**.
> 

### Uniform continuity

> **(Uniform continuity)** Given a metric space $(X, d_1)$ and $(Y, d_2)$,  a function $f: X \to Y$ is uniformly continuous on $X$  if for every $\epsilon > 0$ there exists a $\delta > 0$ such that whenever $d_1(x,y) < \delta$, we have $d_2(f(x), f(y)) < \epsilon$ 
**(Remark: note that uniform continuity is a local property).**
> 

As opposed to the topological definition, the $\delta\text{-}\epsilon$ continuity definitions require a metric space. 

There’s even more definition of continuity:

### Lipschitz continuity

> **(Lipschitz continuity)** Given two metric spaces $(X, d_X)$ and $(Y, d_Y)$, a function $f: X \to Y$ is Lipschitz continuous if there exists a real constant $K \ge 0$  such that for all $x_1$ and $x_2$ in $X$,
> 
> 
> $$ d_Y(f(x_1), f(x_2)) \le Kd_X(x_1, x_2) $$
> 
> Any such $K$  is called a Lipschitz constant for the function $f$. 
> **(Remark: note that Lipschitz continuity is a global property)** .
> 

### a-**Hölder Condition**

> **($\alpha$-Holder condition)** Given two metric spaces $(X, d_X)$  and $(Y, d_Y)$, a function $f: X \to Y$ satisfies $\alpha$-Holder condition (or $\alpha$-Holder continuous) if there exists $C_\alpha$ such that
> 
> 
> $$d_Y(f(x), f(x')) \le C_\alpha d_X(x, x') \; \forall x,x' \in X$$
> 
> **(Remark: note that Holder condition is a global property)** .
> 

The above two definitions also rely on metric spaces. However, unlike $\delta\text{-}\epsilon$ definitions which are local properties, the above continuities are global properties, hence they are a stronger. 

## Why so many definitions?

### Continuity with different degree of constraints

Clearly there are lots of definitions of continuity but there is a good reason for it. Some continuity conditions are ***stronger*** than others. For instance, uniform continuity is a defines continuity on a set as opposed to point-wise continuity that defines it on a single point. Similarly, Lipschitz continuity and holder condition are both *global* property with very strict condition that all pairs satisfy the bound. 

<!-- ### Continuity preserves topological structure!

Recall that a metric induces a topology. If an operator is continuous, then by the definition of a topological continuity, the open sets are preserved and the topological structure of an image remains intact(?). --> 

## Why topological definition of continuity?

Then why do we have a topological definition and a metric space definition? Well the topological space is more general than the metric space (metric spaces are topological spaces with additional constraints). Hence the definition of continuity on a topological space also hold in metric spaces.
