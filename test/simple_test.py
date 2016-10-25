# -*- coding: utf-8 -*-
import unittest
import os

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from DataPaletteService.DataPaletteServiceImpl import DataPaletteService
from DataPaletteService.DataPaletteServiceServer import MethodContext

from TestUtil import TestUtil

class SimpleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_util = TestUtil()
        cls.serviceImpl = DataPaletteService(cls.test_util.full_cfg())

    @classmethod
    def tearDownClass(cls):
        cls.test_util.cleanup()

    def getImpl(self):
        return self.__class__.serviceImpl

    def ctx(self):
        return self.test_util.ctx()

    def ws(self):
        return self.test_util.ws()


    def load_object_data(self, ws_name):
        objects = [{
                    'type':'Empty.AType',
                    'data': { 'foo':5 },
                    'name':'A1',
                    'meta':{'meta':'yes'}
                },{
                    'type':'Empty.AType',
                    'data': { 'foo':5 },
                    'name':'A2',
                    'meta':{'meta':'no'}
                },{
                    'type':'Empty.AType',
                    'data': { 'foo':5 },
                    'name':'A3',
                    'meta':{'meta':'maybe'}
                }]

        objs_info = self.ws().save_objects({
                'workspace':ws_name,
                'objects': objects
            })

        objs = []
        for info in objs_info:
            objs.append({
                    'abs_ref': str(info[6]) + '/' + str(info[0]) + '/' + str(info[4]),
                    'relative_ref': str(info[7]) + '/' + str(info[1]),
                    'info':info
                })
        return objs



    def test_basic_add_remove_from_new_palette(self):
        dps = self.getImpl()

        # create an empty workspace, make sure we get empty list
        ws_name1 = self.test_util.createWorkspace()
        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1]})[0]
        self.assertIn('data', d)
        self.assertEqual(len(d['data']),0)

        # create objects in a different WS, add one to the palette
        ws_name2 = self.test_util.createWorkspace()
        objs = self.load_object_data(ws_name2)

        dps.add_to_palette(self.ctx(),{
                'workspace':ws_name1,
                'new_refs':[{
                    'ref': objs[0]['relative_ref']
                }]
            })

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1]})[0]
        pprint(d)
        self.assertIn('data', d)
        self.assertEqual(len(d['data']),1)
        self.assertEqual(d['data'][0]['ref'], objs[0]['abs_ref'])

        # load the objects again so we have multiple versions of these objects
        objsV2 = self.load_object_data(ws_name2)
        objsV3 = self.load_object_data(ws_name2)

        # add two more to the palette
        dps.add_to_palette(self.ctx(),{
                'workspace':ws_name1,
                'new_refs':[{
                    'ref': objsV2[1]['abs_ref']
                },{
                    'ref': objsV3[2]['relative_ref']
                }]
            })

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1]})[0]
        pprint(d)
        self.assertEqual(len(d['data']),3)
        self.assertEqual(d['data'][0]['ref'], objs[0]['abs_ref'])
        self.assertEqual(d['data'][1]['ref'], objsV2[1]['abs_ref'])
        self.assertEqual(d['data'][2]['ref'], objsV3[2]['abs_ref'])

        # add one more to the palette, which should update a reference
        dps.add_to_palette(self.ctx(),{
                'workspace':ws_name1,
                'new_refs':[{
                    'ref': objsV3[0]['relative_ref']
                }]
            })

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1]})[0]
        pprint(d)
        self.assertEqual(len(d['data']),3)
        self.assertEqual(d['data'][0]['ref'], objsV3[0]['abs_ref'])
        self.assertEqual(d['data'][1]['ref'], objsV2[1]['abs_ref'])
        self.assertEqual(d['data'][2]['ref'], objsV3[2]['abs_ref'])

        # try to add a reference to a prohibited object, should throw an error
        obj_info = self.ws().save_objects({
                'workspace':ws_name2,
                'objects': [{
                    'type': 'KBaseReport.Report',
                    'name': 'report',
                    'data': {'text_message':'hello', 'objects_created':[]}
                }]
            })[0]
        with self.assertRaises(ValueError) as error:
            dps.add_to_palette(self.ctx(),{
                            'workspace':ws_name1,
                            'new_refs':[{'ref': ws_name2 + '/report'}]
                        })
        self.assertTrue('cannot be added to a data palette' in str(error.exception))

        
        # try to remove from the data palette
        dps.remove_from_palette(self.ctx(),{
                'workspace':ws_name1,
                'refs':[{
                    'ref': objsV3[0]['abs_ref']
                }]
            })
        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1]})[0]
        self.assertEqual(len(d['data']),2)
        self.assertEqual(d['data'][0]['ref'], objsV2[1]['abs_ref'])
        self.assertEqual(d['data'][1]['ref'], objsV3[2]['abs_ref'])


        # try to copy the data palette
        ws_name3 = self.test_util.createWorkspace()
        dps.copy_palette(self.ctx(),{
                'from_workspace':ws_name1,
                'to_workspace':ws_name3
            })

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name3]})[0]
        self.assertEqual(len(d['data']),2)
        self.assertEqual(d['data'][0]['ref'], objsV2[1]['abs_ref'])
        self.assertEqual(d['data'][1]['ref'], objsV3[2]['abs_ref'])

        dps.add_to_palette(self.ctx(),{
                'workspace':ws_name3,
                'new_refs':[{
                    'ref': objsV3[0]['relative_ref']
                }]
            })
        d = dps.list_data(self.ctx(),{'workspaces':[ws_name3]})[0]
        self.assertEqual(len(d['data']),3)
        self.assertEqual(d['data'][0]['ref'], objsV2[1]['abs_ref'])
        self.assertEqual(d['data'][1]['ref'], objsV3[2]['abs_ref'])
        self.assertEqual(d['data'][2]['ref'], objsV3[0]['abs_ref'])






