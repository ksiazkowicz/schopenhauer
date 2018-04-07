from django.contrib.auth.signals import user_logged_out


def user_logged_out_handler(sender, request, user, **kwargs):
    if user.guest:
        user.delete()


user_logged_out.connect(user_logged_out_handler)
