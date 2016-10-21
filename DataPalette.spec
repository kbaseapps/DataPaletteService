/*
    Definition of the WS object for 
*/
module DataPalette {

    /* @id ws */
    typedef string ws_ref;

    typedef structure {
        ws_ref ref;
    } DataReference;

    /*
        Note: will probably need a 'next' DataPalette object, otherwise
        max size of palette is 40k refs or something like that.
        @metadata ws length(data) as n
    */
    typedef structure {
        list <DataReference> data;
    } DataPalette;
};
