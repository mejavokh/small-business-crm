from django.contrib import admin
from .models import User, Service, Order, Booking, Payment, Employee

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Employee)
