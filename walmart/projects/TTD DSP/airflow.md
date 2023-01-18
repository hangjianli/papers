Tree View

sequential tasks 

Graph View

- Blocks: 
  - task
  - color around the box



### Start airflow task

Turn on --> refresh --->  completed tasks 

check logs to see if anything wrong

#### install package

```python
# Airflow config (in _task.py)
'machineTypeSubFamily="highmem",masterMachineTypeCores=16,workerMachineTypeCores=16,extraArgs="--properties=^#^dataproc:pip.packages=TimezoneFinder==5.2.0"'
```

<img src="/Users/h0l07zi/Library/Application Support/typora-user-images/Screen Shot 2022-10-03 at 4.21.01 PM.png" alt="Screen Shot 2022-10-03 at 4.21.01 PM" style="zoom:33%;" />

#### Files need to update after updating DAG

Constants 

- JOB





### Design



```python
def retrieve_impression_data():
  pass


@dag(schedule_interval='@daily', start_date)
def train_dag():
  
  @task()
  def get_impression_data():
    pass
  
  @task()
  def feature_processing():
    pass
  
  @task()
  def estimate_parameters():
    pass
  
  
  features = feature_processing(get_impression_data())
  estimate_parameters(features[], features[])
  
train = train_dag()
  
  
  

  
```

### Output

bid factor table 

```
+-----------+-----------+----------------+----------------+----------+
|campaign_id|ad_group_id|dimension_grp_id|bid_factor_value|      date|
+-----------+-----------+----------------+----------------+----------+
|    zw1rqnj|    fiin6x9|        region_1|          0.7629|2022-09-28|
|    zw1rqnj|    fiin6x9|        region_2|          0.7799|2022-09-28|
|    zw1rqnj|    fiin6x9|        region_3|           0.833|2022-09-28|
|    zw1rqnj|    fiin6x9|          site_1|          1.5778|2022-09-28|
|    zw1rqnj|    fiin6x9|          site_2|           1.207|2022-09-28|
|    zw1rqnj|    fiin6x9|          site_3|          0.4263|2022-09-28|
|    zw1rqnj|    fiin6x9|          site_4|          0.3072|2022-09-28|
|    zw1rqnj|    fiin6x9|          site_5|          1.8238|2022-09-28|
|    zw1rqnj|    fiin6x9|   hour_of_day_1|          1.0322|2022-09-28|
|    zw1rqnj|    fiin6x9|   hour_of_day_2|           0.942|2022-09-28|
|    zw1rqnj|    fiin6x9|   hour_of_day_3|          1.4439|2022-09-28|
|    zw1rqnj|    fiin6x9|       weekday_1|          0.9266|2022-09-28|
|    zw1rqnj|    fiin6x9|       weekday_2|          1.0009|2022-09-28|
+-----------+-----------+----------------+----------------+----------+
```





### test items 

- [x] read all 3 tables
- [x] install and import packages
- [x] write to table
- [ ] task chaining

