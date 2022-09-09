from hashlib import algorithms_available
import logging

from helperFunctions.config import read_list_from_config
from helperFunctions.hash import get_hash, get_ssdeep, get_imphash
from analysis.PluginBase import AnalysisBasePlugin


class AnalysisPlugin(AnalysisBasePlugin):
    '''
    This Plugin creates several hashes of the file
    '''
    NAME = 'file_hashes'
    DEPENDENCIES = ['file_type']
    DESCRIPTION = 'calculate different hash values of the file'
    VERSION = '1.0'

    def __init__(self, plugin_administrator, config=None, recursive=True):
        '''
        recursive flag: If True recursively analyze included files
        default flags should be edited above. Otherwise the scheduler cannot overwrite them.
        '''
        self.config = config
        self.hashes_to_create = self._get_hash_list_from_config()

        # additional init stuff can go here

        super().__init__(plugin_administrator, config=config, recursive=recursive, plugin_path=__file__)

    def process_object(self, file_object):
        '''
        This function must be implemented by the plugin.
        Analysis result must be a dict stored in file_object.processed_analysis[self.NAME]
        If you want to propagate results to parent objects store a list of strings 'summary' entry of your result dict
        '''
        file_object.processed_analysis[self.NAME] = {}
        for h in self.hashes_to_create:
            if h in algorithms_available:
                file_object.processed_analysis[self.NAME][h] = get_hash(h, file_object.binary)
            else:
                logging.debug('algorithm {} not available'.format(h))

        # Skip these always-on FACT algos if we don't specifically request them.
        #
        # Glue tables (or any stray calls to the FACT compare plugin or storage)
        # may expect these so always add the keys and just skip the value.
        always_on_algos = [('ssdeep', get_ssdeep), ('imphash', get_imphash)]
        for algo_name, get_value_func in always_on_algos:
            algo_value = None  # default
            if algo_name in self.hashes_to_create:
                algo_value = get_value_func(file_object.binary)
            file_object.processed_analysis[self.NAME][algo_name] = algo_value
        return file_object

    def _get_hash_list_from_config(self):
        try:
            return read_list_from_config(self.config, self.NAME, 'hashes', default=['sha256'])
        except Exception:
            logging.warning("'file_hashes' -> 'hashes' not set in config")
            return ['sha256']
