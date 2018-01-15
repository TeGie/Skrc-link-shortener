from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent
from shorty.forms import SubmitUrlForm
from shorty.models import SkrcUrl


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SubmitUrlForm()
        ctx = {'form': form}
        return render(request, 'shorty/home.html', ctx)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        ctx = {'form': form}
        template = 'shorty/home.html'

        if form.is_valid():
            url = form.cleaned_data.get('url')
            obj, created = SkrcUrl.objects.get_or_create(url=url)
            ctx = {
                'object': obj,
                'created': created,
            }
            if created:
                template = 'shorty/success.html'
            else:
                template = 'shorty/already-exists.html'

        return render(request, template, ctx)


class SkrcRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(SkrcUrl, shortcode=shortcode)
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
