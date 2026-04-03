{%- macro schema_summary(schema) -%}
    {%- if '$ref' in schema -%}
        {%- set ref_name=schema['$ref'].split('/')[3] -%}
        [{{ ref_name }}](#{{ ref_name|lower }}-)
    {%- elif schema['type'] == 'array' -%}
        Array\[{{ schema_summary(schema['items']) }}\]
    {%- elif 'oneOf' in schema -%}
        {%- for subschema in schema['oneOf'] -%}
            {{ schema_summary(subschema) }}
            {%- if not loop.last %} \| {% endif -%}
        {%- endfor -%}
    {%- elif 'allOf' in schema -%}
        {%- for subschema in schema['allOf'] -%}
            {{ schema_summary(subschema) }}
            {%- if not loop.last %} \| {% endif -%}
        {%- endfor -%}
    {%- elif 'additionalProperties' in schema -%}
        Map\[`string`, {{ schema_summary(schema['additionalProperties']) }}\]
    {%- elif 'type' in schema -%}
        `{{ schema['type'] }}`
    {%- else -%}
        any
    {%- endif -%}
{%- endmacro -%}
{%- macro props_table(props, schema) -%}
| Field Name | Type | Description |
| --- | :---: | --- |
{% for prop_name, prop_schema in props.items() -%}{%- if prop_schema is mapping -%}
    | {{ prop_name }} | {{ schema_summary(prop_schema) }} | {% if 'required' in schema and prop_name in schema.required %}**REQUIRED**. {% endif -%}
            {% if 'minProperties' in prop_schema %}**Minimum properties: {{ prop_schema.minProperties }}.** {% endif -%}
            {% if 'minItems' in prop_schema %}**Minimum items: {{ prop_schema.minItems }}.** {% endif -%}
        {{ prop_schema.description }} |
{% endif %}{% endfor %}
{%- endmacro -%}

# Translator Reasoner API

## Components

{% for name, schema in schemas.items() -%}{%- if schema is mapping -%}
#### {{ name }} [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/{{ sha }}/TranslatorReasonerAPI.yaml#L{{ schema._start }}:L{{ schema._end }})

{% if 'description' in schema -%}
    {{ schema.description }}
{% endif -%}
{% if 'type' in schema and schema.type != 'object' -%}
    `{{ schema.type }}`
{%- if schema.type == 'string' and 'pattern' in schema %} (pattern: `{{ schema.pattern }}`)
{%- endif %}
{% endif -%}
{% if 'enum' in schema %}
one of:

{% for option in schema.enum -%}
- {{ option }}
{% endfor %}
{% endif -%}
{%- if schema.type == 'object' -%}
{% if 'properties' in schema -%}
##### Fixed Fields

{{ props_table(schema['properties'], schema) }}
{% endif -%}
{%- if 'patternProperties' in schema %}
##### Pattern Fields

{{ props_table(schema['patternProperties'], schema) }}
{% endif -%}
{% endif -%}
{%- if 'example' in schema %}
##### Example

```json
{{ schema.example|tojson(indent=4) }}
```

{% endif -%}
{%- if 'allOf' in schema %}{% for subschema in schema['allOf'] %}
{%- if '$ref' in subschema %}
{%- set ref_name=subschema['$ref'].split('/')[3] %}

*Inherits from:* [{{ ref_name }}](#{{ ref_name|lower }}-)
{% endif -%}
{%- if 'properties' in subschema %}
##### Fixed Fields

{{ props_table(subschema['properties'], subschema) }}
{% endif -%}
{%- if 'patternProperties' in subschema %}
##### Pattern Fields

{{ props_table(subschema['patternProperties'], subschema) }}
{% endif -%}
{% endfor %}{% endif -%}
{%- endif -%}{%- endfor -%}
