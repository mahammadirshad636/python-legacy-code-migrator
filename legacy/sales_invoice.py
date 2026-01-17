# Copyright (c) 2019
# ERPNext Legacy DocType Controller

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class SalesInvoice(Document):
    def validate(self):
        self.validate_items()
        self.calculate_totals()
        self.validate_credit_limit()

    def before_submit(self):
        self.update_stock_ledger()
        self.create_gl_entries()

    def on_cancel(self):
        self.reverse_gl_entries()
        self.update_stock_ledger(cancel=True)

    # ---------------------------
    # Validation
    # ---------------------------

    def validate_items(self):
        if not self.items:
            frappe.throw(_("Sales Invoice must have at least one item"))

        for row in self.items:
            if flt(row.qty) <= 0:
                frappe.throw(_("Quantity must be greater than zero"))

            if not row.rate:
                row.rate = self.get_item_price(row.item_code)

    def validate_credit_limit(self):
        if not self.customer:
            return

        credit_limit = frappe.db.get_value(
            "Customer", self.customer, "credit_limit"
        ) or 0

        outstanding = frappe.db.sql(
            """
            SELECT SUM(outstanding_amount)
            FROM `tabSales Invoice`
            WHERE customer=%s AND docstatus=1
            """,
            self.customer
        )[0][0] or 0

        if outstanding + self.grand_total > credit_limit:
            frappe.throw(_("Customer credit limit exceeded"))

    # ---------------------------
    # Calculations
    # ---------------------------

    def calculate_totals(self):
        self.total = 0
        self.total_qty = 0

        for row in self.items:
            row.amount = flt(row.qty) * flt(row.rate)
            self.total += row.amount
            self.total_qty += flt(row.qty)

        self.grand_total = self.total - flt(self.discount_amount)

    def get_item_price(self, item_code):
        price = frappe.db.get_value(
            "Item Price",
            {"item_code": item_code, "selling": 1},
            "price_list_rate"
        )
        return price or 0

    # ---------------------------
    # Stock
    # ---------------------------

    def update_stock_ledger(self, cancel=False):
        for row in self.items:
            qty = -row.qty if not cancel else row.qty

            frappe.db.sql(
                """
                INSERT INTO `tabStock Ledger Entry`
                (item_code, warehouse, actual_qty, posting_date, voucher_no)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    row.item_code,
                    row.warehouse,
                    qty,
                    nowdate(),
                    self.name
                )
            )

    # ---------------------------
    # Accounting
    # ---------------------------

    def create_gl_entries(self):
        if not self.grand_total:
            return

        frappe.db.sql(
            """
            INSERT INTO `tabGL Entry`
            (posting_date, account, debit, credit, voucher_no)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                nowdate(),
                "Debtors - CO",
                self.grand_total,
                0,
                self.name
            )
        )

    def reverse_gl_entries(self):
        frappe.db.sql(
            """
            DELETE FROM `tabGL Entry`
            WHERE voucher_no=%s
            """,
            self.name
        )


@frappe.whitelist()
def make_sales_invoice_from_order(sales_order):
    so = frappe.get_doc("Sales Order", sales_order)

    inv = frappe.new_doc("Sales Invoice")
    inv.customer = so.customer

    for row in so.items:
        inv.append("items", {
            "item_code": row.item_code,
            "qty": row.qty,
            "rate": row.rate,
            "warehouse": row.warehouse
        })

    inv.insert()
    return inv.name
