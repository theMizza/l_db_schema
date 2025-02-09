from django.urls import path
from .views import sql_executor

urlpatterns = [
    path('', sql_executor, name='sql_form'),
]