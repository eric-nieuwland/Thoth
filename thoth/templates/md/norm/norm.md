{% if profile.identifier or profile.title -%}
# {% if profile.identifier -%}{{ norm.identifier }}{%- endif -%} {%- if profile.identifier and profile.title %} - {% endif -%}{%- if profile.title -%}{{ norm.title[language] }}{%- endif %}
{%- endif %}

{% if profile.intro -%}
{{ norm.intro[language] }}
{%- endif %}

{% if profile.scope -%}

## scope

{{ norm.scope[language] }}
{%- endif %}

{% if profile.triggers -%}

## triggers

{% if norm.triggers -%}
{% for trigger in norm.triggers -%}
- {{ trigger[language] }}
{%- endfor %}
{%- endif %}
{%- endif %}

{% if profile.criteria -%}

## criteria

{% if norm.criteria -%}
{% for criterium in norm.criteria -%}
- {{ criterium[language] }}
{%- endfor %}
{%- endif %}
{%- endif %}

{% if profile.objectives -%}

## objectives

{% if norm.objectives -%}
{% for objective in norm.objectives -%}
- {{ objective[language] }}
{%- endfor %}
{%- endif %}
{%- endif %}

{% if profile.risks -%}

## risks

{% if norm.risks -%}
{% for risk in norm.risks -%}
- {{ risk[language] }}
{%- endfor %}
{%- endif %}
{%- endif %}

{% if profile.drivers -%}

## drivers

{% if norm.drivers -%}
|{% for driver in norm.drivers %} {{ driver.name }} |{% endfor %}
|{% for driver in norm.drivers %} --- |{% endfor %}
|{% for driver in norm.drivers %} {% if driver.details -%}{%- for detail in driver.details %}{{ detail }}{% if not loop.last %}<br/>{% endif %}{% endfor %}{% endif %} |{% endfor %}
{%- endif %}
{%- endif %}

{% if profile.indicators -%}

## indicators

{% if norm.indicators -%}
{% for indicator in norm.indicators -%}
{% if profile.indicators.identifier or profile.indicators.title -%}

### {% if profile.indicators.identifier -%}{{ indicator.identifier }}{%- endif %} {% if profile.indicators.title -%} {{ indicator.title[language] }}{%- endif %}

{%- endif %}

{% if profile.indicators.description -%}
{{ indicator.description[language] }}
{%- endif %}

{%- if profile.indicators.conformities %}

#### conformity indicators

{% if indicator.conformities -%}
{% for conformity in indicator.conformities -%}
{% if profile.indicators.identifier %}{{ indicator.identifier }}{% endif -%}
{%- if profile.indicators.identifier and profile.indicators.conformities.identifier -%} / {%- endif -%}
{%- if profile.indicators.conformities.identifier %}{{ conformity.identifier }}{% endif %}
: {% if profile.indicators.conformities.description %}{{ conformity.description[language] }}{% endif %}
{% if profile.indicators.conformities.guidance -%}
{% if conformity.guidance -%}
: _{{ conformity.guidance[language] }}_
{% endif %}
{%- endif %}
{% endfor %}
{%- endif %}
{%- endif -%}
{% if profile.indicators.explanation -%}

#### explanation

{{ indicator.explanation[language] }}

{% endif %}
{%- endfor %}
{%- endif %}
{%- endif %}

{% if profile.references -%}

## references

{% if norm.references -%}
{% for reference in norm.references -%}
{% if profile.references.name -%}{{ reference.name }}{%- endif -%}
{%- if profile.references.name and profile.references.url and reference.url %} - {% endif -%}
{%- if profile.references.url -%}{%- if reference.url -%}[{{ reference.url }}]({{ reference.url }}){%- endif -%}{%- endif %}
{% if profile.references.notes -%}
{% if reference.notes %}
{% for note in reference.notes -%}
- {{ note[language] }}
{% endfor %}
{%- endif %}
{% endif %}

{%- endfor %}
{%- endif %}
{%- endif %}


rendered by Thoth on {{ timestamp.astimezone().strftime("%Y/%m/%d at %H:%M") }} in '{{ language }}' from {{ source }}
