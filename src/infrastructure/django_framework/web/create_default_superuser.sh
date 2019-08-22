from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('Admin', 'admin@myproject.com', 'admin');