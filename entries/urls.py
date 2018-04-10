from django.conf.urls import url

from .views import index, add_data, display_image, electricityBillView, avgProductionRequirementView, productionView, cryptoPriceView, cwrView, distributionView

urlpatterns = [
    url(r'^$', index),
    url(r'^add_data/$', add_data, name='add_data'),
    url(r'^show_graph/$', display_image, name='display_image'),
    url(r'^add_electricity_bill', electricityBillView, name='electricity_bill_view'),
    url(r'^add_avg_production_requirement', avgProductionRequirementView, name='avg_production_requirement_view'),
    url(r'^add_production', productionView, name='production_view'),
    url(r'cryptoprice', cryptoPriceView, name='crypto_price_view'),
    url(r'^add_cwr_value', cwrView, name='cwr_view' ),
    url(r'^add_distribution', distributionView, name='distribution_view' )
]
