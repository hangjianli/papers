# Deep Learning Fundamentals

## What's the difference between hidden markov model and RNN?







# Reinforcement Learning

#### Discounted return at $t$

$$
G_t = \sum_{k=t+1}^T\gamma^{k-t-1} R_k
$$



#### Q-function

* an *action-value function*.
* expected return starting from state $s$, following policy $\pi$, taking action $a$.

$$
Q^\pi(s, a) = \mathbb{E}_\pi[G_{t+1}\mid s, a] = \sum_{r}p(r\mid a, s)\cdot r + \gamma \sum_{s^\prime\in A}p(s^\prime\mid s, a) \cdot V^\pi(s^\prime)
$$

#### V-function

* an *state-value function*.
* expected return from state $s$ following policy $\pi$.


$$
V^\pi(s) = \sum_{a\in A} \pi(a\mid s)\cdot Q^\pi(s, a)
$$


#### Optimal Bellman equations


$$
V^*(s) = \max_a Q^*(s, a)
$$

$$
Q^*(s, a) = \sum_{r}p(r\mid a, s)\cdot r + \gamma \sum_{s^\prime\in A}p(s^\prime\mid s, a) \cdot V^*(s^\prime)
$$







## Q-learning

#### - *Find the optimal policy without knowing the model*

#### model-free

- no model for instantaneous reward 
- no model for dynamics



#### Solution

* given samples $s_t, s_t, r_{t+1}, s_{t+1}$ from the envrionment, update $Q$-values to try to satisfy Bellman equation.
* *off-policy*: samples don't have to be from the optimal policy.



1. Choose $a$ from $s$.
2. Take action $a$, observe $r, s^\prime$

$$
Q(s, a) \leftarrow Q(s, a) + \alpha\left[r + \gamma\max_{a^\prime} Q(s^\prime, a^\prime) - Q(s, a)\right]\\
s\leftarrow s^\prime;
$$

### Deep Q-learning

* a function approximator $Q(s, a; \theta)$. 

* Optimize

* $$
  \mathbb{E}_\rho\left[\|R + \gamma \max_{a^\prime}Q(S^\prime, a^\prime) - Q(s, a) \|_2^2\right]
  $$

  * $\rho$ is a distribution over states, depends on $\theta$.

* gradient descent

  * take some action $a_i$ and observe $(s_i, a_i, s_i^\prime, r_i)$.
    $$
    \begin{align}
    y_i &= r(s_i, a_i) + \gamma\max_{a^\prime}Q_\theta(s_i^\prime, a_i^\prime)\\
    \theta&\leftarrow \theta - \alpha \frac{\partial Q_\theta}{\partial \theta}(s_i, a_i)\cdot \left(Q_\theta(s_i, a_i) - y_i\right)
    \end{align}
    $$

  * 

* Stabilize the iteration by fixing a ***target network*** $Q_{\phi^\prime}$ for a few iterations.

  * xxx

* 

