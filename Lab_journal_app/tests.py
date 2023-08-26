from datetime import datetime

from django.test import TestCase
import pytest
from django.test import Client
from django.urls import reverse
from .models import Position, Method, Sample, Analysis
from django.contrib.auth.models import User


# Create your tests here.

@pytest.mark.django_db
def test_start_page():

    url = reverse('start-page')
    client = Client()
    response = client.get(url)

    assert response.status_code == 200
    assert 'Rejestracja' in str(response.content)

@pytest.mark.django_db
def test_add_user_view():
    url = reverse('user_add')
    client = Client()
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_add_user_view_post():
    url = reverse('user_add')
    position = Position.objects.create(position=10)

    dane = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'position': position.id
    }
    client = Client()
    response = client.post(url, dane)
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_user_view_get():
    url = reverse('login')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_user_view_post():
    user = User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    url = reverse('login')
    client = Client()
    dane = {
        'username': 'Magda',
        'password': 'FoliaAluminiowa',
    }
    response = client.post(url, dane)
    assert response.status_code == 302

@pytest.mark.django_db
def test_logout_user_view():

    user = User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    url = reverse('logout')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('start-page')


@pytest.mark.django_db
def test_main_page_view():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    url = reverse('main-page')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    response = client.get(url)
    assert response.status_code == 200
    assert 'Witaj' in str(response.content)


@pytest.mark.django_db
def test_add_method_view_get():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    url = reverse('add-method')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in str(response.content)

@pytest.mark.django_db
def test_add_method_view_post():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    url = reverse('add-method')
    dane ={ 'name': 'Metoda analiztyczna',
            'description': 'bla bla bla',
            'measurement_name': 'pomiar',
            'measurement_unit': 'jednostka',
            'procedure': 'instrukcja'
    }

    response = client.post(url, dane)
    assert response.status_code == 302
    assert response.url == reverse('method-list')

@pytest.mark.django_db
def test_method_list_view():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('method-list')
    response = client.get(url)

    assert response.status_code == 200
    assert method.name in str(response.content)

@pytest.mark.django_db
def test_delete_method_view():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('delete-method', args=[method.id])

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('method-list')

@pytest.mark.django_db
def test_detail_method_view():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('method-detail', args=[method.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'Procedura pomiarowa' in str(response.content)

@pytest.mark.django_db
def test_modify_method_view_get():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('modify-method', args=[method.id])
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_modify_method_view_post():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')

    name = 'pH roztworu 1'
    description = 'opis 2'
    measurement_name = 'Ta sama'
    measurement_unit = 'Ta sama'
    procedure = 'procedura'

    url = reverse('modify-method', args=[method.id])
    response = client.post(url, {
        'name': name,
        'description': description,
        'measurement_name': measurement_name,
        'measurement_unit': measurement_unit,
        'procedure': procedure
    })

    updated_method = Method.objects.get(id=method.id)

    assert response.status_code == 302
    assert response.url == reverse('method-list')
    assert updated_method.name == name
    assert updated_method.description == description
    assert updated_method.measurement_name == measurement_name
    assert updated_method.measurement_unit == measurement_unit
    assert updated_method.procedure == procedure

@pytest.mark.django_db
def test_sample_add_view_get():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('add-sample')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_result_view_get():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    url = reverse('add-sample')
    response = client.get(url)
    assert response.status_code == 200


class SampleFactory:
    pass


@pytest.mark.django_db
def test_add_result_view_post():
    User.objects.create_user(username='Magda', password='FoliaAluminiowa')
    client = Client()
    assert client.login(username='Magda', password='FoliaAluminiowa')

    method = Method.objects.create(name='pH roztworu')
    sample = Sample.objects.create(
        name='Probka',
        description='probka 1',
        analysis_date=datetime.now()
    )
    url = reverse('add-results', kwargs ={'sample_id': sample.id})
    data = { f'comment_{method.id}':'Komentarz',
             f'result_{method.id}': 130,
             }

    response = client.post(url, data)
    assert response.status_code == 302





