#!/usr/bin/env python

import unittest
from context import lyra
import logging
import sys



class TestTuneFileIngest(unittest.TestCase):
    def test_ingest_tune_from_file_to_es(self):

        log = logging.getLogger('lyra')
        index_name = 'test_index'

        host = '54.175.142.35'
        cluster = lyra.ElasticsearchCluster().add_host(host)
        es_client = lyra.ElasticsearchDBClient(cluster)
        es_client.connect('', '')
        log.debug('Connected to elasticsearch instance at %s' % host)

        loader = lyra.ESTuneLoader(index_name, es_client)

        initial_num_docs = es_client.get_doc_count(index_name, 'abc_tune')
        

        loader.load_tunefile('../sample.abc')
        es_client.instance.indices.refresh(index=index_name)

        final_num_docs = es_client.get_doc_count(index_name, 'abc_tune')
        #log.debug('%d documents in index.' % num_docs)

        self.assertEqual(1, final_num_docs - initial_num_docs)



if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger('lyra').setLevel( logging.DEBUG )
    unittest.main()



