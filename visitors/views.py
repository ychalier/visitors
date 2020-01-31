import json
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .monitor_visitors import monitor_visitors
from . import models


@monitor_visitors
def dummy(request):
    """View used to create fake log entries"""
    return render(request, "visitors/home.html", {})


@login_required
def monitor(request):
    """Render main monitoring view"""
    return render(request, "visitors/monitor.html", {})


def groupby(queryset, group_key, count_key):
    """Operates a GROUP BY on a queryset"""
    return queryset.values(group_key).annotate(count=Count(count_key, distinct=True))


def date_range(start_date, end_date):
    """Iterate over days"""
    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        yield datetime.date.fromordinal(ordinal)


def init_date_labels(start_date):
    """Create a dictionnary for a timeseries"""
    labels = dict()
    for date in date_range(start_date, datetime.date.today()):
        labels[date.strftime("%Y-%m-%d")] = 0
    return labels


def get_field_per_day(field):
    """Count number of distinct field value per day"""
    entries = list(groupby(
        models.Visit.objects.all().annotate(date=TruncDate("timestamp")),
        "date",
        field
    ).order_by("date"))
    field_per_day = init_date_labels(entries[0]["date"])
    for entry in entries:
        field_per_day[entry["date"].strftime("%Y-%m-%d")] = entry["count"]
    return field_per_day


def get_field_per_path(field):
    field_per_path = dict()
    for item in groupby(models.Visit.objects.all(), "path", field):
        field_per_path[item["path"]] = item["count"]
    return field_per_path


def extract_path_group(path):
    if path == "/":
        return "/"
    if "/" in path[1:]:
        second_slash_index = path[1:].index("/")
        return path[1:(second_slash_index + 1)]
    return path[1:]


def get_visits_per_path_group():
    visits_per_path_group = dict()
    visits_per_path = get_field_per_path("id")
    for path, count in visits_per_path.items():
        group = extract_path_group(path)
        visits_per_path_group.setdefault(group, 0)
        visits_per_path_group[group] += count
    return visits_per_path_group



@login_required
def api(request):
    """API view"""
    parts = request.GET.get("part", "")
    response = dict()
    for part in parts.split(","):
        if part == "paths":
            response["visits_per_path"] = get_field_per_path("id")
            response["visitors_per_path"] = get_field_per_path("visitor")
        elif part == "traffic":
            response["traffic_visits"] = get_field_per_day("id")
            response["traffic_visitors"] = get_field_per_day("visitor")
        elif part == "total":
            response["total_visits"] = models.Visit.objects.all().count()
            response["total_visitors"] = models.Visitor.objects.all().count()
        elif part == "group":
            response["visits_per_group"] = get_visits_per_path_group()
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def dump(_):
    """Raw data dump"""
    response = HttpResponse(content_type="text/tsv")
    response["Content-Disposition"] = "attachment; filename=\"visitors.tsv\""
    response.write("\t".join([
        "timestamp",
        "ip",
        "useragent",
        "host",
        "path"
    ]))
    def format_visit(visit):
        return "\t".join([
            visit.timestamp.isoformat(),
            visit.visitor.ip_address,
            visit.visitor.user_agent,
            visit.host,
            visit.path
        ])
    for visit in models.Visit.objects.all().order_by("timestamp"):
        response.write("\n" + format_visit(visit))
    return response
