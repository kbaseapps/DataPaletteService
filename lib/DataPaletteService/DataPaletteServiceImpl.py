# -*- coding: utf-8 -*-
#BEGIN_HEADER
#END_HEADER


class DataPaletteService:
    '''
    Module Name:
    DataPaletteService

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "HEAD"
    
    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        #END_CONSTRUCTOR
        pass
    

    def list_data(self, ctx, params):
        """
        :param params: instance of type "ListDataParams" (todo: pagination?)
           -> structure: parameter "workspaces" of list of type
           "ws_name_or_id"
        :returns: instance of type "DataList" -> structure: parameter "data"
           of list of type "DataInfo" -> structure: parameter "ref" of type
           "ws_ref" (@id ws), parameter "meta" of String, parameter "src_nar"
           of String
        """
        # ctx is the context object
        # return variables are: data_list
        #BEGIN list_data
        #END list_data

        # At some point might do deeper type checking...
        if not isinstance(data_list, dict):
            raise ValueError('Method list_data return value ' +
                             'data_list is not type dict as required.')
        # return the results
        return [data_list]

    def add_to_palette(self, ctx, params):
        """
        :param params: instance of type "AddToPaletteParams" -> structure:
           parameter "workspace" of type "ws_name_or_id", parameter
           "new_refs" of list of type "ObjectReference" (todo: allow passing
           in a reference chain) -> structure: parameter "ref" of type
           "ws_ref" (@id ws)
        """
        # ctx is the context object
        #BEGIN add_to_palette
        #END add_to_palette
        pass

    def remove_from_palette(self, ctx, params):
        """
        :param params: instance of type "RemoveFromPaletteParams" ->
           structure: parameter "workspace" of type "ws_name_or_id",
           parameter "refs" of list of type "ws_ref" (@id ws)
        """
        # ctx is the context object
        #BEGIN remove_from_palette
        #END remove_from_palette
        pass

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
