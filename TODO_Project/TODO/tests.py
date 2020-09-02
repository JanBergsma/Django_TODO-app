import logging
import inspect
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .models import Item
from .views import IndexView, CreateView, UpdateView, ClearDeletedView

logger = logging.getLogger(__name__)


class TestUrls(SimpleTestCase):
    def test_slash_is_resolved(self):
        url = reverse('TODO:index')
        self.assertEquals(url, '/')
        resolved = resolve(url)

        expected = f'{IndexView}'.split("'")[1]
        result = resolved._func_path
        self.assertEquals(expected, result)


class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(title="todo 1")
        Item.objects.create(title="todo 2", completed=True)
        Item.objects.create(title="todo 3", completed=False)
        Item.objects.create(title="todo 4", completed=True)

    def test_smoke_test(self):
        self.assertTrue(True)


