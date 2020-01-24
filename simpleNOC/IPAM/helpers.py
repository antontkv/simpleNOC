from IPAM.models import Subnet
from django.core.exceptions import ValidationError

def add_multiple_subnets(input_, save=False):
    """
    Takes as input list of subnets divided by “\\r\\n”.
    Returns tuple (valid_subnets, invalid_subnets).
    Saves valid subnets to DB, if save is True.
    """
    subnets = input_.split('\r\n')
    valid_subnets, invalid_subnets = [], []

    for subnet_candidat in subnets:
        if '/' not in subnet_candidat:
            invalid_subnets.append(subnet_candidat)
            continue

        try:
            subnet = Subnet()
            subnet.CIDR = subnet_candidat
            subnet.full_clean()
            valid_subnets.append(subnet_candidat)
            if save:
                subnet.save()
        except ValidationError:
            invalid_subnets.append(subnet_candidat)

    return (valid_subnets, invalid_subnets)
