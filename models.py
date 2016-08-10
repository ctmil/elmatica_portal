from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	@api.one
	def _compute_sale_id(self):
		return_value = None
		for line in self.invoice_line:
			if line.order_id:
				return_value = line.order_id.id
		return return_value 

	@api.one
	def _compute_customer_po(self):
		return_value = 'N/A'
		if self.sale_id:
			return_value = self.sale_id.client_order_ref
		return return_value

	customer_po = fields.Char(string='Customer PO',compute=_compute_customer_po)
	sale_id = fields.Many2one('sale.order',string='Elmatica SO',compute=_compute_sale_id)
