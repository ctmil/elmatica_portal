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
	def _compute_customer_po(self):
		return_value = 'N/A'
		if self.sale_order:
			return_value = self.sale_order.client_order_ref
		return return_value

	customer_po = fields.Char(string='Customer PO',compute=_compute_customer_po)

class sale_order(models.Model):
	_inherit = 'sale.order'
	
	@api.one
	def _compute_delivery_date(self):
		return_value = None
		if self.picking_ids:
			for picking in self.picking_ids:
				if picking.min_date:
					return_value = picking.min_date
		return return_value

	customer_delivery_date = fields.Date(string='Delivery Date',compute=_compute_delivery_date)
