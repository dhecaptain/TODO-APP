from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='todo'),
    path('del/<int:item_id>',views.remove,name='del'),
    path('done/<int:item_id>',views.done,name='done'),
    path('export/',views.export_tasks,name='export_tasks'),
]
