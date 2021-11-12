from django.urls import path
from .views import (HomePageView,
                    PaintAppView,
                    ResultPageView,
                    DeleteCategoryView,
                    paint,
                    random_temp)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('draw/<int:pk>/', PaintAppView.as_view(), name='paint_app'),
    path('delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete_view'),
    path('thanks/', ResultPageView.as_view(), name='result_page'),
    path('save/', paint, name='save_image'),
    path('random/', random_temp, name='random_temp'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
]
