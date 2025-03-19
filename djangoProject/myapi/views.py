from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse

from django.db import connection
from django.db import transaction, IntegrityError, DatabaseError
from django.db.models import Avg

from django.core.exceptions import ValidationError

from .models import SeatStatus
from .models import TimeSlot
from .models import ScreeningRoom
from .models import Film
from .models import Actor
from .models import TicketService
from .models import rating
from .exceptions import seatOccupiedException


# Create your views here.
def login_view(request):
    return render(request, 'loginPage.html')


def seats_detail(request):
    ts_id = request.GET.get('ts_id')
    seats = SeatStatus.objects.filter(timeslot=ts_id).values_list('seat_number', 'is_occupied', 'ID')
    seats_list = list(seats)
    sr_id = TimeSlot.objects.filter(ID=ts_id).values_list('ScreeningRoom', flat=True).first()
    rows = ScreeningRoom.objects.filter(ID=sr_id).values_list('rows', flat=True).first()
    columns = ScreeningRoom.objects.filter(ID=sr_id).values_list('columns', flat=True).first()
    data = {'seats_list': seats_list, 'rows': rows, 'columns': columns}
    return JsonResponse(data, safe=False)


def timeslot_info(request):
    ts_id = request.GET.get('ts_id')
    temp = TimeSlot.objects.get(ID=ts_id)
    film_title = temp.film.title
    sr_name = temp.ScreeningRoom.name
    data = {'film_title': film_title, 'time': temp.begin_time, 'SR_name': sr_name, 'ticketPrice': temp.ticketPrice}
    return JsonResponse(data, safe=False)


def actor(request):
    film_id = request.GET.get('film_id')
    data = Actor.objects.filter(film=film_id).values_list('name', flat=True)
    data = list(data)
    return JsonResponse(data, safe=False)


def film_list(request):
    data = Film.objects.filter(now_showing=True).values_list('ID', 'title', 'director', 'release_date')
    data = list(data)
    return JsonResponse(data, safe=False)


def search_film(request):
    title = request.GET.get('title')
    data = Film.objects.filter(name__icontains=title, now_showing=True).values_list('ID', 'title',
                                                                                    'director', 'release_date')
    data = list(data)
    return JsonResponse(data, safe=False)


def film_avg_rating(request):
    film_id = request.GET.get('film_id')
    film = Film.objects.get(ID=film_id)
    data = rating.objects.filter(film=film).aggregate(avg=Avg('film_rating'))['avg']
    if data:
        data = round(data, 1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse(0.0, safe=False)


def timeslot_list(request):
    film_id = request.GET.get('film_id')
    temp = TimeSlot.objects.filter(film=film_id).select_related('ScreeningRoom')
    data = temp.values_list('ID', 'begin_time', 'ScreeningRoom__name', 'ScreeningRoom')
    data = list(data)
    return JsonResponse(data, safe=False)


def avai_seat(request):
    ts_id = request.GET.get('ts_id')
    data = SeatStatus.objects.filter(timeslot=ts_id, is_occupied=False).count()
    return JsonResponse(data, safe=False)


def total_seat(request):
    ts_id = request.GET.get('ts_id')
    sr_id = TimeSlot.objects.filter(ID=ts_id).values_list('ScreeningRoom', flat=True).first()
    temp = ScreeningRoom.objects.filter(ID=sr_id).values_list('rows', 'columns').first()
    data = {'rows': temp[0], 'columns': temp[1]}
    return JsonResponse(data, safe=False)


@api_view(['POST'])
@permission_classes([])
def register(request):
    username = request.data['username']
    password = request.data['password']
    User.objects.create_user(username=username, password=password)
    return JsonResponse({'message': "注册成功"}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(request):
    username = request.query_params.get('username')
    user = User.objects.filter(username=username).first()
    data = user.id
    return JsonResponse(data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_orders(request):
    user_id = request.query_params.get('user_id')
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
            SELECT F.title, T.begin_time, S.seat_number, T.ticketprice, S.is_paid, S.id FROM myapi_ticketservice AS S
            JOIN myapi_timeslot AS T ON S.timeslot_id = T.ID
            JOIN myapi_film AS F ON F.ID = T.film_id 
            WHERE S.user_id = %s''',
                [user_id]
            )
            result = cursor.fetchall()
        data = list(result)
        return JsonResponse(data, safe=False)
    except DatabaseError as e:
        return JsonResponse({'error': f"query error: {e}"}, status=500)


# to-do
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_seats(request):
    seat_status_id = request.data['ss_id_list']
    ts_id = request.data['ts_id']
    user_id = request.data['user_id']
    is_paid = request.data['is_paid']
    timeslot = TimeSlot.objects.get(ID=ts_id)
    user = User.objects.get(id=user_id)

    try:
        with transaction.atomic():
            for ss_id in seat_status_id:
                item = SeatStatus.objects.get(ID=ss_id)
                if item.is_occupied:
                    raise seatOccupiedException("seat already occupied")
                else:
                    item.is_occupied = True
                    item.save()
                    ticket_service = TicketService(
                        timeslot=timeslot,
                        seat_number=item.seat_number,
                        user=user,
                        is_paid=is_paid
                    )
                    ticket_service.save()
        return JsonResponse({"message": "订票成功"}, status=200)
    except seatOccupiedException:
        return JsonResponse({'error': "您要预定的座位似乎被别人抢先了呢"}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': f"something went wrong, {e}"}, status=500)
    finally:
        transaction.set_autocommit(True)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_rating(request):
    user_id = request.data['user_id']
    film_id = request.data['film_id']
    score = request.data['score']
    try:
        user = User.objects.get(id=user_id)
        film = Film.objects.get(ID=film_id)
        new_rating, created = rating.objects.get_or_create(user=user, film=film, defaults={'film_rating': score})
        if not created:
            return JsonResponse({'error': "您已经评分过啦"}, status=400)
        return JsonResponse({'message': "评分成功"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': "用户信息无效"}, status=404)
    except Film.DoesNotExist:
        return JsonResponse({'error': "电影不存在"}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_order_in_timeslot(request):
    user_id = request.query_params.get('user_id')
    ts_id = request.query_params.get('ts_id')
    data = TicketService.objects.filter(user_id=user_id, timeslot_id=ts_id).values_list('seat_number', flat=True)
    data = list(data)
    return JsonResponse(data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    ticket_id = request.query_params.get('ticket_id')
    try:
        ticket = TicketService.objects.get(id=ticket_id)
        ticket.delete()
        return JsonResponse({"message": "退票成功"}, status=200)
    except TicketService.DoesNotExist:
        return JsonResponse({"error": "fatal error, database has data missing"}, status=404)
    except SeatStatus.DoesNotExist:
        return JsonResponse({"error": "fatal error, seat instance missing"}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_booked(request):
    try:
        ticket_id = request.data['ticket_id']
        ticket = TicketService.objects.get(id=ticket_id)
        if ticket.is_paid:
            return JsonResponse({"error": "fatal error"}, status=400)
        else:
            ticket.is_paid = True
            ticket.save()
            return JsonResponse({"message": "支付成功"}, status=200)
    except TicketService.DoesNotExist:
        return JsonResponse({"error": "Order does not exist"}, status=404)
