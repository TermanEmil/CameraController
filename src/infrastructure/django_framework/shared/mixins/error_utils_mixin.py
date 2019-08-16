from django.shortcuts import render


class ErrorUtilsMixin:
    error_template = 'shared/error_page.html'

    def render_to_error(self, request, error: str):
        context = {'error': error}
        return render(request=request, template_name=self.error_template, context=context)