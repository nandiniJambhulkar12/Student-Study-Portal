# from django.urls import path
# from . import views  # Import views from the same app

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('notes', views.notes, name='notes'),
#     path('delete_note/<int:pk>',views.delete_note,name='delete_note'),
#     path('notes_detail/<int:pk>',views.NotesDetailView.as_view(),name='notes_detail'),# Route for home view
    
    
    
#     path('homework', views.homework, name='homework'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<int:pk>/', views.delete_note, name='delete_note'),
    path('notes_detail/<int:pk>/', views.NotesDetailView.as_view(), name='notes_detail'),
    
    
    # for homework
    path('homework/', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),
    
    
    # for youtube:
    path('youtube/', views.youtube, name='youtube'),
    
    # for todo:
    path('todo/', views.todo, name='todo'),
    path('update_todo/<int:pk>/', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),
    
    
    # for books:
    path('books/', views.books, name='books'),
    
    
    # for dict:
    path('dictionary/', views.dictionary, name='dictionary'),
    
    # for wikipedia:
    path('WikiPedia/', views.wiki, name='wiki'),
    # for conversion :
    path('conversion/', views.conversion, name='conversion'),
    
    
    
    
    
]
