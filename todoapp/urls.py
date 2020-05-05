from django.urls import path
from todoapp import views

app_name = 'todo_app'

urlpatterns = [
    path('current/<username>/<int:done>/<int:shared>', views.TodosView.as_view(), name = 'currenttodos'),
    path('tag/<username>/<tag>', views.TagView.as_view(), name = 'tagsview'),
    path('finish/<pk>', views.CompleteTodoView.as_view(), name = 'makecomplete'),
    path('revert/<pk>', views.RevertComplete.as_view(), name = 'revertcomplete'),
    path('remove/<user>/<pk>', views.DeleteTodoView.as_view(), name = 'remove'),
    path('create/', views.CreateTodoView.as_view(), name = 'createtodo' ),
    path('edit/<pk>', views.EditTodoView.as_view(), name = 'edittodo' ),
    path('show_task/<pk>', views.ShowTaskView.as_view(), name = 'showtask'),
    path('comment/<pk>',views.ToDoCommentView.as_view(), name='add_comment'),
]