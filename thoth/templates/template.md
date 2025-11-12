# Main document
{% for line in template.lines %}
{{ line }}
{% endfor %}

# You can also use
{% raw %}
{{ source }} - the document rendered

{{ timestamp.strftime("%Y/%m/%d %H:%M") }} - the date and time the document was rendered
{% endraw %}
