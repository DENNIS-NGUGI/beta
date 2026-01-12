from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import UserSession
from .utils import invalidate_all_user_sessions_except_current

class SessionManagementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            user = request.user

            request.current_session_key = current_session_key

            if current_session_key:
                user_session, created = UserSession.objects.get_or_create(
                    user=user,
                    session_key=current_session_key,
                )

                invalidate_all_user_sessions_except_current(user, current_session_key)

    def process_response(self, request, response):
        if request.user.is_authenticated:
            current_session_key = getattr(request, 'current_session_key', None)
            
            if current_session_key:
                UserSession.objects.filter(user=request.user, session_key=current_session_key).update(created_at=timezone.now())
                
        return response
