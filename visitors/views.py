from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .monitor_visitors import monitor_visitors
from . import models
import datetime


@monitor_visitors
def dummy(request):
    return render(request, "visitors/home.html", {})


@login_required
def monitor(request):
    visits = models.Visit.objects.all().order_by("timestamp")
    total_visits = models.Visit.objects.all().count()
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    visits_today = models.Visit.objects.filter(timestamp__gt=yesterday).count()
    visitors = models.Visitor.objects.all()
    return render(request, "visitors/monitor.html", {
        "visits": visits,
        "visitors": visitors,
        "stats": {
            "total": total_visits,
            "today": visits_today
        }
    })
