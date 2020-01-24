from django.urls import path
import IPAM.views as ipam_views

urlpatterns = [
    path('add_subnets/', ipam_views.AddSubnetsView.as_view(), name='add-subnets'),
    path('add_subnets/summary/', ipam_views.add_subnets_summary, name='add-subnets-summary'),
]