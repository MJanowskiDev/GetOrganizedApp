"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from todoapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.SiteLoginView.as_view(), name = 'login'),
    path('logout/', views.SiteLogoutView.as_view(), name = 'logout'),
    path('signup/', views.SignUpView.as_view(), name = 'signupuser' ),
    path('current/<username>/<int:done>', views.TodosView.as_view(), name = 'currenttodos'),
    path('tag/<username>/<tag>', views.TagView.as_view(), name = 'tagsview'),
    path('finish/<pk>', views.CompleteTodoView.as_view(), name = 'makecomplete'),
    path('revert/<pk>', views.RevertComplete.as_view(), name = 'revertcomplete'),
    path('remove/<user>/<pk>', views.DeleteTodoView.as_view(), name = 'remove'),
    path('create/', views.CreateTodoView.as_view(), name = 'createtodo' ),
    path('edit/<pk>', views.EditTodoView.as_view(), name = 'edittodo' ),
    path('show_task/<pk>', views.ShowTaskView.as_view(), name = 'showtask'),
    path('', views.HomeView.as_view(), name = 'home')
]
