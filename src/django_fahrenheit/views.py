from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.csrf import requires_csrf_token

from .http import HttpResponseUnavailableForLegalReason

ERROR_451_TEMPLATE_NAME = '451.html'
DEFAULT_ = """<html>
 <head><title>Unavailable For Legal Reasons</title></head>
 <body>
  <h1>Unavailable For Legal Reasons</h1>
  <p>This request may not be serviced For Legal Reasons</p>
 </body>
</html>
"""


@requires_csrf_token
def unavailable_for_legal_reasons(
        request,
        template_name=ERROR_451_TEMPLATE_NAME
):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_451_TEMPLATE_NAME:
            raise
        return HttpResponseUnavailableForLegalReason(
            DEFAULT_,
            content_type='text/html'
        )
    return HttpResponseUnavailableForLegalReason(
        template.render(
            request=request,
            context={}
        )
    )
