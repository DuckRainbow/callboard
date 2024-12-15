from django.http import Http404
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from callboard.models import Ad, Feedback
from callboard.paginators import CustomPagination
from callboard.serializers import AdSerializer, FeedbackSerializer, AdDetailSerializer
from users.permissions import IsAdmin, IsAuthor


class AdCreateAPIView(CreateAPIView):
    """Контроллер для создания объявления."""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Привязка автора объявления к текущему пользователю"""
        ad = serializer.save()
        ad.author = self.request.user
        print(ad.author)
        ad.save()


class AdListAPIView(ListAPIView):
    """Контроллер для просмотра списка всех объявлений"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = (SearchFilter,)
    search_fields = (
        "title",
        "description",
    )
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


class AdRetrieveAPIView(RetrieveAPIView):
    """Контроллер для просмотра объявления"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateAPIView(UpdateAPIView):
    """Контроллер для изменения объявления"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )


class AdDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления объявления"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )


class UsersAdListAPIView(ListAPIView):
    """Контроллер для просмотра списка объявлений пользователя"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthor,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        """Список объявлений автора"""
        user = self.request.user
        return super().get_queryset().filter(author=user)


class FeedbackCreateAPIView(CreateAPIView):
    """Контроллер для создания отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Привязываем отзыв к автору и объявлению"""
        feedback = serializer.save()
        feedback.author = self.request.user
        feedback.ad = Ad.objects.get(pk=self.kwargs["pk"])
        print(feedback.ad)
        feedback.save()


class FeedbackListAPIView(ListAPIView):
    """Контроллер для просмотра всех отзывов объявления"""

    queryset = Feedback.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод для получения отзывов объявления"""
        pk = self.kwargs.get("pk")
        try:
            ad = Ad.objects.get(id=pk)
        except Ad.DoesNotExist:
            raise Http404("Указанного объявления не существует.")
        feedbacks_list = ad.ad_feedback.all()
        return feedbacks_list


class FeedbackRetrieveAPIView(RetrieveAPIView):
    """Контроллер для просмотра одного отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)


class FeedbackUpdateAPIView(UpdateAPIView):
    """Контроллер для изменения отзыва"""

    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )


class FeedbackDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )


class UsersFeedbackListAPIView(ListAPIView):
    """Контроллер для просмотра списка отзывов пользователя"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthor,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод для получения списка отзывов пользователя"""
        author = self.request.user
        return super().get_queryset().filter(author=author)
