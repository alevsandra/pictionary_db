import time

import simplejson
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, DeleteView
from .models import TempCategory, Drawing, Category


class HomePageView(TemplateView):
    template_name = 'home.html'
    model = TempCategory


class PaintAppView(DetailView):
    template_name = 'paint_app.html'
    model = TempCategory

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet random category
        context['model'] = TempCategory.objects.all()
        context['category'] = TempCategory.objects.get(
            pk=min(TempCategory.objects.filter().values_list('pk', flat=True)))
        if TempCategory.objects.count() > 1:
            context['new_category'] = TempCategory.objects.get(
                pk=min(TempCategory.objects.filter().values_list('pk', flat=True)) + 1)
        else:
            context['new_category'] = TempCategory.objects.get(
                pk=min(TempCategory.objects.filter().values_list('pk', flat=True)))
        return context


class ResultPageView(TemplateView):
    template_name = 'result_page.html'


class DeleteCategoryView(SuccessMessageMixin, DeleteView):
    model = TempCategory

    def get_success_url(self, **kwargs):
        if TempCategory.objects.exists():
            return reverse_lazy('paint_app',
                                kwargs={'pk': min(TempCategory.objects.filter().values_list('pk', flat=True)) + 1})
        else:
            return reverse_lazy('result_page')

    def delete(self, request, *args, **kwargs):
        self.object = TempCategory.objects.get(pk=min(TempCategory.objects.filter().values_list('pk', flat=True)))
        name = self.object.name
        request.session['name'] = name  # name will be change according to your need
        message = request.session['name'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DeleteCategoryView, self).delete(request, *args, **kwargs)


@csrf_exempt
def paint(request):
    if request.method == 'POST':
        category_name = request.POST['category']
        for record in Category.objects.all():
            if record.name == category_name:
                current_category = record
        image = request.POST['save_image']
        if not Drawing.objects.filter(picture=image).exists():
            file_data = Drawing(category=current_category, time=time.time(), picture=image)
            file_data.save()
        return HttpResponseRedirect('/')


@csrf_exempt
def random_temp(request):
    if request.method == 'POST':
        # adding randomly to model TempCategory 5 categories
        while len(TempCategory.objects.all()) < 5:
            s = Category.objects.random()
            if not TempCategory.objects.filter(name=s).exists():
                TempCategory.objects.create(name=s)
        # picking up the first category with the smallest id
        category_f = TempCategory.objects.get(
            pk=min(TempCategory.objects.filter().values_list('pk', flat=True)))
        # forwarding first category id to request response
        json_dump = simplejson.dumps({'pid': category_f.pk})
        return HttpResponse(json_dump, content_type='application/json')
