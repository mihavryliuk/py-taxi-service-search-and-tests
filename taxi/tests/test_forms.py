from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)
from taxi.models import Car, Manufacturer, Driver


class FormsTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="ABC12345"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": self.car.model,
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver.pk],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "DEF67890",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)

        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "XYZ67890"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validate_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "GHI12345",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)

        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test Model")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "testdriver"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testdriver")
