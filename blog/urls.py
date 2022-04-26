from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^contact$', views.ContactPage.as_view(), name='contact')


]