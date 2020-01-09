from django.db import models

# Create your models here.


class Tenant(models.Model):
    """
    Room's owner/tenant
    """
    first_name = models.CharField(
        'First name',
        max_length=250,
    )
    last_name = models.CharField(
        'Last name',
        max_length=250,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        db_index=True,
    )
    phone = models.CharField(
        'Phone num',
        max_length=20,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        'Photo',
        upload_to='tenant',
        help_text='Photo of the tenant',
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Room(models.Model):
    number = models.IntegerField()
    max_tenants = models.IntegerField()
    current_tenant = models.OneToOneField(
        Tenant,
        on_delete=models.SET_DEFAULT,
        default='free'
    )

    def __str__(self):
        return f'Room {self.number}'

    class Meta:
        ordering = ['number']


class Journal(models.Model):
    created = models.DateTimeField()
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_DEFAULT,
        default='not existing room'
    ),
    guests_count = models.IntegerField(
        blank=True,
        null=True
    )
    is_kept = models.BooleanField()

    def __str__(self):
        return f'Entry: {self.created} room {self.room} became ' \
               f'{"vacated" if self.is_kept else "occupied"}'

    class Meta:
        ordering = ['created']
