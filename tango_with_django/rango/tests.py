from django.test import TestCase
from rango.models import Category
from django.core.urlresolvers import reverse

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        #Make sure that views cannot be negative
        cat = Category(name="test",views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        #Make sure a new slug is created when a new Category is created

        cat = Category(name = "Random Category String")
        cat.save()
        self.assertEqual(cat.slug, "random-category-string")

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        #Make sure when no categories exist a message is displayed
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context["categories"],[])

    def test_index_view_with_categories(self):
        #Make sure that the categories are displayed in the index view
        add_cat("test",1,1)
        add_cat("temp",1,1)
        add_cat("tmp",1,1)
        add_cat("tmp temp test",1,1)

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp temp test")

        num_cats = len(response.context["categories"])
        self.assertEqual(num_cats, 4)
