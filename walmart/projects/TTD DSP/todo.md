2022/10/13

TTD pipeline improvement

- [x] Add message to show what campaign and adgroup is the experiment for.

- [ ] Access BC table directly from airflow using `dev_adhoc_ds` SA.

  - [x] test in GCP
  - [ ] test in airflow

- [ ] Implement parameter estimation for multiple bid factors

  - [x] Step1. test in GCP

  - [ ] Step2. test in airflow

  - Issues:

    		1. Unseen values
    	
     	- Region:  where I saw Canadian regions? Isn’t it supposed to be US?
    	
     	- Revenue per impression (use one average for now: total rev / total count)
    	
    		2. Solution

         - wait for a week and ignore them from then

         - In the future: Frequent  pattern match optimization

           

- [ ] Implement  mapping between my dimension and TTD IDs. 

  - [ ] geo
  - [ ] site
  - [ ] Hour of day
  - [ ] day of week
  - [ ] adformat
  - [ ] 

1. Total     cost = Media cost + extra fees. These fees are not constant (% of bid +     constants)

 

```python
  def poke(self, context):
        self.logger.info("Updated cluster name is: %s", self._cluster_name)
        self.create()
        encoded_sa = get_sa_key(self._service_account)

        # print(f"encoded_sa is {encoded_sa}")
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(encoded_sa, strict=False), scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
        ds = list(self.partition_with_values.values())[0]
        # Submit a job to Dataproc
        # gcloud dataproc jobs submit pyspark --cluster=$CLUSTER_NAME --region=$REGION \
        #   run/script.py
        query_statement = "SELECT substring(Time, 0, 10) as ds, AdUnitId, \
                        REGEXP_EXTRACT(CustomTargeting, r'location=(.*?);') AS LocationKeyValue, \
                        CURRENT_DATE('America/Los_Angeles') AS Created_dt FROM \
                        `wmt-84fe52fae01cc3d4b5e52e8625.wmg_dfp.NetworkImpressions`\
                        where substring(Time, 0, 10)='" + ds + "' LIMIT 5"
        query_job = client.query(query_statement)
        result = query_job.result().to_dataframe()
        if result.shape[0] > 0:
            return True
        else:
            return False
```







Airflow notes:

1. change airflow ENV here

   <img src="/Users/h0l07zi/Desktop/Screen Shot 2022-10-13 at 10.15.18 AM.png" alt="Screen Shot 2022-10-13 at 10.15.18 AM" style="zoom:33%;" /> 

2. 



Access big query errors:

1. `BigQueryRelationProvider could not be instantiated`
   * Fix: spark version needs to be v.3.
   * 
2. 



presentation

- Overview: one sentence
  - sales lift is an important metric to understand the effectiveness of our campaigns
  - The actual number is never observed. But it's not a constant. Based on sampling. it's always subject to mistakes. 
  - false negatives and false positives.
- SLR estimator 
  - How many impressions are needed to 
  - power analysis
    - difficulties
      1. find luids that's represetnative of the control
      2. Seasonality, campaign duration, item sets, etc. 
      3. estimate the $\mu_1$ and $\mu_2$ as well their variances for the campaign period. 
      4. 
    - 















