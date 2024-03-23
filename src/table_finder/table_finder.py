import re
import pandas as pd

def table_finder(query: str)->pd.DataFrame:
    tables=[]
    
    table_pattern=r'(FROM|JOIN|INSERT INTO TABLE|INSERT INTO|INSERT OVERWRITE TABLE|INSERT OVERWRITE|CREATE TABLE IF NOT EXISTS|CREATE TABLE|ALTER TABLE|ALTER|DROP TABLE IF EXISTS|DROP TABLE)\s+([\S\.]+)'
    cte_pattern1=r"(WITH|\,)\s+([\w_]+)\s+AS"
    cte_pattern2=r"(\,)([\w_]+)\s+AS"
    
    query=re.sub(r'\s+', ' ', query)
    cte_names1=set([k[1] for k in set(re.findall(cte_pattern1, query.strip('\n').upper()))])
    cte_names2=set([k[1] for k in set(re.findall(cte_pattern2, query.strip('\n').upper()))])
    cte_names=cte_names1.union(cte_names2)
    table_names=set(re.findall(table_pattern, query.strip('\n').upper(), re.IGNORECASE))

    for i in table_names:
        if i[1] not in cte_names:
            tables.append((i[1].strip(';'), i[0]))
    
    return pd.DataFrame(tables, columns=["table_name", "table_position"])
