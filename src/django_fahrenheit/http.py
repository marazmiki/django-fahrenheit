from django import http


class HttpResponseUnavailableForLegalReason(http.HttpResponse):
    status_code = 451
    reason_phrase = "Unavailable For Legal Reasons"


__all__ = ['HttpResponseUnavailableForLegalReason']

