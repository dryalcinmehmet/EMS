# http://elasticsearch-dsl.readthedocs.io/en/stable/search_dsl.html
# https://github.com/sabricot/django-elasticsearch-dsl
# https://github.com/elastic/elasticsearch-dsl-py/blob/master/docs/search_dsl.rst
from elasticsearch import Elasticsearch

client = Elasticsearch(['elasticsearch:9200'])
