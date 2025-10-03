from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("homepage", views.homepage, name="homepage"),
    path("homepage2", views.homepage2, name="homepage2"),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path("add_book/", views.add_book, name="add_book"),
    path("my_books/", views.book_list, name="book_list"),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path("reset/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    path('change_password/', views.change_password , name='change_password'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

]