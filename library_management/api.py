import frappe
from frappe.utils import today, getdate
from frappe.query_builder import DocType

import os
import barcode
from barcode.writer import ImageWriter

@frappe.whitelist()
def check_book_status(book):
    """
    Check whether a book is available or already issued.
    """

    existing_issue = frappe.db.exists(
        "Book Issue",
        {
            "book": book,
            "status": "Issued"
        }
    )

    if existing_issue:
        return {
            "available": False,
            "status": "Issued"
        }

    return {
        "available": True,
        "status": "Available"
    }


@frappe.whitelist()
def calculate_fine(issue_name):
    """
    Calculate overdue fine for a Book Issue.
    Fine = ₹10 per overdue day.
    """

    issue = frappe.get_doc("Book Issue", issue_name)

    due_date = getdate(issue.due_date)
    current_date = getdate(today())

    overdue_days = (current_date - due_date).days

    if overdue_days < 0:
        overdue_days = 0

    fine = overdue_days * 10

    return {
        "issue": issue.name,
        "days": overdue_days,
        "fine": fine
    }


@frappe.whitelist()
def create_task(task_subject):
    task = frappe.new_doc("Task")
    task.subject = task_subject
    task.save()

    return task.name


@frappe.whitelist()
def todo_validate(doc, method):
    frappe.msgprint("Hook executed!")





@frappe.whitelist()
def document_api_demo():

    Book = DocType("Book")
    Category = DocType("Category")

    books = (
        frappe.qb.from_(Book)
        .join(Category)
        .on(Book.category == Category.name)
        .select(
            Book.name,
            Book.book_title,
            Category.category_name
        )
        .limit(5)
    ).run(as_dict=True)

    
    if books:
        book = frappe.get_doc("Book", books[0]["name"])

        book.available = "Available"

        book.save()

    
    for b in books:
        frappe.db.set_value(
            "Book",
            b["name"],
            "available",
            "Available"
        )

    return books


@frappe.whitelist()
def generate_barcode(book_name):
    code128 = barcode.get("code128", book_name, writer=ImageWriter())

    file_name = f"{book_name}.png"

    output_path = os.path.join(
        frappe.get_site_path("public", "files"),
        book_name
    )

    code128.save(output_path)

    file_url = f"/files/{file_name}"

    frappe.db.set_value(
        "Book",
        book_name,
        "barcode_image",
        file_url
    )

    frappe.db.commit()

    return file_url


@frappe.whitelist()
def todo_api_demo():

    todos = frappe.get_list(
        "ToDo",
        fields=["name", "description", "owner"],
        order_by="creation desc",
        limit=5
    )

    for todo in todos:
        todo["email"] = frappe.db.get_value(
            "User",
            todo["owner"],
            "email"
        )

    return {
        "timestamp": frappe.utils.now(),
        "records": todos
    }