from django.test import TestCase
from IPAM.models import Subnet, IP
from ipaddress import ip_network, ip_address

class IPAMModelTest(TestCase):
    def test_subnet(self):
        first_subnet = Subnet()
        first_subnet.CIDR = '192.168.0.0/24'
        first_subnet.save()

        second_subnet = Subnet()
        second_subnet.CIDR = '192.168.1.0/24'
        second_subnet.save()

        saved_sabnets = Subnet.objects.all()
        self.assertEqual(saved_sabnets.count(), 2)

        first_saved_subnet = saved_sabnets[0]
        second_saved_subnet = saved_sabnets[1]
        self.assertEqual(first_saved_subnet.CIDR, ip_network('192.168.0.0/24'))
        self.assertEqual(second_saved_subnet.CIDR, ip_network('192.168.1.0/24'))

    def test_ip(self):
        subnet = Subnet(CIDR='192.168.0.0/24')
        subnet.save()

        first_ip = IP()
        first_ip.address = '192.168.0.1'
        first_ip.subnet = subnet
        first_ip.save()

        second_ip = IP()
        second_ip.address = '192.168.0.2'
        second_ip.subnet = subnet
        second_ip.save()

        saved_ips = IP.objects.all()
        self.assertEqual(saved_ips.count(), 2)

        first_saved_ip = saved_ips[0]
        second_saved_ip = saved_ips[1]
        self.assertEqual(first_saved_ip.address, ip_address('192.168.0.1'))
        self.assertEqual(first_saved_ip.subnet, subnet)
        self.assertEqual(second_saved_ip.address, ip_address('192.168.0.2'))
        self.assertEqual(second_saved_ip.subnet, subnet)
