from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent
from shorty.forms import SubmitUrlForm
from shorty.models import SkrcUrl


class HomeView(View):
    form_class = SubmitUrlForm
    template = 'shorty/home.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            url = form.cleaned_data.get('url')
            obj, created = SkrcUrl.objects.get_or_create(url=url)
            ctx = {
                'object': obj,
                'created': created,
            }
            self.template = 'shorty/shortcode.html'

        return render(request, self.template, ctx)


class SkrcRedirectView(View):
    def get(self, request, shortcode):
        obj = get_object_or_404(SkrcUrl, shortcode=shortcode)
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)
