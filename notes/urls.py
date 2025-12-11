from django.urls import path

from .views import create, delete, get_all, get_by_id, get_mine, update

urlpatterns = [
    path('', get_all),
    path('me', get_mine),
    path('<int:id>', get_by_id),
    path('create', create),
    path('update/<int:id>', update),
    path('delete/<int:id>', delete),
]
