from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from models.models import Advertisement, ExchangeProposal

User = get_user_model()


class AdvertisementTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass456'
        )

        self.ad1 = Advertisement.objects.create(
            title='Book 1',
            description='Good book',
            user=self.user1,
            category='Books',
            condition='new'
        )
        self.ad2 = Advertisement.objects.create(
            title='Phone X',
            description='Used phone',
            user=self.user2,
            category='Electronics',
            condition='used'
        )

        self.client = APIClient()

    def test_create_advertisement(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:advertisement-list')
        data = {
            'title': 'New Book',
            'description': 'Brand new book',
            'category': "Books",
            'condition': 'new'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 3)
        self.assertEqual(response.data['user'], self.user1.id)

    def test_update_advertisement_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:advertisement-detail', args=[self.ad1.id])
        data = {'title': 'Updated Book Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Updated Book Title')

    def test_delete_advertisement(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:advertisement-detail', args=[self.ad1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Advertisement.objects.count(), 1)

    def test_search_ads(self):
        url = reverse('api:v1:advertisement-list')
        response = self.client.get(url, {'search': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Phone X')

    def test_filter_ads(self):
        url = reverse('api:v1:advertisement-list')
        response = self.client.get(url, {'condition': 'used'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Phone X')


class ExchangeProposalTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass456'
        )

        self.ad1 = Advertisement.objects.create(
            title='Laptop',
            user=self.user1,
            category='Electronics',
            condition='new'
        )
        self.ad2 = Advertisement.objects.create(
            title='Phone',
            user=self.user2,
            category='Electronics',
            condition='used'
        )

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Good offer'
        )

        self.client = APIClient()

    def test_create_proposal(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:proposal-list')
        data = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Test proposal'
        }
        ExchangeProposal.objects.all().delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_update_proposal_status(self):
        self.client.force_authenticate(user=self.user2)  # receiver
        url = reverse('api:v1:proposal-detail', args=[self.proposal.id])
        data = {'status': 'accepted'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'accepted')

    def test_delete_proposal_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:proposal-detail', args=[self.proposal.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExchangeProposal.objects.count(), 0)

    def test_filter_proposals(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:v1:proposal-list')
        response = self.client.get(url, {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_unauthorized_access(self):
        url = reverse('api:v1:proposal-detail', args=[self.proposal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
