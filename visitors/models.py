from django.db import models


class Visitor(models.Model):

    ip_address = models.CharField(max_length=20)
    user_agent = models.CharField(max_length=255)

    def __str__(self):
        return "Visitor<%s>" % self.ip_address


class Visit(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    visitor = models.ForeignKey("Visitor", on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    host = models.CharField(max_length=255)

    def __str__(self):
        return "Visit<%s|%s>" % (self.timestamp, self.visitor)
