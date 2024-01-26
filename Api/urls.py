from django.urls import path
from Api import views_ris, views_esis
from .views import ItemListCreateView
from .views_esis import *

urlpatterns = [
    path('accreditation-records/', ItemListCreateView.as_view(), name='item-list-create'),

    path('esis/extension/records/', views_esis.extension_info, name='extension-info'),
] 