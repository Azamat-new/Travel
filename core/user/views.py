from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MyUser
from .serializers import UserRegisterSerializer, UserProfileListSerializer, MyUserSerializer, BookingSerializer



class MyUserViewSet(APIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

class UserRegisterView(APIView):
    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Ошибка при регистрации.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_object = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfileListSerializer(user_object)
        return Response({
            'message': 'Информация о пользователе успешно получена.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserProfileListSerializer)
    def patch(self, request):
        user_object = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfileListSerializer(user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Профиль успешно обновлен.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Ошибка при обновлении профиля.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserBookingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        bookings = user.bookings.all() 
        serializer = BookingSerializer(bookings, many=True) 
        return Response({
            'message': 'История заказов успешно получена.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Отмена бронирования")
    def delete(self, request, booking_id):
        user = get_object_or_404(MyUser, id=request.user.id)
        booking = get_object_or_404(Booking, id=booking_id, users=user)
        booking.delete()  

        return Response({
            'message': 'Бронирование успешно отменено.'
        }, status=status.HTTP_204_NO_CONTENT)
    

class UserTourCreationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.status < 2: 
            return Response({'error': 'У вас нет прав для создания тура.'}, status=403)
        
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user) 
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, tour_id):
        user = request.user
        tour = get_object_or_404(Tour, id=tour_id, author=user)
        serializer = TourSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class UserWithdrawFundsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.status < 2:  
            return Response({'error': 'У вас нет прав для вывода средств.'}, status=403)
        
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Не указана сумма вывода.'}, status=400)
        
        if amount > user.balance:
            return Response({'error': 'Недостаточно средств.'}, status=400)

        user.balance -= amount
        user.save()

        return Response({'message': 'Запрос на вывод средств успешно отправлен.'}, status=200)