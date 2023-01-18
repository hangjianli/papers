# TTD Design (WIP)

###### Hangjian Li. version: 0.3

## What is dimensional bidding provided by TradeDesk?

* **Ad Group**: made up of multiple elements that combine into a cohesive strategy.
  * Audience.
  * Bid Lists.
  * Budgets.
  * Creatives.
  * Base and Max bids, defined by CPM.
* Dimensional bidding.
  * A **dimension** is a targeting item that you can target, block, or apply bid factors to. e.g, "Site", "Ad Format", "Geolocation". 

<img src="/Users/h0l07zi/Desktop/Screen Shot 2022-08-18 at 1.31.21 PM.png" alt="s" style="zoom:43%;" />



* Example of a **bid list**

```python
{
		"BidListId": "2131712",
    "Name": "Bidlist 1",
    "BidListSource": "User",
    "BidListAdjustmentType": "Optimized",
    "ResolutionType": "ApplyMultiplyAdjustment",
    "BidLines": [
        {
            "BidLineId": "1216340",
            "BidAdjustment": 2.030000,
            "DomainFragment": "com.cardgame.solitaire.flat",
            "SupplyVendorId": 1,
            "PublisherId": "f77344fc701f4b1f981238390e0b8ffb",
            "ImpressionPlacementValue": "f37ac1804f8040a4b49295e5d13167ff"
        },
        {
            "BidLineId": "1216341",
            "BidAdjustment": 1.020000,
            "DomainFragment": "com.merriamwebster",
            "SupplyVendorId": 118,
            "PublisherId": "11653",
            "ImpressionPlacementValue": "177976"
        },
    ]
}
```

* Currently, we only use `BlockList` and `TargetList`. 

## General Requirements

* Objectives:
  * Make use of the `Optimized` bid list type.
  * **Maximize total (attributed) revenue** subject to the budget constraint.
* Our deliverable
  * Bid dimensions.
  * An optimization framework that can produce the bid factors. 

## Data available

* `attributed sales` (14 or 30 days attribution window)
* `Impression cost` (equal to bid price under first price auction)
* `Impression attributes` (time, geo, publisher, platform, etc.)
* `campaign metadata` (budget, start and end dates, etc.)



## Design 1: disjoint dimensions

* **Objective**: maximize ROAS under budget constraint for each **adgroup**.

* **Assumptions**:

  * Cost per impression (**CPI**) (under first price auction): $b_i = b_0 \cdot f_i$
    *  $i$ refers to dimension $i$. 
    * assume based bid $b_0=1$ for simplicity, and we manipulate the bid factor $f_i$ for each dimension
  * Number of impressions won: $\mathbb{E}\left[n_i\right] = g(f_i)$, e.g., $n_i = \beta_i \cdot f_i$.
  * Revenue per impression ($RPI_i$) 
    * independent from $b_i$.
    * can be estimated for each dimension $i$.
    * property of dimension $i$ and stay constant during the day.

* **Notations**

  * $CPI_i = f_i$
  * $n_i = \mathcal{N}\left(\beta_i \cdot f_i, \sigma^2\right)$.
  * Total spending in $i$: $S_i$.
  * Total revenue in $i$: $R_i$.
  * Daily budget constraint: $B$.

  |            | State1                      | State2           | State3           |        |
  | :--------- | --------------------------- | :--------------- | ---------------- | :----- |
  | **Site 1** | 1 (= $n_1 = \beta_1 f_{1}$) | 2 $(\beta_2f_2)$ | 3 $(\beta_3f_3)$ | **6**  |
  | **Site 2** | 12 $(\beta_4f_4)$           | 1 $(\beta_5f_5)$ | 6 $(\beta_6f_6)$ | **19** |
  | **Site 3** | 7 $(\beta_7f_7)$            | 5 $(\beta_8f_8)$ | 9 $(\beta_9f_9)$ | **21** |
  |            | **20**                      | **8**            | **18**           |        |

* Parameter estimation

  * $RPI_i$ can be estimated based on attributed sales for dimension $i$. 
  *  $\beta_i$ can be estimated through linear regression. 

* **Optimization**

$$
\begin{aligned}
&\max_{f_i}\ \sum_{i=1}^m RPI_i\cdot g(f_i) \\\\
\text{subject to}\ &\sum_{i=1}^m S_i = \sum_{i=1}^m f_i\cdot g(f_i)= B.
\end{aligned}
$$

