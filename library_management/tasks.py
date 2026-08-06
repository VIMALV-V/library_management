import frappe
from frappe.utils import today


def check_overdue_books():

    overdue_books = frappe.get_all(
        "Book Issue",
        filters={
            "due_date": ["<", today()],
            "status": "Issued"
        },
        fields=["name", "member", "book"]
    )

    for issue in overdue_books:
        frappe.db.set_value(
            "Book Issue",
            issue.name,
            "status",
            "Overdue"
        )

    frappe.logger().info("Daily overdue book check completed.")


def daily_maintenance():
    frappe.log_error("Daily maintenance job executed")