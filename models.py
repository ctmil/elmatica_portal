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

	customer_po = fields.Char(string='Customer PO',related='sale_order.client_order_ref')