From the assumptions we know
$$
\begin{aligned}
S_i &= n_i \cdot CPI_i = \beta_i\cdot f_i^2 \\
R_i &= RPI_i \cdot n_i = RPI_i \cdot \beta_i \cdot f_i =  RPI_i \cdot  \sqrt{\beta_i\cdot S_i}.
\end{aligned}
$$

$$
\begin{aligned}
\max_{f_i} &\sum_{i=1}^m RPI_i\cdot \beta_i\cdot f_i \\
\text{subject to}\quad &\sum_{i=1}^m f_i^2\cdot\beta_i = B
\end{aligned}
$$

The Lagrangian can be written as:
$$
\mathcal{L(\lambda, f_1,\ldots, f_m)} = \sum_{i=1}^m PRI_i\cdot\beta_i\cdot f_i - \lambda\left(\sum_{j=1}^m f_j^2\cdot\beta_j - B\right)
$$

$$
\begin{aligned}
\begin{cases}
      \nabla_{\lambda}\mathcal{L}(\lambda, f_1,\ldots, f_m) &= \sum_{j=1}^m \beta_jf_j^2 - B = 0\\
			\nabla_{f_i}\mathcal{L}(\lambda, f_1,\ldots, f_m) &\propto RPI_i  - 2\lambda f_i = 0
    \end{cases}
\end{aligned}
$$

Solving these two equations gives the **optimal choice of bid factor $\hat f_i$**:
$$
\hat f_i^2 = \frac{RPI_i^2}{\sum_{j=1}^m RPI_j^2\cdot \beta_j}\cdot B
$$
The spending on the $i$th dimension at optimum is 
$$
S_i = \frac{RPI_i^2\cdot \beta_i}{\sum_{j=1}^m RPI_j^2\cdot \beta_j}\cdot B
$$

### Limitation

* Not scalable with more dimensions and groups need to be considered.
  * _curse of dimensionality_ if considering all combinations of bid dimensions. Not enough impression at each section.

* Not making full use of the multidimensional bidding feature.



## Design 2: overlapping bid dimensions 

* Motivation

  * bid price = $b_0 * f_1 * f_2$

* **Example:**

  We now consider two **types** of dimensions (superscript): site and state, each has 3 unique **groups** (subscript). 

|                        | State1 ($f_{1}^2$) | State2  ($f_{2}^2$) | State3  ($f_{3}^2$) |        |
| :--------------------- | :----------------- | :------------------ | ------------------- | ------ |
| **Site 1** ($f_{1}^1$) | 1                  | 2                   | 3                   | **6**  |
| **Site 2** ($f_{2}^1$) | 4                  | 5                   | 6                   | **15** |
| **Site 3** ($f_{3}^1$) | 7                  | 8                   | 9                   | **24** |
|                        | **12**             | **15**              | **18**              |        |

* **Notations**

  * ~~Let $j$ index the marginal dimensions. i.e., $j = 1,\ldots, m$, where $m = K \cdot I$ if each dimension (bid list) has $I$ categories.~~
  * If the example above, $K = 2, I = 3$.

* **Assumptions**

  * $RPI_j^d$ is defined for each marginal dimension

    * constant 
    * estimable

  * Number of impressions won at marginal dimension $(d, j)$:  
    $$
    \begin{aligned}
    \mathbb{E}\left[ n_j^d \right] &= g(f_1^1,\ldots, f_I^K) \\
    &= \text{volume\_intercept}^d + b_0\cdot \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \beta_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]\\
    \end{aligned}
    $$

    * Example:

      * Recall the bidding price is defined as $b_{12} = f^1 \times f^2$ in TTD API. In Design 1 we would have that $\mathbb{E}\left[n_{12}\right] = \beta_{12}\times b_{12}$.

      $$
      \begin{aligned}
      \mathbb{E}\left[n_1^1\right] &= \beta_1^1 \cdot f_1^1 \cdot (\beta_1^2f_1^2 + \beta_2^2f_2^2 + \beta_3^2f_3^2)\\
      \mathbb{E}\left[n_2^1\right] &= \beta_2^1 \cdot f_2^1 \cdot (\beta_1^2f_1^2 + \beta_2^2f_2^2 + \beta_3^2f_3^2)\\
      \mathbb{E}\left[n_3^1\right] &= \beta_3^1 \cdot f_3^1 \cdot (\beta_1^2f_1^2 + \beta_2^2f_2^2 + \beta_3^2f_3^2)\\\\
      \mathbb{E}\left[n_1^2\right] &= \beta_1^2 \cdot f_1^2 \cdot (\beta_1^1f_1^1 + \beta_2^1f_2^1 + \beta_3^1f_3^1)\\
      \mathbb{E}\left[n_2^2\right] &= \beta_2^2 \cdot f_2^2 \cdot (\beta_1^1f_1^1 + \beta_2^1f_2^1 + \beta_3^1f_3^1)\\
      \mathbb{E}\left[n_3^2\right] &= \beta_3^2 \cdot f_3^2 \cdot (\beta_1^1f_1^1 + \beta_2^1f_2^1 + \beta_3^1f_3^1)
      \end{aligned}
      $$

      * If there were one more type of dimension, e.g., **time**, with 3 unique **groups**, the estimated total impresion from `Site1` becomes
        $$
        \mathbb{E}\left[n_1^1\right] = \beta_1^1 \cdot f_1^1 \cdot (\beta_1^2f_1^2 + \beta_2^2f_2^2 + \beta_3^2f_3^2)\cdot (\beta_1^3f_1^3 + \beta_2^3f_2^3 + \beta_3^3f_3^3)
        $$
        

  * Cost for marginal dimension $(d, j)$: 

    * Average cost per impression
      $$
      CPI_j^d = \text{cost\_intercept}^d + b_0\cdot\left(\alpha_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \alpha_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]
      $$

    * Total spending for marginal $(d, j)$

    $$
    S_j^d = n_{j}^d \cdot CPI_{j}^d
    $$

