from django.urls import path
from .views import ItemListCreateView

urlpatterns = [
    path('accreditation-records/', ItemListCreateView.as_view(), name='item-list-create'),
]