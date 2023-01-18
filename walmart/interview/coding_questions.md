# Interview question



## Coding

**implement Naive Bayes from scratch**

```python

def normal_dist(x , mean , sd):
    prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density



class NaiveBayes:
  def fit(self, X, y):
    n_samples, n_features = X.shape
    self._classes = np.unique(y)
    n_classes = len(self._classes)
    
    
    self._mean = 
    self._var = 
    self._prior = 
    
    
    for c in self._classes:
      self._prior = X_c.shape[0] / float(n_samples)
    
    
    
  def predict(self, X):
    """
    Args: X: ndarray
    """
    return y_pred
  
  
  def _predict(self, X):
    posteriors = []
    
    for idx, c enumerate(self._classes):
      prior = np.log(self._prior(idx))
   
  
 def _pdf(self, class_idx, x):
     numerator = np.exp(-(x-mean)**2 /(2*var))
     denominator = 

# scipy.stats.norm(0, 1).pdf(0)
    
    return self._classes[np.argmax(posteriors)]
  
  
  
  dataset = [[3.393533211,2.331273381,0],
	[3.110073483,1.781539638,0],
	[1.343808831,3.368360954,0],
	[3.582294042,4.67917911,0],
	[2.280362439,2.866990263,0],
	[7.423436942,4.696522875,1],
	[5.745051997,3.533989803,1],
	[9.172168622,2.511101045,1],
	[7.792783481,3.424088941,1],
	[7.939820817,0.791637231,1]]
```





#### Suppose we know there were N rats born and died within 100 days or M days. Their birth and death days are stored in N arrays [a, b]. What day has the most rats alive? 



```python
def day_with_max(mice):
	population_changes = [0] * 100
	for mouse in mice:
		population_changes[mouse[0]] +=1
		population_changes[mouse[1]] -= 1
	max_population = 0
	max_population_index = 0
	
	population=0
	for index, population_change in enumerate(population_changes):
		population += population_change
		if population > max_population:
			max_population = population
			max_population_index = index
	return max_population_index


# rats = [[1,10], [2,5], [10, 22], [3, 40], [1, 40]]

# mice = [[1,10], [2,5], [10, 22], [3, 40], [1, 40]]
# mice = [[0,99], [50,79], [80, 99], [81,82]]

```



```python
def flip(intervals, n=100):
    count = [0] * (n+1)
    for intv in intervals:
        count[intv[0]] += 1
        count[intv[1] + 1] += 1
    res = [0] * n
    if count[0] % 2 == 1:
        res[0] = 1
    for i in range(1, n):
        count[i] += count[i-1]
        if count[i] % 2 == 1:
            res[i] = 1
    return res

```

## Implement a weighted sampling method

Given: `dict = {'a':w1, 'b': w2, etc.}`





