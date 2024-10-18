# Generated by Django 5.1 on 2024-09-19 09:19

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('banner_image', models.ImageField(upload_to='banners/', verbose_name='Изображение')),
                ('is_asset', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название категории')),
                ('description', models.TextField(verbose_name='Описание категории')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DateTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала тура')),
                ('end_date', models.DateField(verbose_name='Дата окончания тура')),
                ('season', models.CharField(choices=[('spring', 'Весна'), ('summer', 'Лето'), ('autumn', 'Осень'), ('winter', 'Зима')], max_length=100, verbose_name='Сезон')),
            ],
        ),
        migrations.CreateModel(
            name='RegionTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название региона')),
                ('description', models.TextField(verbose_name='Описание региона')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tours_images/', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(max_length=500, verbose_name='Описание тура')),
                ('route_tour', models.CharField(max_length=200, verbose_name='Маршрут тура')),
                ('duration', models.IntegerField(verbose_name='Продолжительность (дни)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена со скидкой')),
                ('discount_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата начала скидки')),
                ('discount_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания скидки')),
                ('participants_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за участника')),
                ('max_participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Максимальное количество участников')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админская')),
                ('category', models.ManyToManyField(related_name='tours', to='tour.category')),
                ('date_tour', models.ManyToManyField(related_name='tours', to='tour.datetour')),
                ('region', models.ManyToManyField(related_name='tours', to='tour.regiontour')),
                ('images', models.ManyToManyField(blank=True, related_name='tours', to='tour.tourimage')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user_name', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='tour.feedback')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.tour')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество участников')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Итоговая цена')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'В ожидании'), (2, 'Подтверждено'), (3, 'Отклонено')], verbose_name='Статус бронирования')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tour.datetour')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tour.tour')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tour.tour')),
            ],
            options={
                'indexes': [models.Index(fields=['tour', 'user'], name='tour_rating_tour_id_f3c1ad_idx')],
            },
        ),
        migrations.CreateModel(
            name='FavoriteList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.tour')),
            ],
            options={
                'unique_together': {('tour', 'user')},
            },
        ),
    ]
