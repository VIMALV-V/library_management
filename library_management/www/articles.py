import frappe


def get_context(context):
    context.title = "Latest News"
    context.no_cache = True

    context.articles = frappe.get_all(
        "Article",
        filters={"status": "Published"},
        fields=["title", "name"],
        order_by="creation desc"
    )
