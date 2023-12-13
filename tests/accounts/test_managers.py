from accounts.models import User
import pytest

class TestCustomUserManager:
    pytestmark = pytest.mark.django_db
    def test_create_user_managers(self):
        user = User.objects.create_user(email="test@test.com", password="password")
        assert (isinstance(user, User))

    def test_create_user_blank_email(self):
        with pytest.raises(ValueError) as excinfo:  
            user = User.objects.create_user(email="", password="password")

        assert str(excinfo.value) == "The Email must be set"

    def test_create_superuser_managers(self):
        user = User.objects.create_superuser(email="test@test.com", password="password", is_staff=True, is_active=True, is_superuser=True)
        assert (isinstance(user, User))


    def test_create_superuser_is_staff_false(self):
        with pytest.raises(ValueError) as excinfo:  
            user = User.objects.create_superuser(email="test@test.com", password="password", is_staff=False, is_active=True, is_superuser=True)

        assert str(excinfo.value) == "Superuser must have is_staff=True."

    
    def test_create_superuser_is_superuser_false(self):
        with pytest.raises(ValueError) as excinfo:  
            user = User.objects.create_superuser(email="test@test.com", password="password", is_staff=True, is_active=True, is_superuser=False)

        assert str(excinfo.value) == "Superuser must have is_superuser=True."