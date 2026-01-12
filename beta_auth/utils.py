from django.contrib.sessions.models import Session
from .models import UserSession

def invalidate_all_user_sessions_except_current(user, current_session_key):
    user_sessions = UserSession.objects.filter(user=user)

    other_sessions = user_sessions.exclude(session_key=current_session_key)
    
    other_session_keys = other_sessions.values_list('session_key', flat=True)
    
    Session.objects.filter(session_key__in=other_session_keys).delete()
    other_sessions.delete()
