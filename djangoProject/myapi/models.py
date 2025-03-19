from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Film(models.Model):
    ID = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name="film name")
    director = models.CharField(max_length=20, verbose_name="film director")
    release_date = models.DateField(verbose_name="released date")
    now_showing = models.BooleanField(default=True)


class Actor(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class ScreeningRoom(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="screening room name")
    rows = models.IntegerField()
    columns = models.IntegerField()


class TimeSlot(models.Model):
    ID = models.IntegerField(primary_key=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    ScreeningRoom = models.ForeignKey(ScreeningRoom, on_delete=models.CASCADE)
    begin_time = models.DateTimeField(verbose_name="screening time")
    ticketPrice = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)


class SeatStatus(models.Model):
    ID = models.IntegerField(primary_key=True, auto_created=True)
    seat_number = models.IntegerField()
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_occupied = models.BooleanField(default=False)

    class Meta:
        unique_together = (('seat_number', 'timeslot'),)
        indexes = [
            models.Index(fields=['timeslot', 'seat_number'])
        ]


class TicketService(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user'])
        ]


class rating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    film_rating = models.DecimalField(max_digits=3, decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('film', 'user'),)


@receiver(signal=pre_delete, sender=TicketService)
def change_seat_status_to_unoccupied(sender, instance, **kwargs):
    ts_id = instance.timeslot_id
    seat_number = instance.seat_number
    try:
        seat = SeatStatus.objects.get(timeslot_id=ts_id, seat_number=seat_number)
        seat.is_occupied = False
        seat.save()
    except SeatStatus.DoesNotExist:
        print("fatal error, seat instance not found")
        raise
