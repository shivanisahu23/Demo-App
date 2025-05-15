from erpnext.accounts.doctype.accounting_period.accounting_period import AccountingPeriod, OverlapError
import frappe

def validate(doc, method):
	pass
#     # custom_fiscal_year || custom_month || custom_branch (Shouldn't be same)
#     lst = frappe.db.exists("Accounting Period", {"custom_fiscal_year": doc.custom_fiscal_year, "custom_month": doc.custom_month, "custom_month": doc.custom_month})
#     # if doc.custom_fiscal_year ==  and doc.custom_month and doc.custom_branch/
#     if lst:
#         frappe.throw("This record already exists")
    


class CustomAccountingPeriod(AccountingPeriod):
	
	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from erpnext.accounts.doctype.closed_document.closed_document import ClosedDocument

		closed_documents: DF.Table[ClosedDocument]
		company: DF.Link
		end_date: DF.Date
		period_name: DF.Data
		start_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_overlap()
		print("==========")

	def before_insert(self):
		self.bootstrap_doctypes_for_closing()

	def autoname(self):
		company_abbr = frappe.get_cached_value("Company", self.company, "abbr")
		self.name = " - ".join([self.period_name, company_abbr])

	def validate_overlap(self):
		existing_accounting_period = frappe.db.sql(
			"""select name from `tabAccounting Period`
			where (
				(%(start_date)s between start_date and end_date)
				or (%(end_date)s between start_date and end_date)
				or (start_date between %(start_date)s and %(end_date)s)
				or (end_date between %(start_date)s and %(end_date)s)
			) and name!=%(name)s and company=%(company)s and custom_branch = %(custom_branch)s""",
			{
				"start_date": self.start_date,
				"end_date": self.end_date,
				"name": self.name,
				"company": self.company,
				"custom_branch": self.custom_branch,
			},
			as_dict=True, debug = 1
		)

		if len(existing_accounting_period) > 0:
			frappe.throw(
				frappe._("Accounting Period overlaps with {0}").format(existing_accounting_period[0].get("name")),
				OverlapError,
			)

	@frappe.whitelist()
	def get_doctypes_for_closing(self):
		docs_for_closing = []
		# get period closing doctypes from all the apps
		doctypes = frappe.get_hooks("period_closing_doctypes")

		closed_doctypes = [{"document_type": doctype, "closed": 1} for doctype in doctypes]
		for closed_doctype in closed_doctypes:
			docs_for_closing.append(closed_doctype)

		return docs_for_closing

	def bootstrap_doctypes_for_closing(self):
		if len(self.closed_documents) == 0:
			for doctype_for_closing in self.get_doctypes_for_closing():
				self.append(
					"closed_documents",
					{
						"document_type": doctype_for_closing.document_type,
						"closed": doctype_for_closing.closed,
					},
				)