* **Remark**

  * Compared to Model 1, in Model 2 we make the following additional assumptions:

    * $\beta_{j, k} = \beta_j^{d_1}\cdot \beta_k^{d_2}$       (decomposable impression number coefficients).=

    * $f_{j, k} = f_j^{d_1}\cdot f_k^{d_2}$       (decomposable bid feactor).

  * The number of parameters reduces from $O(I^K)$ to $O(IK)$. 

* **Parameter Estimation**

  * $l_2$ Loss function 
    $$
    l(\beta_1^1,\ldots,\beta_3^2\mid f_1^1,\ldots, f_3^2, n_1^1,\ldots, n_3^2) = \sum_{k=1}^K\sum_{i=1}^{I_k}\|n_i^k -\left(\beta_{i}^k\cdot f_{i}^k\right) \cdot \left(\prod_{m \neq k}^K\sum_{j=1}^{I_{m}} \beta_{j}^m\cdot f_{j}^m\right) \|_2^2
    $$

  * Matrix form
    $$
    \begin{aligned}
    \begin{bmatrix}
    n_1^1\\n_2^1\\n_3^1\\n_1^2\\n_2^2\\n_3^2 
    \end{bmatrix}
    &=\begin{bmatrix}
    \beta_1^2 &&&&\\
    &\beta_2^2&&&\\
    &&\beta_3^2&&\\
    &&&\beta_1^1&\\
    &&&&\beta_2^1\\
    &&&&&\beta_3^1
    \end{bmatrix}
    \cdot 
    \begin{bmatrix}
    f_1^2f_1^1 & f_1^2f_2^1 & f_1^2f_3^1 & & & \\
    f_2^2f_1^1 & f_2^2f_2^1 & f_2^2f_3^1 & & & \\
    f_3^2f_1^1 & f_3^2f_2^1 & f_3^2f_3^1 & & & \\
    & & & f_1^1f_1^2 & f_1^1f_2^2 & f_1^1f_3^2 \\
    & & & f_2^1f_1^2 & f_2^1f_2^2 & f_2^1f_3^2 \\
    & & & f_3^1f_1^2 & f_3^1f_2^2 & f_3^1f_3^2 
    \end{bmatrix}
    \begin{bmatrix}
    \beta_1^1\\
    \beta_2^1\\
    \beta_3^1\\
    \beta_1^2\\
    \beta_2^2\\
    \beta_3^2
    \end{bmatrix} 
    \end{aligned}
    $$

  * Data generation

    We need to observe $\{n_i^k\}_{ik}$ for a range of values of $\{f_i^k\}_{{ik}}$ in order to estimate $\{\beta_i^k\}_{ik}$. 

    

