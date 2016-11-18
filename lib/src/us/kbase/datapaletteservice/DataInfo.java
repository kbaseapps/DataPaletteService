
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
import us.kbase.common.service.Tuple11;


/**
 * <p>Original spec-file type: DataInfo</p>
 * <pre>
 * dp_ref - reference to DataPalette container pointing to given object,
 * dp_refs - full list of references to DataPalette containers that
 *     point to given object (in contrast to dp_ref which shows only
 *     first item from dp_refs list).
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "info",
    "dp_ref",
    "dp_refs"
})
public class DataInfo {

    @JsonProperty("ref")
    private java.lang.String ref;
    @JsonProperty("info")
    private Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> info;
    @JsonProperty("dp_ref")
    private java.lang.String dpRef;
    @JsonProperty("dp_refs")
    private List<String> dpRefs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ref")
    public java.lang.String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(java.lang.String ref) {
        this.ref = ref;
    }

    public DataInfo withRef(java.lang.String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("info")
    public Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> getInfo() {
        return info;
    }

    @JsonProperty("info")
    public void setInfo(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> info) {
        this.info = info;
    }

    public DataInfo withInfo(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> info) {
        this.info = info;
        return this;
    }

    @JsonProperty("dp_ref")
    public java.lang.String getDpRef() {
        return dpRef;
    }

    @JsonProperty("dp_ref")
    public void setDpRef(java.lang.String dpRef) {
        this.dpRef = dpRef;
    }

    public DataInfo withDpRef(java.lang.String dpRef) {
        this.dpRef = dpRef;
        return this;
    }

    @JsonProperty("dp_refs")
    public List<String> getDpRefs() {
        return dpRefs;
    }

    @JsonProperty("dp_refs")
    public void setDpRefs(List<String> dpRefs) {
        this.dpRefs = dpRefs;
    }

    public DataInfo withDpRefs(List<String> dpRefs) {
        this.dpRefs = dpRefs;
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
        return ((((((((((("DataInfo"+" [ref=")+ ref)+", info=")+ info)+", dpRef=")+ dpRef)+", dpRefs=")+ dpRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
