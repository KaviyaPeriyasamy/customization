from erpnext.stock.doctype.item.item import Item
from frappe.model.naming import make_autoname
import frappe, os 
from frappe.utils import get_url
from pyqrcode import create as qrcreate

class ERPNextItem(Item):
    def autoname(self):
        #self.name = make_autoname(self.item_group[0:2].upper()+self.supplier_items[-1].supplier[-2::].upper()+".####", "", self)
        #self.item_code = self.name
        if self.item_group == "Alloy":
            self.item_name = f'{self.alloy_name } {self.hardness} {self. thickness} {self.grade} {self.item_type}'
            self.item_code = f'{self.alloy_name[0:2]}-{self.hardness[0:3]}-{self.thickness[0:3]}-{self.grade[0:3]}- {self.item_type[0:2]}'
        if self.item_group == "Spring ":
            self.item_name = f'{self.coil_hook } {self.length} {self. coil_number }'
            self.item_code = f'{self.coil_hook[0:2]}-{self.length}-{self.coil_number}'
        if self.item_group == "Rivet":
            self.item_name = f'{self.item_type} {self.od}{self.head_diameter}/ {self.shunk_diameter}{self.length} {self.head_type}'
            self.item_code = f'{self.item_type[0:2]}-{ self.od}{self.head_diameter}/ {self.shunk_diameter}{self.length}-{self.head_type[0:3]}' 

def update_qrcode(doc, action):
	if not doc.custom_qr_code:
		folder = create_qrcode_folder()
		png_file_name = '{}.png'.format(frappe.generate_hash(length=20))
		_file = frappe.get_doc({
			"doctype": "File",
			"file_name": png_file_name,
			"folder": folder,
			"content": png_file_name})
		_file.save()
		frappe.db.commit()
		file_url = get_url(_file.file_url)
		file_path = os.path.join(frappe.get_site_path('public', 'files'), _file.file_name)
		url = qrcreate(doc.name)
		with open(file_path, 'wb') as png_file:
			url.png(png_file, scale=2, module_color=[0, 0, 0, 180])
		doc.custom_qr_code =  file_url

def create_qrcode_folder():
	'''Get QRcodes folder.'''
	folder_name = 'QRcodes'
	folder = frappe.db.exists('File', {'file_name': folder_name})
	if folder:
		return folder
	folder = frappe.get_doc({
			'doctype': 'File',
			'file_name': folder_name,
			'is_folder':1,
			'folder': 'Home'
		})
	folder.insert(ignore_permissions=True)
	return folder.name