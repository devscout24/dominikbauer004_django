from django.urls import path
from .views import MyAssignedContactsView, SelectContactPersonView

urlpatterns = [
     path('assigned-contacts/', MyAssignedContactsView.as_view(), name='assigned-contacts'),
    path('select-contact/', SelectContactPersonView.as_view(), name='select-contact'),
]
