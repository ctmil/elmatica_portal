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

class product_supplierinfo(models.Model):
	_inherit = 'product.supplierinfo'

	@api.one
	def _compute_product_supplierinfo_portal_url(self):
		#http://localhost:8069/web?db=elmatica_v1#id=377&view_type=form&model=sale.order&menu_id=471&action=645
		dbname = self.env.cr.dbname
		parameter_url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                if not parameter_url:
                        raise osv.except_osv(('Error'), ('portal_url parameter missing!!!'))
                        return None
		parameter_url = parameter_url.value
                action_ids = self.env['ir.actions.act_window'].sudo().search([('res_model','=','product.supplierinfo'),\
				('view_type','=','form')])
                if action_ids:
		#Portal/Elmatica/Sale Orders
		#menu_item = self.env['ir.ui.menu'].sudo().search([('complete_name','=','Portal/Elmatica/Sale Orders')])
		#if not menu_item:
                #        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                #        return None 					      portal.purchase.order.form
		#view_ids = self.env['ir.ui.view'].sudo().search([('name','=','portal.purchase.order.form')])
		#if not view_ids:
                #        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                #        return None
			for action_id in action_ids:
				return_url = parameter_url + '/web?='+dbname+'#id'+str(self.id)+\
					"&view_type=form&model=product.supplierinfo&action="+str(action_id.id)
			self.product_supplierinfo_portal_url = return_url

	product_supplierinfo_portal_url = fields.Char(string='Suppplier Info Portal URL',compute=_compute_product_supplierinfo_portal_url)

class purchase_order(models.Model):
        _inherit = 'purchase.order'

        @api.one
        def _compute_purchase_order_portal_url(self):
                #http://localhost:8069/web?db=elmatica_v1#id=377&view_type=form&model=sale.order&menu_id=471&action=645
                dbname = self.env.cr.dbname
                parameter_url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                if not parameter_url:
                        raise osv.except_osv(('Error'), ('portal_url parameter missing!!!'))
                        return None
                parameter_url = parameter_url.value
                #Portal/Elmatica/Sale Orders
                #menu_item = self.env['ir.ui.menu'].sudo().search([('complete_name','=','Portal/Elmatica/Sale Orders')])
                #if not menu_item:
                #        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                #        return None                                          portal.purchase.order.form
                #view_ids = self.env['ir.ui.view'].sudo().search([('name','=','portal.purchase.order.form')])
                #if not view_ids:
                #        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                #        return None
                #for view_id in view_ids:
                action_id = self.env['ir.actions.act_window'].sudo().search([('name','=','portal.purchase.order')])
                if action_id:
                        return_url = parameter_url + '/web?='+dbname+'#id'+str(self.id)+\
                                "&view_type=form&model=purchase.order&action="+str(action_id.id)
                        self.purchase_order_portal_url = return_url
                        return
                raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))

        purchase_order_portal_url = fields.Char(string='PO Portal URL',compute=_compute_purchase_order_portal_url)



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

	@api.one
	def _compute_sale_order_portal_url(self):
		#http://localhost:8069/web?db=elmatica_v1#id=377&view_type=form&model=sale.order&menu_id=471&action=645
		dbname = self.env.cr.dbname
		parameter_url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                if not parameter_url:
                        raise osv.except_osv(('Error'), ('portal_url parameter missing!!!'))
                        return None
		parameter_url = parameter_url.value
		#Portal/Elmatica/Sale Orders
		#menu_item = self.env['ir.ui.menu'].sudo().search([('complete_name','=','Portal/Elmatica/Sale Orders')])
		#if not menu_item:
                #        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                #        return None
		view_ids = self.env['ir.ui.view'].sudo().search([('name','=','portal.sale.order.form')])
		if not view_ids:
                        raise osv.except_osv(('Error'), ('elmatica_portal module is not  installed!!!'))
                        return None
		for view_id in view_ids:
			action_id = self.env['ir.actions.act_window'].sudo().search([('view_id','=',view_id.id)])
			if action_id:
				return_url = parameter_url + '/web?='+dbname+'#id'+str(self.id)+\
					"&view_type=form&model=sale.order&action="+str(action_id.id)
				self.sale_order_portal_url = return_url
				return
			
		

	customer_delivery_date = fields.Date(string='Delivery Date',compute=_compute_delivery_date)
	sale_order_portal_url = fields.Char(string='SO Portal URL',compute=_compute_sale_order_portal_url)
