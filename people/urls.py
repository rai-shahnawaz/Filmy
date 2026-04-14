from django.urls import path
from .views import (
	PersonList, PersonDetail, search_people,
	soft_delete_person, restore_person,
	export_people_json, import_people_json,
	export_people_csv, import_people_csv
)

urlpatterns = [
	path('', PersonList.as_view(), name='person-list'),
	path('<str:pk>/', PersonDetail.as_view(), name='person-detail'),
	path('search/', search_people, name='search_people'),
	path('admin/<str:uid>/soft_delete/', soft_delete_person, name='soft_delete_person'),
	path('admin/<str:uid>/restore/', restore_person, name='restore_person'),
	path('admin/export/json/', export_people_json, name='export_people_json'),
	path('admin/import/json/', import_people_json, name='import_people_json'),
	path('admin/export/csv/', export_people_csv, name='export_people_csv'),
	path('admin/import/csv/', import_people_csv, name='import_people_csv'),
]
