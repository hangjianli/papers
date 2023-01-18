# Learning bid factors based on matrix factorization

###### Version: 0.4 

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

**Assumptions**

* $RPI_j^d$ is defined for each marginal dimension

  * constant 
  * estimable

* Number of impressions won at marginal dimension $(d, j)$:  
  $$
  \begin{aligned}
  \mathbb{E}\left[ n_j^d \right] &= g(f_1^1,\ldots, f_I^K) \\
  &= \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \beta_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]\\
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
    
    * In matrix form
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
      
  
* Cost for marginal dimension $(d, j)$: 

  * Average cost per impression
    $$
    CPI_j^d = \left(\alpha_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \alpha_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]
    $$

  * Total spending for marginal $(d, j)$





## Trade Desk Systems

#### Pacing (throttling)

For each ad group

* Define buckets of inventories (can be modified through API).
* For each bucket, set a **keep rate** (0% - 100%) on the impressions to bid on. 
* Affected only by budget.
* Every 30 seconds.

#### Predictive clearing (bid shading)

Push down bid price while maintaining certain win rate.

* Follow the **win rate curve** for a pocket of inventory.
* Independent from **pacing** and **optimization** systems.
* Saved budget (surplus) is added back to total budget which in turn affacts pacing and optimization.
* Daily ?

## New model

#### Assumptions

* $RPI_j^d$ 

  * independent from $b$

* Cost per impression

  * $$
    \widetilde{CPI}_j^d = \left(\alpha_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \alpha_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]
    $$

  * $$
    CPI_j^d = C_0 + C_{bid\ shading}\cdot \widetilde{CPI}_j^d
    $$

* Impression volume

  * $$
    \begin{aligned}
    \tilde n_j^d &= g(f_1^1,\ldots, f_I^K) \\
    &= \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \beta_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]\\
    \end{aligned}
    $$

  * $$
    \mathbb{E}[n_{j}^d] = C_{pacing} \cdot \tilde n_j^d
    $$



#### Parameter estimation



* RPI

  * Exponential moving average:
    $$
    RPI_t^{EM} = \alpha\left[RPI_t + (1 - \alpha)\cdot RPI_{t-1} + (1 - \alpha)^2 \cdot RPI_{t-2} + \ldots + (1 - \alpha)^t \cdot RPI_0 \right]
    $$

  * 

    

## Control system

* error factor
* update time interval $\Delta t_k = t_k - t_{k-1}$.
* change in error factor $\Delta e(t_k) = e(t_k) - e(t_{k-1})$.
* $p$ factor push the current variable to reference value.
* $i$ factor reduces the accumulative error. 
* $d$ factor contorls the fluctuation of the variable.


$$
\begin{align}

e(t_k) &= \tilde f_i^d(t_k) - f_i^d(t_{k-1}) \quad\text{(difference in the proposed and current bid factors.)}
\\
\phi(t_{k+1}) &= K_pe(t_k) + K_d\frac{\Delta e(t_k)}{\Delta t_k} + K_i\sum_{j=1}^k e(t_j)\Delta t_j \quad\text{(control signal at time $t$)}
\end{align}
$$

##### Actuator

$$
f_i^d(t_k)  = f_i^d(t_{k-1})\cdot\exp\{\phi(t_k)\}
$$

## Next steps



1. If we know win rate distribution $G(b_t)$, how can we improve the model?
2. How to identify dimensions to optimize on?
