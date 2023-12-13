import pytest
from accounts.models import User, OneTimePassword

@pytest.fixture
def first_user(db, user_factory):
    user = user_factory.create(email="jhon-doe@gmail.com", first_name="Jhon", last_name="Doe")
    return user

@pytest.fixture
def admin_user(db, user_factory):
    user = user_factory.create(email="admin@gmail.com", first_name="admin", is_staff=True, is_active=True, is_superuser=True)
    return user

class TestUser:
    pytestmark = pytest.mark.django_db
    def test_user_create(self, first_user):
        assert first_user.email == "jhon-doe@gmail.com"

    def test_get_user_full_name(self, first_user):
        user = User.objects.get(email='jhon-doe@gmail.com')
        assert user.first_name == "Jhon"
        assert user.get_full_name == "Jhon Doe"

    def test_user_str_fun(self, first_user):
        user = User.objects.get(email='jhon-doe@gmail.com')
        assert str(user) == 'jhon-doe@gmail.com'

    def test_one_time_password_str_fun(self, first_user):
        user = User.objects.get(email='jhon-doe@gmail.com')
        otp = OneTimePassword.objects.create(user=user, otp=123456)
        assert str(otp) == 'Jhon- passcode'

    
