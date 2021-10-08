from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def make_custom_fields(update=True):
	custom_fields = {
    'Item': [
		{
			'fieldname': 'custom_qr_code',
			'label': 'QR Code',
			'fieldtype': 'Attach Image',
			'insert_after': 'stock_uom'
		},
        {
			'fieldname': 'no_of_labels_required',
			'label': 'No of Labels Required',
			'fieldtype': 'Int',
			'insert_after': 'custom_qr_code'
		}
	]
	}
	create_custom_fields(
	custom_fields, ignore_validate=frappe.flags.in_patch, update=update)
