#!/usr/bin/env python
# placehoder module for Elasticsearch ingest operations


import requests
from elasticsearch import Elasticsearch



class ElasticsearchCluster(object):
    def __init__(self):
        self._hosts = []


    def add_host(self, hostname):
        self._hosts.append(hostname)


    @property
    def hosts(self):
        return self._hosts



class ElasticsearchDBClient(object):
    def __init__(self, es_cluster, port, **kwargs):
        self._es_client = None
        self._cluster = es_cluster
        self._port = port


    def connect(self, username, password, **kwargs):
        self._es_client = Elasticsearch(self._cluster.hosts,
                                        http_auth=(username, password),
                                        port=self._port,
                                        use_ssl=kwargs.get('use_ssl' or False))


    @property
    def instance(self):
        return self._es_client



    def index_doc(self, index_name, doctype, id, json_doc):
        self._es_client.index(index=index_name,
                              doc_type=doctype,
                              id=id,
                              body=json_doc)


    def get_doc(self, index, id):
        return self._es_client.get(index=index, id=id)



class ESQuery(object):
    def __init__(self):
        pass



class ESQueryBuilder(object):
    def __init__(self):
        pass


    def build(self):
        return ESQuery()


