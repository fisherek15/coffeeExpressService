from django.forms import ModelForm, DateField, DateInput
from .models import Order, Customer, Device, Comment




class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'email']


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['producer', 'type', 'model', 'id_number']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ApplicationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_id', 'order_type', 'acceptance_date', 'description_for_service', 'description_from_service',
                  'description_for_customer', 'max_repair_cost', 'technical_condition',
                  'service_repair_cost', 'sms_sent_date', 'repair_cost', 'return_date', 'status']
        acceptance_date = DateField(
        )


class ServiceApplicationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['description_from_service', 'service_repair_cost', 'status']


class ShopApplicationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['description_for_customer', 'repair_cost', 'return_date', 'status', 'sms_sent_date']


