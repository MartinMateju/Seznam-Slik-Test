USER = 'root'    
PASSWORD = 'seznam123'
HOST = 'db'
PORT = '3306'
DB_TEST = 'MYSQLTEST'
QUERY_INSERT_CLICK = """INSERT INTO clicks (clickTimestamp, impressionId) VALUES (%s, %s) """
QUERY_INSERT_IMPRESSION = """INSERT INTO impressions (impressionTime, impressionId, adId, visitorHash) VALUES (%s, %s, %s, %s) """
QUERY_GET_IMPRESSIONS = """SELECT COUNT(adId) FROM impressions WHERE adId={ad_id} AND impressionTime between '{date} 00:00:00' and '{date} 23:59:00'"""
QUERY_GET_CLICKS = """
with recursive d as (
      select impressionId, clickTimestamp,
             min(clickTimestamp) over (order by `clickTimestamp`
                             range between interval 10 minute following and unbounded following
                            ) as next_time
      from clicks
     ),
     clicks(impressionId, clickTimestamp, next_time) as (
      (select impressionId, clickTimestamp, next_time
       from d 
       order by clickTimestamp
       limit 1
      ) union all
      select d.impressionId, d.clickTimestamp, d.next_time
      from clicks join
           d 
           on d.clickTimestamp = clicks.next_time
      )
select count(distinct(impressionId)) from clicks WHERE clickTimestamp LIKE '{date}%'
"""