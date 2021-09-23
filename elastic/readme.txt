Demo The ElasticSearch Engine

1. Install python dependency
pip install -r requirement.txt

2. install docker using below link
https://docs.docker.com/engine/install/

3. Install docker-compose file.
https://docs.docker.com/compose/install/
-Make sure to edit the /etc/sysctl.conf by adding vm.max_map_count=262144 at the end of the file to expand the elasticsearch limit

To run the container run these two commands
sudo docker-compose up -d
python3 search.py

After the elastic container finishes loading you can navigate to this

http://localhost:5601/app/dev_tools#/console

and run each query individually

Here are some sample queries:

GET _search
{
  "query": {
    "match_all": {}
  }
}

GET _cat/indices
DELETE ssadocs

GET ssadocs/_search
{ 
  "query": {
    "match": {
      "table_name": {
        "query": "fin"
      }
    }
  }
}


GET ssadocs/_search
{ 
  "query": {
    "match": {
      "Table Summary": {
        "query": "opportuni"
      }
    }
  }
}



GET ssadocs/_search
{
  "query": {
    "nested": {
      "path": "column",
      "query": {
        "match": {
          "column.column_name": {"query": "bill"}
        }
      }
    }
  }
}
