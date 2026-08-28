from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum

from .models import User, Service, Order, Booking, Payment

@staff_member_required
def statistics_view(request):
    users = User.objects.all()

    context = {
        "users": users,
        'total_clients': User.objects.filter(role='client').count(),
        'total_employees': User.objects.filter(role='employee').count(),
        'total_services': Service.objects.count(),
        'total_orders': Order.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_revenue': Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    }

    return render(request, 'crm_admin/statistics.html', context)


