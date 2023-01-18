## Choose partitions

- Dimensions to split:
    1. Geo
    2. Site
    3. hour of day
    4. day of week
- Split criterion 
    - equal impression volume
        1. Sort each set by imp volume 
        2. Pick number of groups `k`
        3. Divide total imp volume by `k` and use it as threshold
        4. start with small group with label 1
    - performance-based (TODO)
    - based on cost or ROAS 
    
## Parameter estimation

Current model for bidding landscape.

$$
\begin{aligned}
\mathbb{E}\left[ n_j^d \right] &= g(f_1^1,\ldots, f_I^K)\\
&= a^d + \left(\beta_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \beta_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K] \\
CPI_j^d &= c^d + \left(\alpha_{j}^d\cdot f_{j}^d\right) \cdot \left(\prod_{k \neq d}^K\sum_{i=1}^{I_{k}} \alpha_{i}^k\cdot f_{i}^k\right),\quad  k, d\in[K]
\end{aligned}
$$


- Method:
    1. in historical data, all bid factors are equal to $1$.
    2. solve a system of equations (K-order) by minimizing $\|y - g(f)\|_2^2$, $y$ are CPI or volume.
- __Issues__:
    1. What the input volume should be?
        1. daily average imp cnt?
        2. total imp cnt so far?
    2. When modeling imp volume, algorithm is hard to converge. 
        - Fix: scale down the imp volume by a factor
    3. Estimated $\alpha, \beta$ can have negative components. 
        - Fix: add nonnegative constraint
    
#### Example of parameter estimation

If we only have one day of data, we don't need the timestamp.
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


In practice, for a new day $t$, we observe new values of $(n_{j, t}^d, f_{j, t}^d)$, where $n_{j, t}^d$ is the total volume in day $t$ for dimension $(d, j)$. As the campaign continues, we will have observations from multiple days.

* $$n_{j, t}^d = g(f_{[I], t}^{[K]})$$



```python
args_vol = (
	imp_volume / self.imp_volume_scale_factor,
	bid_factor,
	basebid,
	beta_lam,
	null_level_lst
)

```






## bid factor optimizer

- __Issues__:
    1. negative spend 
        1. with the estimated $\alpha,\beta$, positive bid factors can lead to negative ad spend
    2. convergence.
    3. does not meet the budget
- Quick validation of optimization results:
    1. predicted revenue > actual revenue
    2. predicted ROAS by dimension > actual ROAS
    3. 

## PID controller
Total remaining budget as target.


## Offline evaluation

Suppose we already picked the dimensions and groups.
    
- Split one campaign into training and testing
    1. The first 70% days of the campaign impressions used as training
        1. collect RPI, CPI, volume, budget
        2. model volume and CPI for each dimension. Estimation the model parameters. 
        3. optimize the bid factors $f$.
        4. bid with the optimized $f$
    2. 
- AB test on __two groups__ of campaigns
    1. Identify comparable campaigns
    2. 



## Online evaluation