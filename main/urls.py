from django.urls import path
from .views import new_application, edit_application, readonly_application, \
    check_my_application, update_application_service, update_application_shop, \
    readonly_application_service, readonly_application_shop, start, comments, question_delete, statuses, print_confirmation_for_customer

from django.urls import include, path


urlpatterns = [
    path('', start, name='start'),

    # path('search_form/', search_form, name='search_form'),

    #path('applications/', applications_list, name='applications'),
    path('applications/new/', new_application, name='new_application'),
    path('applications/edit/<int:id>/', edit_application, name='edit_application'),
    path('applications/readonly/<int:id>/', readonly_application, name='readonly_application'),

    #path('shop/applications/new/', new_application_shop, name='new_application_shop'),
    #path('shop/applications/', applications_list_shop, name='applications_shop'),
    path('shop/applications/update/<int:id>/', update_application_shop, name='update_application_shop'),
    path('shop/applications/readonly/<int:id>/', readonly_application_shop, name='readonly_application_shop'),

    #path('service/applications/', applications_list_service, name='applications_service'),
    path('service/applications/update/<int:id>/', update_application_service, name='update_application_service'),
    path('service/applications/readonly/<int:id>/', readonly_application_service, name='readonly_application_service'),

    path('check_application/', check_my_application, name='check_my_application'),
    path('applications/comments/<int:id>/', comments, name='comments'),
    path('applications/statuses/<int:id>/', statuses, name='statuses'),
    path('applications/delete/<int:id>/', question_delete, name='question_delete'),
    path('print', print_confirmation_for_customer, name='print_confirmation_for_customer'),


]

