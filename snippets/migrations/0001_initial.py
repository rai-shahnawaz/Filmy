# Generated by Django 4.1.1 on 2022-09-12 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('released_on', models.DateField()),
                ('plot', models.TextField(blank=True)),
                ('animated', models.BooleanField(default=False)),
                ('rating', models.IntegerField(null=True)),
                ('available', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('available', models.BooleanField()),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('film', models.ManyToManyField(to='snippets.film')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('aired_on', models.DateField()),
                ('unaired_on', models.DateField(blank=True, null=True)),
                ('plot', models.TextField(blank=True)),
                ('animated', models.BooleanField(default=False)),
                ('rating', models.IntegerField(null=True)),
                ('available', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=256)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.film')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Watchedlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.film')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SubGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('available', models.BooleanField()),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('film', models.ManyToManyField(to='snippets.film')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.genre')),
                ('series', models.ManyToManyField(to='snippets.series')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('aired_on', models.DateField()),
                ('unaired_on', models.DateField(blank=True, null=True)),
                ('plot', models.TextField(blank=True)),
                ('animated', models.BooleanField(default=False)),
                ('rating', models.IntegerField(null=True)),
                ('available', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
            ],
        ),
        migrations.AddField(
            model_name='genre',
            name='series',
            field=models.ManyToManyField(to='snippets.series'),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.film')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('aired_on', models.DateField()),
                ('unaired_on', models.DateField(blank=True, null=True)),
                ('plot', models.TextField(blank=True)),
                ('animated', models.BooleanField(default=False)),
                ('rating', models.IntegerField(null=True)),
                ('available', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.season')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('dod', models.DateField(blank=True, default=None, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('film', models.ManyToManyField(to='snippets.film')),
                ('series', models.ManyToManyField(to='snippets.series')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.film')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('dod', models.DateField(blank=True, default=None, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.badge')),
                ('film', models.ManyToManyField(to='snippets.film')),
                ('series', models.ManyToManyField(to='snippets.series')),
            ],
        ),
    ]