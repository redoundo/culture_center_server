from django.urls import path
from . import views


urlpatterns = [
    path('lecture', views.find_lectures_by_search_options),
    path('lecture/detail', views.find_lecture_by_lecture_id),
    path('lecture/liked', views.set_liked_this_lecture_by_lecture_id),
    path('lecture/detail/liked', views.set_liked_this_lecture_by_lecture_id),
    path('lecture/detail/applied', views.set_applied_this_lecture_by_lecture_id),
    path('lecture/applied', views.set_applied_this_lecture_by_lecture_id),
    path('myPage/user', views.find_user_by_user_id),
    path('myPage/<str:applied_liked>/delete', views.my_page_delete_liked_or_applied_by_lecture_id),
    path('myPage/edit', views.find_user_info_for_edit_info),
    path('myPage/edit/update', views.update_user_info),
    path('myPage/withdraw', views.let_withdraw_user_by_user_id),
    path('<str:sns>/login', views.sns_access_token),
    path('naver/user_info', views.naver_get_user_info),
    path('signin/<str:sns>/publish_jwt', views.sign_in_publish_jwt),
    path('login/<str:sns>/publish_jwt', views.login_publish_jwt),
    path('auth/isValid', views.is_logged_in),
    path('signin/check_nickname_is_unique', views.nickname_uniqueness),
    path('register_fcm_receiver', views.registering_fcm_receiver),
    path('new_data_json', views.download_new_data)
]