* **Optimization**

  * Total revenue $R$:
    $$
    R = \frac{1}{K}\sum_{k=1}^K\sum_{i=1}^{I_k} n_{i}^k\cdot RPI_i^k.
    $$

  * Total spending $S$:
    $$
    S = B = \frac{1}{K}\sum_{k=1}^K\sum_{i=1}^{I_k} n_{i}^k\cdot CPI_i^k.
    $$

  * Objective function
    $$
    \begin{aligned}
    &\max_{\{f_{i}^d\}}\ \sum_{d=1}^K\sum_{j=1}^{D_d} \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{D_{k}} \beta_{i}^k\cdot f_{i}^k\right) \cdot RPI_j^d\\\\
    \text{subject to}&\quad \sum_{d=1}^K\sum_{j=1}^{D_d}\left[\beta_{j}^d\cdot  \alpha_{j}^d\cdot (f_{j}^d)^2 \cdot \prod_{k \neq d}^K\left(\sum_{i=1}^{D_{k}} \beta_{i}^k \cdot f_{i}^k\right) \cdot \left(\sum_{i=1}^{D_{k}} \alpha_{i}^k\cdot f_{i}^k\right) \right]\leq K\cdot B, \\
    &\quad f_i > 0,
    \end{aligned}
    $$
    
  * Lagrangian
    $$
    \begin{aligned}
    \mathcal{L}(f_j^d,\lambda) &= \sum_{d=1}^K\sum_{j=1}^{D_d} \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{D_{k}} \beta_{i}^k\cdot f_{i}^k\right) \cdot RPI_j^d \\
    \ & - \lambda\left(\sum_{d=1}^K\sum_{j=1}^{D_k}\left[\beta_{j}^d\cdot  \alpha_{j}^d\cdot (f_{j}^d)^2 \cdot \prod_{k \neq d}^K\left(\sum_{i=1}^{D_{k}} \beta_{i}^k \cdot f_{i}^k\right) \cdot \left(\sum_{i=1}^{D_{k}} \alpha_{i}^k\cdot f_{i}^k\right) \right] - K\cdot B\right)\\
    \end{aligned}
    $$
    
  * Quasi-Newton's method (`BFGS`, `L-BFGS-B`, `SLSQP`).
  
    







## API

* start from one `ad_group` and use statistical test to determine if the improvement in KPI is significant compared to control `ad_groups`. (`t-test`)
* each bid list must contain a distinct combination type (e.g., site and geo, device type and ad environment, etc.).
* API example response

```python
{
    "IsGlobal": false,
    "BidListDimensions": [
        "HasDomainFragmentId",
        "HasSupplyVendorId",
        "HasImpressionPlacementId",
        "HasPublisherId"
    ],
    "BidListId": "2131712",
    "Name": "Bidlist 1",
    "BidListSource": "User",
    "BidListAdjustmentType": "Optimized",
    "ResolutionType": "ApplyMultiplyAdjustment",
    "BidLines": [
        {
            "BidLineId": "1216340",
            "BidAdjustment": 2.030000,
            "DomainFragment": "com.cardgame.solitaire.flat",
            "SupplyVendorId": 1,
            "PublisherId": "f77344fc701f4b1f981238390e0b8ffb",
            "ImpressionPlacementValue": "f37ac1804f8040a4b49295e5d13167ff"
        },
        {
            "BidLineId": "1216341",
            "BidAdjustment": 1.020000,
            "DomainFragment": "com.merriamwebster",
            "SupplyVendorId": 118,
            "PublisherId": "11653",
            "ImpressionPlacementValue": "177976"
        },
        {
            "BidLineId": "1216342",
            "BidAdjustment": 1.020000,
            "DomainFragment": "com.pandora.android",
            "SupplyVendorId": 50,
            "PublisherId": "71711271",
            "ImpressionPlacementValue": "cKClcPNTu1Te"
        },
        {
            "BidLineId": "1216343",
            "BidAdjustment": 1.020000,
            "DomainFragment": "com.strawdogstudios.simonscatcrunchtime",
            "SupplyVendorId": 99,
            "PublisherId": "FYBER-139222",
            "ImpressionPlacementValue": "530c4d2894e444a1976f41d527c03a07"
        }
    ],
    "BidListOwner": "AdGroup",
    "BidListOwnerId": "sberg7l",
    "IsAvailableForLibraryUse": false
}			
```

#### Associate the new bid list to an ad group

```python
{
    "AdGroupId": "sberg7l",
	"AssociatedBidLists": [
        {
            "BidListId": "2131711",
            "IsEnabled": true,
            "IsDefaultForDimension": true,
            "BidListAdjustmentType": "Optimized",
        },
        {
            "BidListId": "2131712",
            "IsEnabled": true,
            "IsDefaultForDimension": true,
            "BidListAdjustmentType": "Optimized",
        }
    ]
}
```
