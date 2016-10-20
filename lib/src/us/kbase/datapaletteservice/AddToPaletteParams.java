
package us.kbase.datapaletteservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: AddToPaletteParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace",
    "new_refs"
})
public class AddToPaletteParams {

    @JsonProperty("workspace")
    private String workspace;
    @JsonProperty("new_refs")
    private List<ObjectReference> newRefs;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace")
    public String getWorkspace() {
        return workspace;
    }

    @JsonProperty("workspace")
    public void setWorkspace(String workspace) {
        this.workspace = workspace;
    }

    public AddToPaletteParams withWorkspace(String workspace) {
        this.workspace = workspace;
        return this;
    }

    @JsonProperty("new_refs")
    public List<ObjectReference> getNewRefs() {
        return newRefs;
    }

    @JsonProperty("new_refs")
    public void setNewRefs(List<ObjectReference> newRefs) {
        this.newRefs = newRefs;
    }

    public AddToPaletteParams withNewRefs(List<ObjectReference> newRefs) {
        this.newRefs = newRefs;
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
        return ((((((("AddToPaletteParams"+" [workspace=")+ workspace)+", newRefs=")+ newRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
