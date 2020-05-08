from django.urls import path
from notesapp import views

app_name = 'notes_app'

urlpatterns = [ path('create/', views.CreateNoteView.as_view(), name = 'createnote' ),
                path('all_notes/<int:option>', views.AllNotesView.as_view(), name = 'allnotes'),
                path('show_note/<pk>', views.ShowNoteView.as_view(), name = 'shownote'),
                path('edit_note/<pk>', views.EditNoteView.as_view(), name = 'editnote'),
                path('edit_star/<pk>', views.EditStarView.as_view(), name = 'editstar'),
                path('tags_view/<tag>', views.NotesTagView.as_view(), name = 'tagsview'),
                path('remove/<pk>', views.DeleteNote.as_view(), name = 'removenote'),
                path('search_note/<phrase>', views.SearchNoteView.as_view(), name = 'searchnote')

]