from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("list/<str:listId>", views.listView, name="listView"),
    path("idData/<str:bidId>", views.bidId, name="bidId"),
    path("publish/", views.publish_view, name="publish"),
    path("userComment/<str:commId>", views.user_comment, name="userComment"),
    path("watchList", views.watch_list, name="watch"),
    path("delete/<str:deletId>", views.delete_item, name="delteId"),
    path("^category/<str:categoryName>/<str:idLast>$", views.display_cate, name="categoryData"),
    path("myList", views.myPost, name="myListPost"),
    path("close/<str:closeId>", views.close_case, name="close")

]
