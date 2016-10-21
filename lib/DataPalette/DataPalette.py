


from pprint import pprint

from biokbase.workspace.client import Workspace


class WorkspaceInfo():
    def __init__(self, info):
        self.id = info[0]
        self.name = info[1]
        self.owner = info[2]
        self.moddate = info[3]
        self.n_objects = info[4]
        self.user_permission = info[5]
        self.globalread = info[6]
        self.lockstat = info[7]
        self.metadata = info[8]


class DataPalette():

    PROVENANCE = [{'service':'DataPaletteService'}]
    DATA_PALETTE_WS_METADATA_KEY = 'data_palette_id'

    def __init__(self, ws_name_or_id, ws_url=None, token=None):
        if ws_url is None:
            raise ValueError('ws_url was not defined')
        if token is None:
            print('DataPalette warning: token was not set')
        self.ws = Workspace(ws_url, token=token)

        if str(ws_name_or_id).isdigit():
            self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({'id':int(ws_name_or_id)}))
        else:
            self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({'workspace':str(ws_name_or_id)}))

        self.palette_ref = None


    def list(self, options):
        # if there is no data palette, return nothing
        dp_ref = self._get_root_data_palette_ref()
        if dp_ref is None:
            return []

        palette = self._get_data_palette()
        palette = self._attach_palette_data_info(palette)

        return palette['data']


    def add(self, refs=None):

        objs = self._get_object_info(refs)

        palette = self._get_data_palette()
        data_index = self._build_palette_data_index(palette['data'])

        for o in objs:
            ws = str(o[6])
            obj = str(o[0])
            ver = str(o[4])
            ref = ws+'/'+obj+'/'+ver

            if ws+'/'+obj in data_index:
                # the object is in the palette, so check versions
                index = data_index[ws+'/'+obj]
                if index['ver'] == ver:
                    # the version didn't change, so continue
                    continue
                # the version is different, so update it
                data_index[ws+'/'+obj]['ver'] = ver
                palette['data'][index['idx']]['ref'] = ref

            else:
                # the object wasn't in the palette, so add it
                idx = len(palette['data'])
                palette['data'].append({'ref':ref })
                data_index[ws+'/'+obj] = {'ver':ver, 'idx':idx}

        self._save_data_palette(palette)
        return

        

    def remove(self):
        dp_ref = self._get_root_data_palette_ref()
        if dp_ref is None:
            raise ValueError('Cannot remove from data_palette')

        return


    def _build_palette_data_index(self, palette_data):
        data_index = {}
        for k in range(0,len(palette_data)):
            tokens = palette_data[k]['ref'].split('/')
            key = tokens[0] + '/' + tokens[1]
            value = {'ver': tokens[2], 'idx': k }
            data_index[key] = value
        return data_index



    def _get_object_info(self, objects):
        return self.ws.get_object_info_new({'objects':objects })


    def _attach_palette_data_info(self, palette):
        #TODO: make sure we get object info via reference chain
        if len(palette['data'])==0:
            return palette

        all_info = self.ws.get_object_info_new({
                                'objects':palette['data'],
                                'includeMetadata':1
                            })

        for k in range(0,len(all_info)):
            palette['data'][k]['info'] = all_info[k]

        return palette



    def _save_data_palette(self, palette):
        obj_info = self.ws.save_objects({
                'id':self.ws_info.id,
                'objects': [{
                    'type': 'DataPalette.DataPalette-0.1',
                    'objid': self._get_root_data_palette_objid(),
                    'data': palette,
                    'provenance': self.PROVENANCE,
                    'hidden': 1
                }]
            })[0]
        return obj_info


    def _get_data_palette(self):
        palette_ref = self._get_root_data_palette_ref()
        if palette_ref is None:
            return self._create_data_palette()
        data = self.ws.get_objects2({
                'objects':[{'ref':palette_ref}]
            })
        return data['data'][0]['data']


    def _create_data_palette(self):
        # 1) save the data_palette object
        palette = { 'data':[] }
        obj_info = self.ws.save_objects({
                'id':self.ws_info.id,
                'objects': [{
                    'type':'DataPalette.DataPalette-0.1',
                    'name':'data_palette',
                    'data': palette,
                    'provenance':self.PROVENANCE,
                    'hidden':1
                }]
            })[0]

        # 2) update ws metadata
        self.ws.alter_workspace_metadata({
                            'wsi':{
                                'id': self.ws_info.id
                            },
                            'new': {
                                self.DATA_PALETTE_WS_METADATA_KEY : str(obj_info[0])
                            }
                        })

        # 3) refresh local ws info
        self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({'id':self.ws_info.id}))
        return palette


    def _get_root_data_palette_objid(self):
        ref = self._get_root_data_palette_ref()
        if ref is None:
            return None
        return self._get_root_data_palette_ref().split('/')[1]

    def _get_root_data_palette_ref(self):
        if self.palette_ref is not None:
            return self.palette_ref
        if self.DATA_PALETTE_WS_METADATA_KEY not in self.ws_info.metadata:
            return None
        dp_id = self.ws_info.metadata[self.DATA_PALETTE_WS_METADATA_KEY]
        self.palette_ref = str(self.ws_info.id) + '/' + str(dp_id)
        return self.palette_ref











