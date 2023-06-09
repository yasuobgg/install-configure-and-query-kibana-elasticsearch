# Install-configure-and-query-kibana-elasticsearch
install on ubuntu 22.04 run on VM
all steps folllow [the page](https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-elastic-stack-on-ubuntu-22-04)

* to make ELK accessed on host machine
- in the elasticsearch configure(/etc/elasticsearch/elasticsearch.yml)
```python
# ---------------------------------- Cluster -----------------------------------
cluster.name: node-1
cluster.initial_master_nodes: node-1

# ---------------------------------- Network -----------------------------------
network.host: 0.0.0.0
```

- in the kibana configure(/etc/kibana/kibana.yml)
```python
server.port: 5601
server.host: 0.0.0.0
elasticsearch.hosts: ["http://localhost:9200"]
```

# Discover kibana
- on local machine, access http://<VM_ip>:5601
## in the Dev-tools:
- Show all indexes
```python
GET _cat/indices?v
```
- Get all data of an index(eg:employees)
```python
GET employees/_search
{ 
  "query": {
    "match_all": {}
  }
}
```
- Query data by datetime(eg: date_of_birth greater than or equal 1986/01/01)
```python
POST employees/_search
{
  "query": {
    "range": {
      "date_of_birth": {
        "gte": "1986-01-01"
      }
    }
  }
}
```
- Query a string that match many values in a field(tamil or amrican or bollywood in field: ethnicity)
```python
POST movies/_search
{
  "_source": ["genre","ethnicity"], # the field that data will return
  "size": 100, # get 100 elements
  "from": 1,  # from the 2nd element
  "query": {
    "bool": {
      "should": [
        {"match": {
          "ethnicity": "tamil american bollywood"
        }
        }
      ]
    }
  }
}
```
- Query a string that match excatly in the field(only bolywood in field:ethnicity)
```python
POST movies/_search
{
  "_source": ["genre","ethnicity"], 
  "size": 100,
  "from": 1, 
  "query": {
    "match_phrase": {
      "ethnicity": "Bollywood"
    }
  }
}
```
- Query to fetch the field contain the given string
```python
GET movies/_search
{
  "_source": ["director"],
  "query": {
    "prefix": {
      "director": "se" # Start must be Se..., can be seperated by `space`
    }
  }
}
```
- Query wildcard pattern 
```python
GET movies/_search
{
  "_source": ["ethnicity"], 
  "query": {
    "wildcard": {
      "ethnicity": {
        "value": "*am*"  # fields must contains the `am` in the body, eg: american, malayam, tamil,... 
      }
    }
  }
}
```
- Sort the movies index based on their descending order of year
```python
GET movies/_search
{
  "_source": ["title","year"], 
  "sort": [
    {
      "year": {
        "order": "desc" # desc means decending, asc means ascending
      }
    }
  ]
}
```
- bool query (query index movies (genre = drama or genre = romance) and (ethnicity = american or ethnicity = tamil) and (year >= 2010))
```python
POST movies/_search
{
  "_source": ["genre","ethnicity","year"], 
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {
                "match": {
                  "genre": "drama"
                }
              },
              {
                "match": {
                  "genre": "romance"
                }
              }
            ]
          }
        },
        {
          "bool": {
            "should": [
              {
                "match": {
                  "ethnicity": "american"
                }
              },
              {
                "match": {
                  "ethnicity": "tamil"
                }
              }
            ]
          }
        },
   {
          "bool": {
            "must": [
              {
                "range": {
                  "year": {
                    "gte": 2010
                  }
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

or can be query by query_string(for short)
```python
POST movies/_search
{
  "_source": ["title","genre","ethnicity","year"], 
  "query": {
    "query_string": {
      "query": "(drama romance) AND (american tamil) AND (year:(>=2010))",
      "fields": [
        "genre",
        "ethnicity"
      ]
    }
  }
}
```