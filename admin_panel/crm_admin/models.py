from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    duration = models.IntegerField()

    class Meta:
        db_table = 'services'
        managed = False

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, db_index=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_column='client_id')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_column='service_id')
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'orders'
        managed = False

    def __str__(self):
        return self.status

class Booking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, db_column='employee_id')
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'bookings'
        managed = False

    def __str__(self):
        return str(self.scheduled_at)

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='booking_id')
    amount = models.FloatField()
    paid_at = models.DateTimeField(auto_now_add=False)
    method = models.CharField(max_length=50)

    class Meta:
        db_table = 'payments'
        managed = False

    def __str__(self):
        return self.method

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='employee')

class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
