import frappe
from frappe.tests import IntegrationTestCase


class TestArticle(IntegrationTestCase):

    def test_article_creation(self):
        article = frappe.get_doc({
            "doctype": "Article",
            "title": "My First Test",
            "status": "Published"
        })

        article.insert()

        self.assertEqual(article.title, "My First Test")
        self.assertTrue(
            frappe.db.exists("Article", article.name)
        )