from django.urls import path
from .views.address_view import AddressView
from .views.import_network_coverage_view import ImportNetworkCoverageView

urlpatterns = [
    path('address/', AddressView.as_view(), name='address-coverage'),
    path('import/', ImportNetworkCoverageView.as_view(), name='import-network-coverage'),

 ]
