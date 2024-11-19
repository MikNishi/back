from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    TagListView,
    CategoryListView,
    PostSearchView,
)

urlpatterns = [
    path("", BlogListView.as_view(), name="post_list"),
    path("search/", PostSearchView.as_view(), name="post_search"),
    path("<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("new/", BlogCreateView.as_view(), name="post_new"),
    path("<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),


    path('tag/<slug:slug>', TagListView.as_view(), name='post_by_tag'),
    path('category/<slug:slug>', CategoryListView.as_view(), name='post_by_category'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='post_detail_by_slug'),
    path("id/<int:id>/", BlogDetailView.as_view(), name="post_detail_by_id"),

]
