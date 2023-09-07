import xlsxwriter
from odoo import models

class InvoiceUtilidadXls(models.AbstractModel):
    _name = 'report.utilidad_facturas.invoice_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_lines(self, obj):
        lines = []

        domain = [
            ('invoice_date', '>=', obj.fecha_ini),
            ('invoice_date', '<=', obj.fecha_fin),
            ('move_type', '=', 'out_invoice'),
            ('state', '!=', 'draft'),
        ]

        receipt_ids = self.env['account.move'].search(domain)

        for line in receipt_ids:

            EI = IU = ID = IT = 0.0

            for tax in line.invoice_line_ids:
                if tax.tax_ids.impuesto == '002':
                    if tax.tax_ids.amount == 0.0:
                        IU += ((tax.price_unit * tax.quantity) * (tax.tax_ids.amount / 100))
                    elif tax.tax_ids.amount == 16:
                        ID += ((tax.price_unit * tax.quantity) * (tax.tax_ids.amount / 100))
                elif tax.tax_ids.impuesto == '003':
                    IT += ((tax.price_unit * tax.quantity) * (tax.tax_ids.amount / 100))

            if line.tipo_comprobante == 'I':
                comproban = 'Ingreso'
            elif line.tipo_comprobante == 'E':
                comproban = 'Egreso'
            elif line.tipo_comprobante == 'T':
                comproban = 'Traslado'    

            vals = {
                'Dcomprobante': comproban,
                'UUID': line.folio_fiscal,
                'Nfactura': line.number_folio,
                'RFC': line.partner_id.vat,
                'Rsocial': line.partner_id.name,
                'Subtotal': line.subtotal, #tal vez
                'Descuentos': line.discount,
                'ExcentoIva': EI,
                'ImpuestoU': IU,
                'ImpuestoD': ID,
                'ImpuestoT': IT,
                'Total': line.total_factura, #tal vez
                'FechaF': line.invoice_date, #tal vez
                'FechaT': line.fecha_factura,
            }
            lines.append(vals)

        return lines
    
    def generate_xlsx_report(self, workbook, data, wizard_obj):
        for obj in wizard_obj:
            lines = self.get_lines(obj)
            worksheet = workbook.add_worksheet('Reporte de utilidad')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})

            worksheet.merge_range('A1:B1', 'Ingresos Ventas', bold)
            worksheet.set_row(0, 30)

            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 2, 40)
            worksheet.set_column(3, 3, 25)
            worksheet.set_column(4, 4, 25)
            worksheet.set_column(5, 5, 45)
            worksheet.set_column(6, 6, 25)
            worksheet.set_column(7, 7, 25)
            worksheet.set_column(8, 8, 25)
            worksheet.set_column(9, 9, 25)
            worksheet.set_column(10, 10, 25)
            worksheet.set_column(11, 11, 45)
            worksheet.set_column(12, 12, 25)
            worksheet.set_column(13, 13, 25)

            worksheet.write('A2', 'Detalle tipo de comprobante', bold)
            worksheet.write('B2', 'UUID(Folio Fiscal)', bold)
            worksheet.write('C2', 'Numero Factura', bold)
            worksheet.write('D2', 'RFC', bold)
            worksheet.write('E2', 'Razon social', bold)
            worksheet.write('F2', 'Subtotal(Antes de impuestos y descuentos)', bold)
            worksheet.write('G2', 'Descuentos', bold)
            worksheet.write('H2', 'Excento de IVA', bold)
            worksheet.write('I2', 'Impuesto(IVA 0%)', bold)
            worksheet.write('J2', 'Impuesto(IVA 16%)', bold)
            worksheet.write('K2', 'Impuesto(IEPS 8%)', bold)
            worksheet.write('L2', 'Total(Subtotal - descuento + impuestos)', bold)
            worksheet.write('M2', 'Fecha Factura', bold)
            worksheet.write('N2', 'Fecha de timbrado', bold)
            row = 2
            col = 0
            for res in lines:
                worksheet.write(row, col, res['Dcomprobante'], text)
                worksheet.write(row, col + 1, res['UUID'], text)
                worksheet.write(row, col + 2, res['Nfactura'], text)
                worksheet.write(row, col + 3, res['RFC'], text)
                worksheet.write(row, col + 4, res['Rsocial'], text)
                worksheet.write(row, col + 5, str(self.env.user.company_id.currency_id.symbol) + str(res['Subtotal']), text)
                worksheet.write(row, col + 6, str(self.env.user.company_id.currency_id.symbol) + str(res['Descuentos']), text)
                worksheet.write(row, col + 7, str(self.env.user.company_id.currency_id.symbol) + str(res['ExcentoIva']), text)
                worksheet.write(row, col + 8, str(self.env.user.company_id.currency_id.symbol) + str(res['ImpuestoU']), text)
                worksheet.write(row, col + 9, str(self.env.user.company_id.currency_id.symbol) + str(res['ImpuestoD']), text)
                worksheet.write(row, col + 10, str(self.env.user.company_id.currency_id.symbol) + str(res['ImpuestoT']), text)
                worksheet.write(row, col + 11, str(self.env.user.company_id.currency_id.symbol) + str(res['Total']), text)
                fecha = res['FechaF'].strftime('%d/%m/%Y')
                worksheet.write(row, col + 12, fecha, text)
                fechad = res['FechaT'].strftime('%d/%m/%Y')
                worksheet.write(row, col + 13, fechad, text)
                row = row + 1