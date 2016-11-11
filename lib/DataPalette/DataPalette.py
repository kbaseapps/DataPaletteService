
from Workspace.WorkspaceClient import Workspace


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

    PROVENANCE = [{'service': 'DataPaletteService'}]
    DATA_PALETTE_WS_METADATA_KEY = 'data_palette_id'
    DEFAULT_PALETTE_OBJ_NAME = 'data_palette'
    PALETTE_OBJ_WS_TYPE = 'DataPalette.DataPalette'

    # set of types that cannot be added to a data palette, add to configuration
    PROHIBITED_DATA_TYPES = ['KBaseReport.Report',
                             'KBaseNarrative.Narrative',
                             'DataPalette.DataPalette']

    def __init__(self, ws_name_or_id, ws_url=None, token=None, ws_info=None, ws=None):
        if ws:
            self.ws = ws
        else:
            if ws_url is None:
                raise ValueError('ws_url was not defined')
            if token is None:
                print('DataPalette warning: token was not set')
            self.ws = Workspace(ws_url, token=token)

        if ws_info:
            if ws_name_or_id:
                raise ValueError("Either ws_name_or_id or ws_info should be set")
            self.ws_info = WorkspaceInfo(ws_info)
        else:
            if str(ws_name_or_id).isdigit():
                self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({'id': int(ws_name_or_id)}))
            else:
                self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({
                                                                    'workspace': str(ws_name_or_id)
                                                                    }))

        self.palette_ref = None

    def list(self, options):
        # if there is no data palette, return nothing
        dp_ref = self._get_root_data_palette_ref()
        if dp_ref is None:
            return []

        palette = self._get_data_palette()
        include_metadata = options.get('include_metadata', 0)
        palette = self._attach_palette_data_info(palette, include_metadata)

        return palette['data']

    def add(self, refs=None):
        '''
        Adds the provided references to the data palette.
        '''
        if len(refs) == 0:
            return {}

        # make sure the references to add are visible and valid
        objs = self._get_object_info(refs)
        self._validate_objects_to_add(objs)

        # get the existing palette and build an index
        palette = self._get_data_palette()
        data_index = self._build_palette_data_index(palette['data'])

        # perform the actual update palette update
        for o in objs:
            ws = str(o[6])
            obj = str(o[0])
            ver = str(o[4])
            ref = ws + '/' + obj + '/' + ver

            if ws + '/' + obj in data_index:
                # the object is in the palette, so check versions
                index = data_index[ws + '/' + obj]
                if index['ver'] == ver:
                    # the version didn't change, so continue
                    continue
                # the version is different, so update it
                data_index[ws + '/' + obj]['ver'] = ver
                palette['data'][index['idx']]['ref'] = ref

            else:
                # the object wasn't in the palette, so add it
                idx = len(palette['data'])
                palette['data'].append({'ref': ref})
                data_index[ws + '/' + obj] = {'ver': ver, 'idx': idx}

        # save the updated palette and return
        self._save_data_palette(palette)
        return {}

    def remove(self, refs=None):
        dp_ref = self._get_root_data_palette_ref()
        if dp_ref is None:
            raise ValueError('Cannot remove from data_palette- data palette ' +
                             'for Workspace does not exist')

        if len(refs) == 0:
            return {}

        # right now, we only match on exact refs, so this works
        palette = self._get_data_palette()
        data_index = self._build_palette_data_index(palette['data'])

        index_to_delete = []
        for r in range(0, len(refs)):
            ref = refs[r]['ref']
            tokens = ref.split('/')
            if len(tokens) != 3:
                raise ValueError('Invalid absolute reference: ' + str(ref) + ' at position ' + str(r) +
                                 ' of removal list.  References must be full, absolute numerical WS refs.')
            is_digits = map(lambda x: x.isdigit(), tokens)
            if False in is_digits:
                raise ValueError('Invalid absolute reference: ' + str(ref) + ' at position ' + str(r) +
                                 ' of removal list.  References must be full, absolute numerical WS refs.')
            ws_slash_id = tokens[0] + '/' + tokens[1]
            if ws_slash_id in data_index:
                if data_index[ws_slash_id]['ver'] == tokens[2]:
                    index_to_delete.append(data_index[ws_slash_id]['idx'])
                else:
                    raise ValueError('Reference: ' + str(ref) + ' at position ' + str(r) +
                                     ' of removal list was not found in palette.  Object exists, but ' +
                                     'version was not correct.')
            else:
                raise ValueError('Reference: ' + str(ref) + ' at position ' + str(r) +
                                 ' of removal list was not found in palette.')

        index_to_delete = set(index_to_delete)
        for i in sorted(index_to_delete, reverse=True):
            del palette['data'][i]

        self._save_data_palette(palette)

        return {}


    def _build_palette_data_index(self, palette_data):
        data_index = {}
        for k in range(0, len(palette_data)):
            tokens = palette_data[k]['ref'].split('/')
            key = tokens[0] + '/' + tokens[1]
            value = {'ver': tokens[2], 'idx': k}
            data_index[key] = value
        return data_index


    def _get_object_info(self, objects):
        return self.ws.get_object_info_new({'objects': objects})


    def _validate_objects_to_add(self, object_info_list):
        for info in object_info_list:
            # validate type, split and ignore the type version
            full_type_name = info[2].split('-')[0]
            if full_type_name in self.PROHIBITED_DATA_TYPES:
                raise ValueError('Object ' + str(info[1]) + ' (id=' + str(info[6]) + '/' +
                                 str(info[0]) + '/' + str(info[4]) + ') is a type (' + full_type_name +
                                 ') that cannot be added to a data palette.')


    def _attach_palette_data_info(self, palette, include_metadata = 0):
        # TODO: make sure we get object info via reference chain
        if len(palette['data']) == 0:
            return palette

        all_info = self.ws.get_object_info_new({
                                               'objects': palette['data'],
                                               'includeMetadata': include_metadata
                                               })

        for k in range(0, len(all_info)):
            palette['data'][k]['info'] = all_info[k]

        return palette


    def _save_data_palette(self, palette):
        obj_info = self.ws.save_objects({
                                        'id': self.ws_info.id,
                                        'objects': [{
                                            'type': self.PALETTE_OBJ_WS_TYPE,
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
                                    'objects': [{'ref': palette_ref}]
                                    })
        return data['data'][0]['data']


    def _create_data_palette(self):
        # 1) save the data_palette object
        palette = {'data': []}
        new_palette_info = self.ws.save_objects({
                                                'id': self.ws_info.id,
                                                'objects': [{
                                                    'type': self.PALETTE_OBJ_WS_TYPE,
                                                    'name': self.DEFAULT_PALETTE_OBJ_NAME,
                                                    'data': palette,
                                                    'provenance': self.PROVENANCE,
                                                    'hidden': 1
                                                }]
                                                })[0]

        # 2) update ws metadata
        self._update_ws_palette_metadata(new_palette_info)
        return palette

    def create_from_existing_palette(self, existing_data_palette):
        # 1) make sure we can actually do it
        dp_target_ref = self._get_root_data_palette_ref()
        if dp_target_ref is not None:
            raise ValueError('Cannot copy data_palette- a data palette already exists in that workspace.')

        dp_source_ref = existing_data_palette._get_root_data_palette_ref()
        if dp_source_ref is None:
            # data palette did not exist, so we don't have to copy over anything
            return {}

        # 2) make the copy
        new_palette_info = self.ws.copy_object({
                                               'from': {'ref': dp_source_ref},
                                               'to': {'wsid': self.ws_info.id, 'name': self.DEFAULT_PALETTE_OBJ_NAME}
                                               })

        # 3) update ws metadata
        self._update_ws_palette_metadata(new_palette_info)
        return {}


    def set_palette_to_obj(self, new_data_palette_name_or_id):

        if new_data_palette_name_or_id is None:
            new_data_palette_name_or_id = self.DEFAULT_PALETTE_OBJ_NAME

        new_palette_ref = str(self.ws_info.id) + '/' + str(new_data_palette_name_or_id)
        new_palette_info = self._get_object_info([{'ref': new_palette_ref}])[0]

        if not str(new_palette_info[2]).startswith(self.PALETTE_OBJ_WS_TYPE):
            raise ValueError('Cannot set data palette for workspace to non-palette type.  Type of (' +
                             new_palette_ref + ') was: ' + str(new_palette_info[1]))

        self._update_ws_palette_metadata(new_palette_info)
        return {}


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
        if not str(dp_id).isdigit():
            raise ValueError('Warning: WS metadata for ' + str(self.ws_info.id) +
                             'was corrupted.  It is not set to an object ID.  It was: ' + str(dp_id))
        self.palette_ref = str(self.ws_info.id) + '/' + str(dp_id)
        return self.palette_ref

    def _update_ws_palette_metadata(self, palette_obj_info):
        self.ws.alter_workspace_metadata({
                                         'wsi': {
                                             'id': self.ws_info.id
                                         },
                                         'new': {
                                             self.DATA_PALETTE_WS_METADATA_KEY: str(palette_obj_info[0])
                                         }
                                         })
        # refresh local ws info
        self.ws_info = WorkspaceInfo(self.ws.get_workspace_info({'id': self.ws_info.id}))
