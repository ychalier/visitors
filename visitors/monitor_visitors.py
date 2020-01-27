"""Material for the 'monitor_visitors' Django view decorator"""
from . import models


def bot_blacklist(user_agent):
    blacklist = [
        "googlebot",
        "yandexbot",
        "bingbot",
        "mj12bot",
        "ahrefsbot",
        "mail.ru_bot",
    ]
    for bot_agent in blacklist:
        if bot_agent in user_agent.lower():
            return True
    return False


def get_or_create_visitor(ip_address, user_agent):
    if models.Visitor.objects.filter(ip_address=ip_address, user_agent=user_agent).exists():
        return models.Visitor.objects.get(ip_address=ip_address, user_agent=user_agent)
    return models.Visitor.objects.create(ip_address=ip_address, user_agent=user_agent)


def inspect_request(request):
    if request.user.is_authenticated:
        return
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if bot_blacklist(user_agent):
        return
    ip_address = request.META.get("REMOTE_ADDR", "")
    visitor = get_or_create_visitor(ip_address, user_agent)
    models.Visit.objects.create(
        visitor=visitor,
        path=request.path,
        host=request.META.get("HTTP_HOST", ""),
    )


def monitor_visitors(view):
    def wrapper(request, *args, **kwargs):
        inspect_request(request)
        return view(request, *args, **kwargs)
    return wrapper
