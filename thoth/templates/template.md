# Main document
{% for line in template.lines %}
{{ line }}
{% endfor %}

# You can also use

## Fragments

{% raw -%}

{{ fragments.title[language] }}

{{ fragments.chapter.one[language] }}

{{ fragments.chapter.two[language] }}

{{ fragments.copyright[language] }}

{%- endraw %}

## Rendering info

{% raw -%}

{{ source }} - the document rendered

{{ timestamp.strftime("%Y/%m/%d %H:%M") }} - the date and time the document was rendered

{%- endraw %}
