from django.urls import reverse, resolve
import pytest

class TestUrl():
    def test_register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'


    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'


    def test_verify_url(self):
        path = reverse('verify')
        assert resolve(path).view_name == 'verify'
