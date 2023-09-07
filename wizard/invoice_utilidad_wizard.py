from odoo import fields, models, api
from datetime import datetime, timedelta

class XlsInvoiceUtilidadFac(models.Model):
    _name = "xls.invoice.utilidadfac"
    _description = "Invoice Utilidad"

    fecha_ini = fields.Date(string='Fecha inicial', required=True)
    fecha_fin = fields.Date(string='Fecha final', required=True)
    no_resultado = fields.Boolean(string='No Result', default=False)

    def print_xls_utilidad(self, context=None):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'xls.invoice.utilidadfac'
        datas['form'] = self.read()[0]
        return self.env.ref('utilidad_facturas.utilidadfac_invoice_xls').report_action(self, data=datas)