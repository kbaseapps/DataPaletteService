/*
    Definition of the WS object for 
*/
module DataPalette {

    /* @id ws */
    typedef string ws_ref;

    typedef structure {
        ws_ref ref;
    } DataReference;

    typedef structure {
        list <DataReference> data;
    } DataPalette;
};
