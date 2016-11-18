# -*- coding: utf-8 -*-
import unittest
import os
import time
import json

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from DataPaletteService.DataPaletteServiceImpl import DataPaletteService
from DataPaletteService.DataPaletteServiceServer import MethodContext
from DataPalette.DataPalette import DataPalette

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
        self.assertIn('data_palette_refs', d)
        self.assertEqual(len(d['data_palette_refs']),0)

        # create objects in a different WS, add one to the palette
        ws_name2 = self.test_util.createWorkspace()
        objs = self.load_object_data(ws_name2)

        dps.add_to_palette(self.ctx(),{
                'workspace':ws_name1,
                'new_refs':[{
                    'ref': objs[0]['relative_ref']
                }]
            })

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1], 'include_metadata': 1})[0]

        self.assertIn('data', d)
        self.assertEqual(len(d['data']),1)
        self.assertEqual(d['data'][0]['ref'], objs[0]['abs_ref'])
        self.assertIsNotNone(d['data'][0]['info'][10])
        self.assertIsNotNone(d['data'][0]['dp_ref'])
        self.assertIn('data_palette_refs', d)
        self.assertEqual(len(d['data_palette_refs']),1)
        ws_id1 = self.test_util.ws().get_workspace_info({'workspace': ws_name1})[0]
        dp_ref = d['data_palette_refs'][str(ws_id1)]
        dp_type = self.test_util.ws().get_object_info_new({'objects': [{'ref': dp_ref}]})[0][2]
        self.assertTrue(dp_type.startswith("DataPalette.DataPalette"))

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

        self.assertEqual(len(d['data']),3)
        self.assertEqual(d['data'][0]['ref'], objs[0]['abs_ref'])
        self.assertIsNone(d['data'][0]['info'][10])
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

        # corrupt the WS, and list_data should produce an error:
        self.ws().alter_workspace_metadata({
                            'wsi':{ 'workspace': ws_name3 },
                            'new': { DataPalette.DATA_PALETTE_WS_METADATA_KEY : '' }
                        })
        with self.assertRaises(ValueError) as error:
            dps.list_data(self.ctx(),{'workspaces':[ws_name3]})[0]
        self.assertTrue('was corrupted.  It is not set to an object ID.' in str(error.exception))

        # but we can fix!
        dps.set_palette_for_ws(self.ctx(),{'workspace':ws_name3})
        d = dps.list_data(self.ctx(),{'workspaces':[ws_name3]})[0]
        self.assertEqual(len(d['data']),3)
        
        # Let's delete ws_name2 and check that we can list objects from there fixed in DP ws_name1
        ws_id2 = self.test_util.ws().get_workspace_info({'workspace': ws_name2})[0]
        self.test_util.workspaces.remove(ws_name2)
        self.test_util.ws().delete_workspace({'workspace': ws_name2})
        d = dps.list_data(self.ctx(),{'workspaces':[ws_name1], 'include_metadata': 1})[0]
        self.assertIn('data', d)
        self.assertTrue(len(d['data']) > 0)
        for item in d['data']:
            self.assertEqual(item['info'][6], ws_id2)


    def test_unique_list_items(self):
        dps = self.getImpl()

        # Creating original workspace
        ws_name1 = self.test_util.createWorkspace()
        obj = self.load_object_data(ws_name1)[0]
        obj_ref = obj['abs_ref']
        #obj_info = obj['info']

        # Creating two workspaces with DPs
        ws_name2 = self.test_util.createWorkspace()
        dps.add_to_palette(self.ctx(),{'workspace':ws_name2,
                                       'new_refs':[{'ref': obj_ref}]})
        ws_name3 = self.test_util.createWorkspace()
        dps.add_to_palette(self.ctx(),{'workspace':ws_name3,
                                       'new_refs':[{'ref': obj_ref}]})

        d = dps.list_data(self.ctx(),{'workspaces':[ws_name2, ws_name3]})[0]
        self.assertIn('data', d)
        self.assertEqual(len(d['data']), 1)
        self.assertIn('data_palette_refs', d)
        self.assertEqual(len(d['data_palette_refs']), 2)
        dp_cnt_refs = [d['data_palette_refs'][key] for key in d['data_palette_refs']]
        self.assertTrue('dp_refs' in d['data'][0])
        self.assertEqual(len(d['data'][0]['dp_refs']), 2)
        for dp_cnt_ref in dp_cnt_refs:
            self.assertTrue(dp_cnt_ref in d['data'][0]['dp_refs'])
        

    def test_bulk_list_sets(self):
        ids = []
        for ws_info in self.ws().list_workspace_info({'perm': 'r', 'excludeGlobal': 1}):
            if ws_info[4] < 1000:
                ids.append(str(ws_info[0]))
            else:
                print("Workspace: " + ws_info[1] + ", size=" + str(ws_info[4]) + " (skipped)")

        print("Number of workspaces for bulk list_data: " + str(len(ids)))
        t1 = time.time()
        ret = self.getImpl().list_data(self.ctx(), {'workspaces': ids})[0]['data']
        print("Objects found: " + str(len(ret)) + ", time=" + str(time.time() - t1))
