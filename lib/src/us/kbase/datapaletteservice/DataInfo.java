
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
 * <p>Original spec-file type: DataInfo</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "meta",
    "src_nar"
})
public class DataInfo {

    @JsonProperty("ref")
    private String ref;
    @JsonProperty("meta")
    private String meta;
    @JsonProperty("src_nar")
    private String srcNar;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ref")
    public String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(String ref) {
        this.ref = ref;
    }

    public DataInfo withRef(String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("meta")
    public String getMeta() {
        return meta;
    }

    @JsonProperty("meta")
    public void setMeta(String meta) {
        this.meta = meta;
    }

    public DataInfo withMeta(String meta) {
        this.meta = meta;
        return this;
    }

    @JsonProperty("src_nar")
    public String getSrcNar() {
        return srcNar;
    }

    @JsonProperty("src_nar")
    public void setSrcNar(String srcNar) {
        this.srcNar = srcNar;
    }

    public DataInfo withSrcNar(String srcNar) {
        this.srcNar = srcNar;
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
        return ((((((((("DataInfo"+" [ref=")+ ref)+", meta=")+ meta)+", srcNar=")+ srcNar)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
