from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('tasks/export/csv/', views.ExportApiAsCSV.as_view(), name='export-tasks'),
    path('tasks/export/pdf/', views.TaskExportPDF.as_view(), name='export-tasks'),
    path('tasks/export/excel/', views.TaskExportExcel.as_view(), name='export-tasks'),
    path('auth/token/',obtain_auth_token, name='obtain-token'),
    path('auth/tokenJWT/',TokenObtainPairView.as_view(),name='obtain-jwtToken'),
    path('auth/tokenJWT/refresh/',TokenRefreshView.as_view(),name='refresh-token'),
    path('taskFiltered/',views.TaskListFilteredAPIView.as_view(),name='task-list-filtered'),
    path('<int:pk>',views.TaskListRetrieveUpdateDeleteAPIView.as_view(),name='task-detail'),
    path('',views.TaskGetAllAndPost.as_view(),name='task-get-all'),

]