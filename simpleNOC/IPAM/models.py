from django.db import models
from netfields import CidrAddressField, InetAddressField

class Subnet(models.Model):
    CIDR = CidrAddressField()

class IP(models.Model):
    address = InetAddressField(store_prefix_length=False)
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
