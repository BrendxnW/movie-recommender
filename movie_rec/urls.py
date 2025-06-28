from django.urls import path
from .import views
from .nlp_utils import *

urlpatterns = [
    path("", views.greet_view),
    path("greet/", views.greet_view, name="greet")
]