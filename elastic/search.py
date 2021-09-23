import s3fs
import json
import sys
from elasticsearch import Elasticsearch

def connect_s3():
    fs = s3fs.S3FileSystem(anon=False, key='AKIA4LXXODBPO7CCDV36', secret='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')
    return fs

def create_index(es):
    request_body = {
    	"settings": {
            "index.mapping.total_fields.limit": 20000,
		    "number_of_shards": 1,
   	        "number_of_replicas": 0,
            "analysis": {
            "analyzer": {
            "autocomplete": {
            "tokenizer": "autocomplete",
            "filter": [
                "lowercase"
            ]
            },
            "autocomplete_search": {
            "tokenizer": "lowercase"
            }
        },
        "tokenizer": {
            "autocomplete": {
            "type": "edge_ngram",
            "min_gram": 2,
            "max_gram": 10,
            "token_chars": [
                "letter"
            ]
            }
        }
        }
    },
    "mappings": {
        "properties": {
        "table_name": {
            "type": "text",
            "analyzer": "autocomplete",
            "search_analyzer": "autocomplete_search"
        },
        "Table Summary": {
            "type": "text",
            "analyzer": "autocomplete",
            "search_analyzer": "autocomplete_search"
        },
        "Table Description": {
            "type": "text",
            "analyzer": "autocomplete",
            "search_analyzer": "autocomplete_search"
        },
        "url": {
            "type": "text",
            "analyzer": "autocomplete",
            "search_analyzer": "autocomplete_search"
        },
        "column":{
            "type": "nested",
            "properties": {
            "column_name": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search"
            }
            }
        }
    }
    }
    }
    print("creating index")
    es.indices.create(index = 'ssadocs', body = request_body)

def post_elastic(build_doc):
    es = Elasticsearch()
    if not es.indices.exists(index="ssadocs"):
        create_index(es)
    try:
        res = es.index(index="ssadocs", body=build_doc)
        print("\nclient.index response:", json.dumps(res, indent=4))
    except Exception as e:
        print(e)

def main():
    fs = connect_s3()

    # Uploads all files from said bucket
    with fs.open('rhbidevaida/search.json', 'rb') as f:
        data = f.read()

    # To upload a local file uncomment the two lines below and adjust the path
    #with open('/home/codebind/Documents/elastic/search.json', 'rb') as f:
    #    data = f.read() 

    dict_ = json.loads(data)
    # remove "table" key from data
    rm_table_key = dict_.get('table')
    # build doc for each table and post it to elasticsearch
    for table_name in rm_table_key:
        build_doc = {}
        columns_list = []
        build_doc["table_name"] = table_name
        for table_data in rm_table_key.get(table_name):
            if table_data == "column":
                for column_name in rm_table_key.get(table_name).get('column'):
                    build_column_doc = {}
                    build_column_doc["column_name"] = column_name
                    for column_data in rm_table_key.get(table_name).get(table_data).get(column_name):
                        build_column_doc[column_data] = rm_table_key.get(table_name).get(table_data).get(column_name).get(column_data)
                    columns_list.append(build_column_doc)
                build_doc['column'] = columns_list
            else:
                build_doc[table_data] = rm_table_key.get(table_name).get(table_data)
            post_elastic(build_doc)
    # removes "table" key

if __name__ == "__main__":
    main()
