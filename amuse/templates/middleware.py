from django.core.cache import cache
from .models import FailedLoginAttempt
from django.utils import timezone

MAX_FAILED_ATTEMPTS = 5  # Maximum failed attempts before lockout
LOCKOUT_TIME = 60  # Lockout time in seconds

class BruteForceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            failed_attempt, created = FailedLoginAttempt.objects.get_or_create(username=username)
            failed_attempt.attempts += 1
            failed_attempt.last_attempt = timezone.now()
            failed_attempt.save()

            if failed_attempt.attempts >= MAX_FAILED_ATTEMPTS:
                remaining_time = (failed_attempt.last_attempt - timezone.now()).total_seconds()
                if remaining_time > 0:
                    return render(request, 'login.html', {'error': f'This user account is locked for {remaining_time} seconds.'})
                else:
                    failed_attempt.delete()

        response = self.get_response(request)
        return response
