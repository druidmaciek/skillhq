from django.template import Context, Template


def test_markdown_tag():
    context = Context({'content': '# Markdown tag test'})
    template_to_render = Template(
        '{% load dashboard_tags %}'
        '{{ content|markdown }}'
    )
    rendered_template = template_to_render.render(context)
    print(rendered_template)
    assert "<h1>Markdown tag test</h1>" in rendered_template
