from django.urls import path
from .views import index, upload_file, dataset_overview, basic_statistics, numerical_analysis, categorical_analysis, correlation_analysis, data_integrity

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_file, name='upload_file'),
    path('overview/', dataset_overview, name='dataset_overview'),
    path('basic-stats/', basic_statistics, name='basic-stats'),
    path('numerical-analysis/', numerical_analysis, name='numerical-analysis'),
    path('categorical-analysis/', categorical_analysis, name='categorical-analysis'),
    path('correlation-analysis/', correlation_analysis, name='correlation-analysis'),
    path('data-integrity/', data_integrity, name='data-integrity'),
    # path('api/data-integrity/', data_integrity, name='data_integrity'),


]
