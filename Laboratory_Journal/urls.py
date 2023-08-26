"""Laboratory_Journal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Lab_journal_app.views import StartPageView, MainPageView, AddMethodView, MethodListView, DeleteMethodView, DetailMethodView, ModifyMethodView, AddUserView, LoginUserView, LogoutUserView, AddSampleView, AddResultsView, ResultsListView, ResultsSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPageView.as_view(), name='start-page'),
    path('main/', MainPageView.as_view(), name='main-page'),
    path('method/new/', AddMethodView.as_view(), name='add-method'),
    path('method/list/', MethodListView.as_view(), name='method-list'),
    path('method/delete/<int:method_id>/', DeleteMethodView.as_view(), name='delete-method'),
    path('method/detail/<int:method_id>/', DetailMethodView.as_view(), name='method-detail'),
    path('method/modify/<int:method_id>/', ModifyMethodView.as_view(), name='modify-method'),
    path('adduser/', AddUserView.as_view(), name='user_add'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('sample/', AddSampleView.as_view(), name='add-sample'),
    path('result/add/<int:sample_id>/', AddResultsView.as_view(), name='add-results'),
    path('results/list/', ResultsListView.as_view(), name='results-list'),
    path('results/search/', ResultsSearchView.as_view(), name='results-search')



]