from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductView.as_view(), name = "products"),
    path('<str:id>', views.ProductView.as_view(), name = "product"),
]
