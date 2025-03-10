from django.urls import path
from .views import upload_file, dataset_overview, basic_statistics, numerical_analysis, categorical_analysis, correlation_analysis, data_integrity

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('overview/', dataset_overview, name='dataset_overview'),
    path('basic-stats/', basic_statistics, name='basic_statistics'),
    path('numerical-analysis/', numerical_analysis, name='numerical_analysis'),
    path('categorical-analysis/', categorical_analysis, name='categorical_analysis'),
    path('correlation-analysis/', correlation_analysis, name='correlation_analysis'),
    path('data-integrity/', data_integrity, name='data_integrity'),
]
