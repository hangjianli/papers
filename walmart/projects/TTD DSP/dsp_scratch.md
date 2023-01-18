```flow
st=>start: start
e=>end: end
op1=>operation: bid requests
op2=>operation: ttd translates request into (combo) dimensions 
op3=>operation: ttd looks for matches in bid lists
cond1=>condition: got a match
op4=>operation: bid with bid factors


st->op1->op2->op3->cond1
cond1(yes)->op4->e
cond1(no)->e
```



### UI

* PACING_TYPE_AHEAD	Ahead pacing attempts to spend faster than evenly, to make sure the entire budget is spent by the end of the flight.
* PACING_TYPE_ASAP	Spend all of pacing budget amount as quick as possible.
* PACING_TYPE_EVEN	Spend a consistent budget amount every period of time.

* Ad group:  assembling targeting specifics and strategies



## Scratch section


$$
\begin{aligned}
0 =\frac{\partial}{\partial f_j^d}\mathcal{L}(f_j^d, \lambda)  &= \beta_{j}^d \cdot \left(\prod_{m \neq d}^K\sum_{i=1}^{D_{m}} \beta_{i}^m\cdot f_{i}^m\right)\cdot RPI_j^d  + \sum_{k\neq d}\sum_{j=1}^{D_k} \left(\beta_j^k\cdot f_j^k\right)\cdot \left( \beta_{j}^d \prod_{m\neq\{d, k\}}\sum_{i=1}^{D_m}\beta_i^m\cdot f_i^m\right)\\
\ &- \lambda\Bigg[2\beta_j^d\cdot \alpha_j^d\cdot f_j^d \cdot \prod_{k\neq d}^K\left(\sum_{i=1}^{D_m}\beta_i^m\cdot f_i^m\right) \cdot \left(\sum_{i=1}^{D_{k}} \alpha_{i}^k\cdot f_{i}^k\right) \Bigg] \\
 \ &- \lambda\Bigg[\sum_{m\neq d}^K\sum_{n=1}^{D_m} \beta_n^m\cdot\alpha_n^m \cdot (f_n^m)^2\cdot \left(\beta_j^d \prod_{k\neq \{m, d\}}^K \left(\sum_{i=1}^{D_{k}} \alpha_{i}^k\cdot f_{i}^k\right) + \alpha_j^d\prod_{k\neq \{m, d\}}^K\left(\sum_{i=1}^{D_{k}} \beta_{i}^k\cdot f_{i}^k\right)\right)\Bigg]\\
 \\
 0 = \frac{\partial}{\partial \lambda} &= \left(\sum_{d=1}^K\sum_{j=1}^{D_k}\left[\beta_{j}^d\cdot  \alpha_{j}^d\cdot (f_{j}^d)^2 \cdot \prod_{k \neq d}^K\left(\sum_{i=1}^{D_{k}} \beta_{i}^k \cdot f_{i}^k\right) \cdot \left(\sum_{i=1}^{D_{k}} \alpha_{i}^k\cdot f_{i}^k\right) \right] - K\cdot B\right) 
\end{aligned}
$$

$$
\begin{bmatrix}
\beta_1^2 &&&&\\
&\beta_2^2&&&\\
&&\beta_3^2&&\\
&&&\beta_1^1&\\
&&&&\beta_2^1\\
&&&&&\beta_3^1
\end{bmatrix}
\cdot 
\begin{bmatrix}
f_1^2 &\\
f_2^2 &\\
f_3^2 &\\
& f_1^1\\
& f_2^1\\
& f_3^1
\end{bmatrix}
\cdot
\begin{bmatrix}
f_1^1 & f_2^1 & f_3^1 &&&\\
&&&f_1^2 & f_2^2 & f_3^2 \\
\end{bmatrix}
\cdot 
\begin{bmatrix}
\beta_1^1\\
\beta_2^1\\
\beta_3^1\\
\beta_1^2\\
\beta_2^2\\
\beta_3^2
\end{bmatrix}
$$



### PID controller

* $e(t)$: difference in target spending and current spending of the dimension with **MAX** roas

$$
u(t) = K_pe(t) + K_d\frac{d}{dt}e(t) + K_i\int_{0}^te(\tau)d\tau
$$

### Constraints

* `impression` table refreshing frequecy is **daily**.
  * Start of **day 1**, we provide a sequence of bid factors between TTD allowed **MIN** and **MAX** bid prices for each bid dimension
  * During **day 1**, we bid using each bid factor $f_t$ for a **period of time** $h_t$.
  * After **day 1**,  collect
    * number of impressions $n_t$ won with $f_t$ during $h_t$.
    * compute the average impression cost for each $f_t$. 
    * estimate $\alpha$ and $\beta$ for each dimension.
  * Starting from **day 2**, bid with the estimated $\alpha$ and $\beta$. 
  * Retrain after a few days. 

## Q&A

1. how is budget allocated across **ad groups**? We need fixed budget for each ad group.
   1. Ans:
2. Checked ROAS for campaign `n3b53qu` for a given date
   1. The number of impressions **matched**
   2. Total spending **matched**
   3. Total revenue does ***not match*** because I don't use match rate to inflat **store sales**


3. Are changes of bid cap uniform across all dimensions?

### Motivations

* $b_i = b_0\cdot f_{i, budget\_pacing} \cdot f_{i, bid\_shading} \cdot f_i$
* We can never accurately predict the effect of bid factors as other factors can be adjusted beyond our control (**verify with TTD**).

![image 12.40.39 AM](/Users/h0l07zi/Downloads/image 12.40.39 AM.png)

#### Alternative design (not feasible)

Define bid factors for $K$ dimensions
$$
F_1 = 
\begin{bmatrix}
f_1^1\\
f_2^1\\
f_3^1
\end{bmatrix},

F_2 = \begin{bmatrix}
f_1^2\\
f_2^2\\
f_3^2
\end{bmatrix},
\ldots, 
F_K = \begin{bmatrix}
f_1^K\\
f_2^K\\
f_3^K
\end{bmatrix}.
\\

\text{Bid price} = b_0\cdot F_1\otimes F_2\otimes\dots\otimes F_K.
$$

$$
N_{3\times 3} = (\beta_1 \odot F_1) \cdot (\beta_2 \odot F_2)^\top\\

N_{3\times 3} = g( F_1 \cdot F_2^\top)

\\
$$

##### Issues:

1. Different dimensions have the same relationship between **bid price** and **volume**.
2. 

## 