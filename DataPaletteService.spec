
#include <workspace.spec>

/*

*/
module DataPaletteService {

    /* @id ws */
    typedef string ws_ref;

    typedef structure {
        ws_ref ref;
        Workspace.object_info info;
    } DataInfo;

    typedef structure {
        list <DataInfo> data;
    } DataList;


    typedef string ws_name_or_id;

    /* todo: pagination? */
    typedef structure {
        list <ws_name_or_id> workspaces;
    } ListDataParams;

    funcdef list_data(ListDataParams params)
        returns (DataList data_list) authentication optional;


    /* todo: allow passing in a reference chain */
    typedef structure {
        ws_ref ref;
    } ObjectReference;

    typedef structure {
        ws_name_or_id workspace;
        list <ObjectReference> new_refs;
    } AddToPaletteParams;

    funcdef add_to_palette(AddToPaletteParams params)
        returns () authentication required;


    typedef structure {
        ws_name_or_id workspace;
        list <ws_ref> refs;
    } RemoveFromPaletteParams;

    funcdef remove_from_palette(RemoveFromPaletteParams params)
        returns () authentication required;
};
