
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
 * <p>Original spec-file type: CopyPaletteParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "from_workspace",
    "to_workspace"
})
public class CopyPaletteParams {

    @JsonProperty("from_workspace")
    private String fromWorkspace;
    @JsonProperty("to_workspace")
    private String toWorkspace;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("from_workspace")
    public String getFromWorkspace() {
        return fromWorkspace;
    }

    @JsonProperty("from_workspace")
    public void setFromWorkspace(String fromWorkspace) {
        this.fromWorkspace = fromWorkspace;
    }

    public CopyPaletteParams withFromWorkspace(String fromWorkspace) {
        this.fromWorkspace = fromWorkspace;
        return this;
    }

    @JsonProperty("to_workspace")
    public String getToWorkspace() {
        return toWorkspace;
    }

    @JsonProperty("to_workspace")
    public void setToWorkspace(String toWorkspace) {
        this.toWorkspace = toWorkspace;
    }

    public CopyPaletteParams withToWorkspace(String toWorkspace) {
        this.toWorkspace = toWorkspace;
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
        return ((((((("CopyPaletteParams"+" [fromWorkspace=")+ fromWorkspace)+", toWorkspace=")+ toWorkspace)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
