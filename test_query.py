from elasticsearch import Elasticsearch

es = Elasticsearch("http://<VM_ip_address>:9200")
# es.info().body

resp = es.search(
  _source =  ["genre","ethnicity","year",'cast'],  # set the fields that want to get
  
  index= "movies",  # set index
  
  size = 50,  # set the size to display
  
  # set the query by each want to search, find from kibana dev tools
  query={
      "query_string": {
      "query": "(drama romance) AND (american tamil) AND (year:(>=2010)) AND (james)",
      "fields": [
        "genre",
        "ethnicity",
        "cast"
      ]
    }
  }          
)

print("Got %d Hits:" % resp['hits']['total']['value'])

for hit in resp['hits']['hits']:
  print(hit["_source"])