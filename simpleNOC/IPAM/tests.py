from django.test import TestCase
from IPAM.models import Subnet
from ipaddress import ip_network

class IPAMModelTest(TestCase):
    def test_subnet(self):
        first_subnet = Subnet()
        first_subnet.CIDR = "192.168.0.0/24"
        first_subnet.save()

        second_subnet = Subnet()
        second_subnet.CIDR = "192.168.1.0/24"
        second_subnet.save()

        saved_sabnets = Subnet.objects.all()
        self.assertEqual(saved_sabnets.count(), 2)

        first_saved_subnet = saved_sabnets[0]
        second_saved_subnet = saved_sabnets[1]
        self.assertEqual(first_saved_subnet.CIDR, ip_network("192.168.0.0/24"))
        self.assertEqual(second_saved_subnet.CIDR, ip_network("192.168.1.0/24"))
