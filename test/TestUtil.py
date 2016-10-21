import os
import time
import json
import requests

from os import environ
from pprint import pprint

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from biokbase.workspace.client import Workspace
from DataPaletteService.DataPaletteServiceServer import MethodContext

class TestUtil():

    def __init__(self, verbose=True):
        self._setup_ctx()
        self._load_kb_config()
        self._ws = None
        self.workspaces = []
        self.verbose = verbose


    def _setup_ctx(self):
        self.token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(self.token)).json()['user_id']
        self._ctx = MethodContext(None)
        self._ctx.update({'token': self.token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'DataPaletteService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})

    def _load_kb_config(self):
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        self._cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('DataPaletteService'):
            self._cfg[nameval[0]] = nameval[1]

    def _log(self, mssg):
        if self.verbose:
            print("TESTUTIL: " + str(mssg))


    def ctx(self):
        '''
            WARNING: don't call any logging methods on the test context object,
            it'll result in a NoneType error
        '''
        return self._ctx

    def ws(self):
        if not self._ws:
            self.wsURL = self.cfg('workspace-url')
            self._ws = Workspace(self.wsURL, token=self.token)
            self._log('Initialized WS client to url:' + str(self.wsURL))
        return self._ws


    def cfg(self, key):
        return self._cfg[key]

    def full_cfg(self):
        return self._cfg


    def createWorkspace(self):
        suffix = int(time.time() * 1000)
        ws_name = "test_DataPaletteService_" + str(suffix)
        self.ws().create_workspace({'workspace':ws_name})
        self._log('Created new test WS:' + str(ws_name))
        self.workspaces.append(ws_name)
        return ws_name


    def getAnyWsName(self):
        if len(self.workspaces)==0:
            createWorkspace()
        return self.workspaces[0]


    def cleanup(self):
        for ws_name in self.workspaces:
            self.ws().delete_workspace({'workspace': ws_name})
            self._log('Deleted test WS:' + str(ws_name))



