from django.urls import path
from .views import CreateCommentView, ListCommentView, CreateQuoteView, ListQuoteView

urlpatterns = [
    path('comment/create/<int:class_id>/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/<int:class_id>/', ListCommentView.as_view(), name='list-comments'),

    path('quote/create/<int:class_id>/', CreateQuoteView.as_view(), name='create-quote'),
    path('quotes/<int:class_id>/', ListQuoteView.as_view(), name='list-quotes'),
]
