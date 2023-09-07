{
    'name': 'Reporte de Utilidad',
    'version': '16.01',
    'description': ''' Reporte de utilidad exportable a XLS
    ''',
    'category': 'Stock',
    'author': 'IT Admin',
    'website': 'http://www.itadmin.com.mx',
    'depends': [
        'base','stock', 'account', 'cdfi_invoice','report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_utilidad_wizard.xml',
        'views/invoice_utilidad_id.xml',
    ],
    'application': False,
    'installable': True,
}