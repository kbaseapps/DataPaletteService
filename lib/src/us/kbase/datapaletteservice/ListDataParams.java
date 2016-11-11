
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
 * <p>Original spec-file type: ListDataParams</p>
 * <pre>
 * workspaces - list of workspace names or IDs (converted to strings),
 * include_metadata - if 1, includes object metadata, if 0, does not. Default 0.
 * TODO: pagination?
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspaces",
    "include_metadata"
})
public class ListDataParams {

    @JsonProperty("workspaces")
    private List<String> workspaces;
    @JsonProperty("include_metadata")
    private Long includeMetadata;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspaces")
    public List<String> getWorkspaces() {
        return workspaces;
    }

    @JsonProperty("workspaces")
    public void setWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
    }

    public ListDataParams withWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
        return this;
    }

    @JsonProperty("include_metadata")
    public Long getIncludeMetadata() {
        return includeMetadata;
    }

    @JsonProperty("include_metadata")
    public void setIncludeMetadata(Long includeMetadata) {
        this.includeMetadata = includeMetadata;
    }

    public ListDataParams withIncludeMetadata(Long includeMetadata) {
        this.includeMetadata = includeMetadata;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((("ListDataParams"+" [workspaces=")+ workspaces)+", includeMetadata=")+ includeMetadata)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
