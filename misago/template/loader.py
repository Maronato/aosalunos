from django.template.loader import render_to_string as django_render_to_string
from misago.template.theme import prefix_templates
from misago.template.middlewares import process_context

def render_to_string(template_name, dictionary=None, context_instance=None):
    dictionary = process_context(template_name, dictionary, context_instance)
    template_name = prefix_templates(template_name)
    return django_render_to_string(template_name, dictionary)
