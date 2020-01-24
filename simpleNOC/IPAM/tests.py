from django.test import TestCase
from IPAM.models import Subnet, IP
from ipaddress import ip_network, ip_address
from unittest import skip
from IPAM import helpers as ipam_helpers

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

    def test_add_multiple_subnets(self):
        valid_subnets = ['192.168.0.0/24', '192.168.1.0/24', '10.10.10.10/32']
        invalid_subnets = ['dfdsf', '10.10/24', '192.168.1.1/24', '192.168.1.2']

        submission = ipam_helpers.add_multiple_subnets(
            '\r\n'.join(valid_subnets + invalid_subnets)
        )

        self.assertEqual(submission[0], valid_subnets)
        self.assertEqual(submission[1], invalid_subnets)
        self.assertEqual(Subnet.objects.all().count(), 0)

        ipam_helpers.add_multiple_subnets(
            '\r\n'.join(valid_subnets + invalid_subnets),
            True
        )
        saved_subnets = Subnet.objects.all()
        self.assertEqual(saved_subnets.count(), 3)
        for index, valid_subnet in enumerate(valid_subnets):
            self.assertEqual(saved_subnets[index].CIDR, ip_network(valid_subnet))

class IPAMViewTest(TestCase):
    def test_adding_new_subnets(self):
        valid_subnets = ['192.168.0.0/24', '192.168.1.0/24', '10.10.10.10/32']
        invalid_subnets = ['dfdsf', '10.10/24', '192.168.1.1/24', '192.168.1.2']

        # Tests for /add_subnets
        response = self.client.get('/ipam/add_subnets/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ipam/add_subnets.html')

        response = self.client.post(
            '/ipam/add_subnets/',
            data={'subnets_to_add': '\r\n'.join(valid_subnets + invalid_subnets)}
        )
        self.assertRedirects(response, "/ipam/add_subnets/summary/")
        session_valid_subnets = self.client.session.get('valid_subnets')
        session_invalid_subnets = self.client.session.get('invalid_subnets')
        self.assertEqual(session_valid_subnets, valid_subnets)
        self.assertEqual(session_invalid_subnets, invalid_subnets)

        # Tests for /add_subnets/summary cansel behavior
        response = self.client.post(
            '/ipam/add_subnets/summary/',
            data={'cancel': ['Cancel']}
        )
        self.assertRedirects(response, "/ipam/add_subnets/")
        self.assertEqual(Subnet.objects.all().count(), 0)

        # Tests for /add_subnets/summary add behavior
        response = self.client.post(
            '/ipam/add_subnets/summary/',
            data={'add_subnets': ['Add']}
        )
        self.assertRedirects(response, "/ipam/add_subnets/")
        saved_subnets = Subnet.objects.all()
        self.assertEqual(saved_subnets.count(), 3)
        for index, valid_subnet in enumerate(valid_subnets):
            self.assertEqual(saved_subnets[index].CIDR, ip_network(valid_subnet))
