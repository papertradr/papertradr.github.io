---
title: "About"
layout: single
permalink: /about/
author_profile: true
---
Hello! I spend my time solving math problems and programming in python, c++ and little bit of rust. My job requires me to stay up to date with both math and programming. I usually posts stuff that I found interesting.  

## Books that I enjoyed!
- [Team Topologies][8]: (currently reading!)
- [So Good They Can't Ignore You][4] : don't chase your passion, develop your career capital 
- [Outliers: The story of success][3]: 10,000 hour rule
- [Range: Why generalists Triump in a specialized world][5] : 10,000 hour rule doesn't always work
- [No rules rules][1] : more freedom to employees assuming high talent density
- [The Black Swan][6] : If rare events occur more than it should, then we probably shouldn't use gaussian distribution in our model
- [Thinking fast and slow][7] : cognitive biases need to be accounted for; don't let system 1 make decisions, use system 2
- [Flash Boys][2]: A Wall Street Revolt : pretty good book if you're interested in hft (another masterpiece by michael lewis)

## Setting up this blog
Setting up my first github pages was not as easy as I thought. Since I don't have any experience with creating a static web page, I had to look up bunch of stuff on stackoverflow and tutorials.

1. First thing I did was to clone this repo [minimal mistakes](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/) and follow the `Quick-Start Guide`. Note that you need to install bunch of stuff for this. Plus, you need a `github` account and make your `github pages`.  

2. I'm using [disqus](https://disqus.com/) to enable commenting on my posts.

If you want to run your jekyll site locally, you need to install `jekyll` and run
```
jekyll serve
```
If you modified your `Gemfile`, run
```
bundle exec jekyll serve
```
### Setting up mathjax support
To enable `mathjax` support for you jekyll website, follow the instruction [here](https://benlansdell.github.io/computing/mathjax/).


### Blogging with jupyter notebooks
To embed your jupyter notebook on your jekyll website, follow the tutorial [here](https://cduvallet.github.io/posts/2018/03/ipython-notebooks-jekyll).
Just in case the link is down, here is what you should do:
1. Write the jupyter notebook in the `_jupyter` folder
2. When it's finished, `jupyter nbconvert <nb> --to markdown`
3. Move it to the `_posts` folder

For now I'm gonna see how long I can blog consistently. If this works out, maybe I'll branch out to creating videos on youtube!

[1]: https://www.goodreads.com/book/show/49099937-no-rules-rules
[2]: https://www.goodreads.com/book/show/24724602-flash-boys
[3]: https://www.goodreads.com/book/show/3228917-outliers
[4]: https://www.goodreads.com/book/show/13525945-so-good-they-can-t-ignore-you
[5]: https://www.goodreads.com/book/show/41795733-range
[6]: https://www.goodreads.com/book/show/242472.The_Black_Swan
[7]: https://www.goodreads.com/book/show/11468377-thinking-fast-and-slow
[8]: https://www.goodreads.com/en/book/show/44135420
