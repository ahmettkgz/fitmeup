from django.urls import path

from .views import PostListView, BlogDetailsView, BlogCreateView, BlogUpdateView, BlogDeleteView

# url patterns are created in here

# the as_view() method is called to convert the MyView class into a callable view.
urlpatterns = [

    path("", PostListView.as_view(), name="blogs"),
    path("new/", BlogCreateView.as_view(), name="blog_create"),
    path("<int:pk>/update/", BlogUpdateView.as_view(), name="blog_update"),  # primary key is necessary for the specific blog
    path("<int:id>", BlogDetailsView.as_view(), name="blog_details"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="blog_delete")
]
