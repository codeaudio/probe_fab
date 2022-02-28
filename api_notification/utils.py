import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template


def fetch_pdf_resources(uri, rel):
    if uri.find(settings.STATIC_URL) != -1:
        return os.path.join(
            settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, '')
        )


def render_to_pdf(template_src, context=None):
    from xhtml2pdf import pisa

    if context is None:
        context = {}
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode('utf-8')), result,
        link_callback=fetch_pdf_resources
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
