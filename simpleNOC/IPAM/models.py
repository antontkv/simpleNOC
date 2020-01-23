from django.db import models
from netfields import CidrAddressField

class Subnet(models.Model):
    CIDR = CidrAddressField()
