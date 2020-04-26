from django.contrib.auth import get_user_model

if __name__ == "__main__":
    import django

    django.setup()

    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
