from django.urls import path, include

from cinema.views import HallCreateView, HallUpdateView, HallDetailView, MovieListView, HallListView, HallDeleteView, \
    SessionListView, SessionDetailView, SessionCreateView, SessionDeleteView, SessionUpdateView, PurchaseTicketView

app_name = 'cinema'

urlpatterns = [
    path('', MovieListView.as_view(), name='home_page'),

    path('create-hall/', HallCreateView.as_view(), name='create_hall'),
    path('update-hall/<int:hall_id>/', HallUpdateView.as_view(), name='update_hall'),
    path('delete-hall/<int:hall_id>/', HallDeleteView.as_view(), name='delete_hall'),
    path('hall-list/', HallListView.as_view(), name='hall_list'),
    path('<int:hall_id>/', HallDetailView.as_view(), name='hall'),

    path('session-list/', SessionListView.as_view(), name='session_list'),
    path('session/<int:session_id>/', SessionDetailView.as_view(), name='session'),
    path('create-session/', SessionCreateView.as_view(), name='create_session'),
    path('delete-session/<int:session_id>/', SessionDeleteView.as_view(), name='delete_session'),
    path('update-session/<int:session_id>/', SessionUpdateView.as_view(), name='update_session'),

    path('purchase/<int:session_id>/', PurchaseTicketView.as_view(), name='purchase'),

    path('api/', include('cinema.API.urls')),
]
