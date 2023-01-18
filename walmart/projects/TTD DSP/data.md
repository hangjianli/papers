1. 

2. 

3. Is there actually sigfinificant difference between  `14-day` and `30-day` attribution methods?

   1. How many impressions on average are needed to reach conversion?
   2. How does the number of impressions change as we trace back in time after conversion?

4. 

   

## Issues

The same `impression_id` in the impression tbl and attributed sales can be mapped to different `luid`. 

```python
data_processor = DataProcesser(spark, external_campaign_id='zw1rqnj')
camp_imp = data_processor.load_campaign_impressions_coredata(map_to_luid=True).repartition(1024)

campaign_attr_sales = (
    data_processor.get_attr_trans_camp()
    .repartition(1024, 'impression_id')
    .filter(F.col('attribution_strategy') == 'fair14partner')
)

(
    camp_imp
    .filter(F.col('impression_id') == '343d0236-dca8-4b1e-810e-9d17b0e01b8d')
    .join(campaign_attr_sales, on=['impression_id'], how='inner')
    .show()
)

(
    camp_imp
    .filter(F.col('impression_id') == '343d0236-dca8-4b1e-810e-9d17b0e01b8d')
    .join(campaign_attr_sales, on=['impression_id', 'luid'], how='inner')
    .show()
)
```

For the same impression, `impression` table and `attr_sales` table map to different luid

* `impression_id = 343d0236-dca8-4b1e-810e-9d17b0e01b8d`
* 

​	



## Mapping between `impression` and `transaction`

* 
* transactions to impression: **many to many**
  * one trans/order_id to many impression: **attributed weight**
  * one impression to many orders: **transaction dates**
* same impression was mapped to two different `LUID`s
  * <img src="/Users/h0l07zi/Desktop/Screen Shot 2022-09-10 at 4.39.35 PM.png" alt="Screen Shot 2022-09-10 at 4.39.35 PM" style="zoom: 35%;" />
* <img src="/Users/h0l07zi/Desktop/Screen Shot 2022-09-10 at 4.47.07 PM.png" alt="Screen Shot 2022-09-10 at 4.47.07 PM" style="zoom:35%;" />
* Number of duplicated impressions (mapped to 2 or more luids) is 657   
  * total impression: $1702498$.
  * total impression with sales: $1172901$.
* 



