
package us.kbase.datapaletteservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: SetPaletteForWsParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace",
    "palette_name_or_id"
})
public class SetPaletteForWsParams {

    @JsonProperty("workspace")
    private String workspace;
    @JsonProperty("palette_name_or_id")
    private String paletteNameOrId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace")
    public String getWorkspace() {
        return workspace;
    }

    @JsonProperty("workspace")
    public void setWorkspace(String workspace) {
        this.workspace = workspace;
    }

    public SetPaletteForWsParams withWorkspace(String workspace) {
        this.workspace = workspace;
        return this;
    }

    @JsonProperty("palette_name_or_id")
    public String getPaletteNameOrId() {
        return paletteNameOrId;
    }

    @JsonProperty("palette_name_or_id")
    public void setPaletteNameOrId(String paletteNameOrId) {
        this.paletteNameOrId = paletteNameOrId;
    }

    public SetPaletteForWsParams withPaletteNameOrId(String paletteNameOrId) {
        this.paletteNameOrId = paletteNameOrId;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("SetPaletteForWsParams"+" [workspace=")+ workspace)+", paletteNameOrId=")+ paletteNameOrId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
