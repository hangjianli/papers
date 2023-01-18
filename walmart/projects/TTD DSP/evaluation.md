# Evaluation	

General principle: due to the interaction with black box systems such as pacing and shading, evaluation should primarily be done offline. 



### how to identify two (groups) comparable campaigns







### How to model winning price $p(z\mid x)$

#### Log-normal model

* $z$ is the winning price of impression sample $x$.
* Cui et al (2011): $\log z\sim\mathcal{N}(\mu, \sigma)$.
* Drawback: didn't use $x$. 

#### Censored linear regression (NOT doable)

* observed winning price are right-censored, and biased. 
* but we don't have losing bid price

#### Survival model

?











## Method 1 ROAS comparison under linearity assumption

* bid factors should favor the dimensions with **higher ROAS** from the previous batch.
* ROAS can be computed emprically.



## Method 2 Bid simulator



## Method 3 Cross validation

Given a campaign, get the set of all impressions $I$. 

1. split all impressions into **training** and **validation**, e.g., 70-30 split.
2. estimate $\alpha$,  $\beta$ , $RPI$ based on 
   1. 70% of data
   2. first few weeks of data
3. Optimize bid factors based on inputs
   1. $\alpha$,  $\beta$ , $RPI$ 
   2. budgets. 
      1. total budget - ads spend so far
4. For each impression in **validation set**, use the optimized bid factors to
   1. compute bid price
   2. compare with observed `cost` , which can be regarded as the winning price for that impression
   3. compute `total revenue` and `ad spend` --> `ROAS`
   4. benchmark observed ROAS

Winning price

- impression level 

- group level

  

* win rate for each dimension
* change has to be significant enough
  * total 100 impression, win 99 won't work.
* compute each day separately



## Key metrics to evaluate on 

1. ROAS.
2. Impressions volume achieved.



## Using data from existing campaigns



## System robustness

* What if assumptions are wrong?
* what if coefficients are off





## Bidding Simulator

Google Ads Simulator: https://support.google.com/google-ads/answer/9634060#zippy=%2Cfind-a-smart-bidding-target-simulator-for-your-ad-group

* The simulator is updated each day to reflect the last 7 days.
* 

Google Smart Bidding: https://support.google.com/google-ads/answer/7065882

Google Bidding signals (dimensions): https://support.google.com/google-ads/answer/7065882#zippy=%2Cautomated-bidding-signals



Can we estimate counterfactual ROAS?
