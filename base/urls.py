from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name="home"),
    path('task/<str:pk>/', views.task, name="task"),
    
    
    #CRUD
    path('create-task', views.createTask, name="create-task"),
    path('update-task/<str:pk>/', views.updateTask, name="update-task"),
    path('delete-task/<str:pk>/', views.deleteTask, name="delete-task"),
    
    path('create-tag', views.createTag, name="create-tag"),
    path('update-tag/<str:pk>/', views.updateTag, name="update-tag"),
    

    path('create-list', views.createList, name="create-list"),
    path('update-list/<str:pk>/', views.updateList, name="update-list"),
    
    
    path('create-priority', views.createPriority, name="create-priority"),

    path('create-newpriority', views.createnewPriority, name="create-newpriority"),


    path('update-priority/<str:pk>/', views.updatePriority, name="update-priority"),

    
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    
    
]
