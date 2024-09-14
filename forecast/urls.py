# forecast/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('import-csv',import_csv_view,name='import-csv'),
    path('reservoirs/<int:year>/<int:month>', get_reservoirs_by_year_and_month, name='get_reservoirs_by_year_and_month'),
    path('reservoirs/<str:name>/', get_reservoirs_by_name, name='get_reservoirs_by_name'),
    path('reservoirs/',get_reservoirs,name='get_reservoirs'),
    path('reservoirs/get-month',get_months,name='get_months'),
    path('reservoirs/get-year',get_years,name='get_years'),
    path('reservoirs/get-base', get_basins, name='get_basins'),
]

