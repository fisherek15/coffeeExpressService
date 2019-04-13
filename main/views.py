from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order, Comment, Status
from .forms import ApplicationForm, CustomerForm, DeviceForm, ServiceApplicationForm, ShopApplicationForm, CommentForm, StatusForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
import logging


def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


@login_required
def start(request):
    if request.user.groups.filter(name='admin').exists():
        applications = Order.objects.all()
        return render(request, 'applications_list.html', {'applications': applications})
    elif request.user.groups.filter(name='service').exists():
        applications = Order.objects.all()
        return render(request, 'applications_list_service.html', {'applications': applications})
    elif request.user.groups.filter(name='shop').exists():
        applications = Order.objects.all()
        return render(request, 'applications_list_shop.html', {'applications': applications})
    else:
        return HttpResponse('Nie masz uprawnień do wyświetlania tej strony. Skontaktuj się z administratorem.')


@login_required
@group_required('admin')
def applications_list(request):
    applications = []
    all_applications = Order.objects.all()
    for application in all_applications:
        status = Status.objects.filter(order=application).order_by('-date_of_change').first()
        order = {
            'id': application.id,
            'order_id': application.order_id,
            'acceptance_date': application.acceptance_date,
            'status': status.content
        }
        applications.append(order)
    applications.reverse()
    return render(request, 'applications_list.html', {'applications': applications})


@login_required
@group_required('shop')
def applications_list_shop(request):
    applications = Order.objects.all()
    return render(request, 'applications_list_shop.html', {'applications': applications})


@login_required
@group_required('service')
def applications_list_service(request):
    applications = Order.objects.all()
    return render(request, 'applications_list_service.html', {'applications': applications})


@login_required
@group_required('admin')
def new_application(request):
    device_form = DeviceForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)
    application_form = ApplicationForm(request.POST or None)
    if customer_form.is_valid() and application_form.is_valid() and device_form.is_valid():
        today = datetime.today()
        current_month = today.month
        current_year = today.year
        try:
            last_order = Order.objects.latest('id')
            last_id = last_order.pk + 1
        except ObjectDoesNotExist:
            last_id = 0
        order = application_form.save(commit=False)
        order.customer = customer_form.save()
        order.device = device_form.save()
        order.order_id = str(last_id) + "/" + str(current_month) + "/" + str(current_year)
        order.save()
        status = Status()
        status.order = order
        status.author = request.user
        status.content = "Sklep / Przyjęte"
        status.save()
        return redirect(applications_list)
    return render(request, 'new_application.html', {'deviceForm': device_form, 'customerForm': customer_form,
                                                    'applicationForm': application_form})


@login_required
@group_required('shop')
def new_application_shop(request):
    device_form = DeviceForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)
    application_form = ApplicationForm(request.POST or None)
    if customer_form.is_valid() and application_form.is_valid() and device_form.is_valid():
        order = application_form.save(commit=False)
        order.status_all = order.status_shop;
        order.customer = customer_form.save()
        order.device = device_form.save()
        order.save()
        return redirect(applications_list_shop)
    return render(request, 'new_application_shop.html', {'deviceForm': device_form, 'customerForm': customer_form,
                                                    'applicationForm': application_form})


@login_required
@group_required('admin')
def edit_application(request, id):
    application = get_object_or_404(Order, pk=id)
    application_form = ApplicationForm(request.POST or None, instance=application)
    device_form = DeviceForm(request.POST or None, instance=application.device)
    customer_form = CustomerForm(request.POST or None, instance=application.customer)
    if customer_form.is_valid() and application_form.is_valid() and device_form.is_valid():
        order = application_form.save(commit=False)
        order.customer = customer_form.save()
        order.device = device_form.save()
        order.save()
        return redirect(applications_list)
    return render(request, 'full_application_edit.html',
                  {'applicationOrderId': application.order_id, 'deviceForm': device_form, 'customerForm': customer_form,
                   'applicationForm': application_form})


@login_required
@group_required('service')
def update_application_service(request, id):
    application = get_object_or_404(Order, pk=id)
    application_form = ServiceApplicationForm(request.POST or None, instance=application)
    if application_form.is_valid():
        order = application_form.save(commit=False)
        order.save()
        return redirect(applications_list_service)
    return render(request, 'update_application_service.html',
                  {'applicationOrderId': application.order_id,
                   'descriptionForService': application.description_for_service,
                   'applicationForm': application_form})


@login_required
@group_required('shop')
def update_application_shop(request, id):
    application = get_object_or_404(Order, pk=id)
    application_form = ShopApplicationForm(request.POST or None, instance=application)
    if application_form.is_valid():
        order = application_form.save(commit=False)
        order.save()
        return redirect(applications_list_shop)
    return render(request, 'update_application_shop.html',
                  {'applicationOrderId': application.order_id,
                   'descriptionForService': application.description_for_service,
                   'descriptionFromService': application.description_from_service,
                   'serviceRepairCost': application.service_repair_cost,
                   'applicationForm': application_form})


@login_required
@group_required('shop')
def readonly_application_shop(request, id):
    application = get_object_or_404(Order, pk=id)
    return render(request, 'readonly_application_shop.html',
                  {'application': application, 'device': application.device, 'customer': application.customer})


@login_required
@group_required('admin')
def readonly_application(request, id):
    application = get_object_or_404(Order, pk=id)
    return render(request, 'readonly_application.html',
                  {'application': application, 'device': application.device, 'customer': application.customer})


@login_required
@group_required('service')
def readonly_application_service(request, id):
    application = get_object_or_404(Order, pk=id)
    return render(request, 'readonly_application_service.html',
                  {'application': application, 'device': application.device})


def check_my_application(request):
    return render(request, 'check_my_application.html')


def search_form(request):
    orderId = None
    str_date = None
    # status = None
    if request.POST.get('search'):
        result = request.POST.get('search')
        order = get_object_or_404(Order, order_id=result)
        orderId = order.order_id
        date_time = order.acceptance_date
        str_date = date_time.strftime("%d-%m-%Y")
        # status = order.status
    return render(request, 'search_form.html', {'orderId': orderId, 'acceptanceDate': str_date}) # 'status': status})


@login_required
@group_required('admin', 'shop', 'service')
def comments(request, id):
    application = get_object_or_404(Order, pk=id)
    comments = Comment.objects.filter(order=application).order_by('published_date')
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.order = application
        comment.save()
    return render(request, 'comments.html', {'orderId': application.order_id, 'comments': comments, 'commentForm': comment_form})


@login_required
@group_required('admin', 'shop', 'service')
def statuses(request, id):
    application = get_object_or_404(Order, pk=id)
    statuses = Status.objects.filter(order=application).order_by('date_of_change')
    if request.POST.get('selected_status'):
        status = Status()
        status.content = request.POST.get('selected_status')
        status.author = request.user
        status.order = application
        status.save()
    return render(request, 'statuses.html', {'orderId': application.order_id, 'statuses': statuses})


@login_required()
@group_required('admin')
def question_delete(request, id):
    application = get_object_or_404(Order, pk=id)
    application.delete()
    return redirect(applications_list)

