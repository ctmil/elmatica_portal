{
    'name': 'Elmatica - Portal Module',
    'category': 'Sales',
    'version': '0.1',
    # 'depends': ['base','elmatica_sales_purchase','portal_purchase','elmatica_tickets'],
    'depends': ['base','elmatica_sales_purchase','portal_purchase','sale','elmatica_tickets'],
    'data': [
	'portal_view.xml',
    ],
    'demo': [
    ],
    'qweb': [],
    # 'css': ['static/src/css/styles.css',],
    'installable': True,
}
