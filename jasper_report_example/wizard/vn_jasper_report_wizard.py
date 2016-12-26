# -*- coding: utf-8 -*-
##############################################################################

from odoo import fields, models, api


class sale_order_report_wizard(models.TransientModel):
    _name = "vn.sale.order.report.wizard"

    date_from = fields.Date('From')
    date_to = fields.Date('To')

    @api.multi
    def exp_report_sale_order_xls(self):
        data = {}
        data['model'] = 'vn.sale.order.report.wizard'
        data['ids']=self.ids[0]
        data['date_from'] = self.date_from
        data['date_to'] = self.date_to
        data.update({'parameters': {
            'date_from': data['date_from'],
            'date_to': data['date_to']
        }
        })

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'VNPAY_Report_Sale_Order_XLS',
            'datas': data,
        }

    @api.multi
    def exp_report_sale_order_pdf(self):
        data = {}
        data['model'] = 'vn.sale.order.report.wizard'
        data['ids'] = self.ids[0]
        data['date_from'] = self.date_from
        data['date_to'] = self.date_to
        data.update({'parameters': {
            'date_from': data['date_from'],
            'date_to': data['date_to']
        }
        })

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'VNPAY_Report_Sale_Order_PDF',
            'datas': data,
        }


