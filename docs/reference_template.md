{%- macro schema_summary(schema) -%}
    {%- if '$ref' in schema -%}
        {%- set ref_name=schema['$ref'].split('/')[3] -%}
        [{{ ref_name }}](#{{ ref_name|lower }})
    {%- elif schema['type'] == 'array' -%}
        [{{ schema_summary(schema['items']) }}]
    {%- elif 'oneOf' in schema -%}
        {%- for subschema in schema['oneOf'] -%}
            {{ schema_summary(subschema) }}
            {%- if not loop.last %} \| {% endif -%}
        {%- endfor -%}
    {%- elif 'additionalProperties' in schema -%}
        Map[`string`, {{ schema_summary(schema['additionalProperties']) }}]
    {%- elif 'type' in schema -%}
        `{{ schema['type'] }}`
    {%- else -%}
        any
    {%- endif -%}
{%- endmacro -%}

# Translator Reasoner API

## Components

{% for name, schema in schemas.items() -%}{%- if schema is mapping -%}
#### {{ name }} [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L{{ schema._start }}:L{{ schema._end }})

{% if 'description' in schema -%}
{{ schema.description }}
{% endif -%}
{% if schema.type != 'object' %}
`{{ schema.type }}`
{%- if schema.type == 'string' and 'pattern' in schema %} (pattern: `{{ schema.pattern }}`)
{%- endif %}
{% endif -%}
{%- if schema.type == 'object' %}
##### Fixed Fields

Field Name | Type | Description
---|:---:|---
{% for prop_name, prop_schema in schema['properties'].items() -%}{%- if prop_schema is mapping -%}
    {{ prop_name }} | {{ schema_summary(prop_schema) }} | {% if prop_name in schema.required %}**REQUIRED**. {% endif -%}
    {{ prop_schema.description }}
{% endif %}{%- endfor %}
{% endif -%}
{%- if 'example' in schema %}
##### Example

```json
{{ schema.example|tojson(indent=4) }}
```

{% endif -%}
{%- endif -%}{%- endfor -%}
