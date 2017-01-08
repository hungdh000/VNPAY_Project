# -*- coding: utf-8 -*-
##############################################################################

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
import datetime

REPORT_TYPES = [('rep_store', 'BÁO CÁO BÁN HÀNG THEO CỬA HÀNG'),
                ('rep_date', 'BÁO CÁO BÁN HÀNG THEO NGÀY'),
                ('rep_product', 'BÁO CÁO BÁN HÀNG THEO HÀNG HÓA'),
                ('rep_group_product', 'BÁO CÁO BÁN HÀNG THEO NHÓM HÀNG HÓA'),
                ('rep_order', 'BÁO CÁO BÁN HÀNG THEO ĐƠN HÀNG'),
                ]

ORDER_TYPES = [(0, 'Tất cả'),
               (1, 'Đơn bán'),
               (2, 'Đơn trả')
               ]

PAYMENT_TYPES = [(0, 'Tất cả'),
                 (1, 'Tiền mặt'),
                 (2, 'QR Pay'),
                 (3, 'Ngân hàng'),
                 ]


def _get_first_day_month():
    todayDate = datetime.date.today()
    first_day = datetime.date(day=1, month=todayDate.month, year=todayDate.year)
    # Use that to find the first day of this month.
    prev_month_end = first_day - datetime.timedelta(days=1)
    prev_month_start = datetime.date(day=1, month=prev_month_end.month, year=prev_month_end.year)
    # first_day = todayDate + relativedelta(day=1, months=-1)
    return prev_month_start.strftime('%Y-%m-%d')


def _get_last_day_month():
    todayDate = datetime.date.today()
    first_day = datetime.date(day=1, month=todayDate.month, year=todayDate.year)
    # Use that to find the first day of this month.
    prev_month_end = first_day - datetime.timedelta(days=1)
    return prev_month_end.strftime('%Y-%m-%d')


class vn_report_sale_order_end_day(models.TransientModel):
    _name = "vn.report.sale.order.end.day"

    type_report = fields.Selection([('rep_store', 'BÁO CÁO BÁN HÀNG THEO CỬA HÀNG'),
                                    ('rep_product', 'BÁO CÁO BÁN HÀNG THEO HÀNG HÓA'),
                                    ('rep_group_product', 'BÁO CÁO BÁN HÀNG THEO NHÓM HÀNG HÓA'),
                                    ('rep_order', 'BÁO CÁO BÁN HÀNG THEO ĐƠN HÀNG'),
                                    ], required=True,
                                   string="Report types")
    type_order = fields.Selection(ORDER_TYPES, string="Order types")
    type_payment = fields.Selection(PAYMENT_TYPES, string="Payment types")
    company_id = fields.Many2one('res.company', string='Store', required=False, store=True, )
    user_id = fields.Many2one('res.users', string='Employee', required=False, default=lambda self: self.env.user)
    customer_id = fields.Many2one('res.partner', string='Customer')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    product_id = fields.Many2one('product.product', string='Product')
    pos_categ_id = fields.Many2one('pos.category', string='Point of Sale Category')
    currency = fields.Char(string="Currency", default=lambda self: self.env.user.company_id.currency_id.name)
    start_date = fields.Date(string="Start date", required=True, default=datetime.date.today(), )
    end_date = fields.Date(string="End date", required=True, default=datetime.date.today(), )

    @api.multi
    @api.onchange('company_id')
    def onchange_user_id(self):
        domain = {}
        val = {}
        if self.company_id.id:
            domain['user_id'] = [('company_id', '=', self.company_id.id)]
        else:
            domain['user_id'] = []
        return {
            'domain': domain,
            'value': {'user_id': False, }
        }

    @api.multi
    def exp_report_sale_xls(self):
        data = {}
        data['model'] = 'vn.report.sale.order.end.day'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.type_report == 'rep_store'):
            if (self.company_id):
                data['company_id'] = self.company_id.id
            else:
                data['company_id'] = -1
            if (self.user_id):
                data['user_id'] = self.user_id.id
            else:
                data['user_id'] = -1
            data.update({'parameters': {
                'PRM_Empl_ID': data['user_id'],
                'PRM_Store_ID': data['company_id'],
                'PRM_Currency': data['currency'],
                'PRM_Date_From': data['date_from'],
                'PRM_Date_To': data['date_to'],
            }})

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_End_Date_XLS',
                'datas': data,
            }

    @api.multi
    def exp_report_sale_pdf(self):
        data = {}
        data['model'] = 'vn.report.sale.order.end.day'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.type_report == 'rep_store'):
            if (self.company_id):
                data['company_id'] = self.company_id.id
            else:
                data['company_id'] = -1
            if (self.user_id):
                data['user_id'] = self.user_id.id
            else:
                data['user_id'] = -1
            data.update({'parameters': {
                'PRM_Empl_ID': data['user_id'],
                'PRM_Store_ID': data['company_id'],
                'PRM_Currency': data['currency'],
                'PRM_Date_From': data['date_from'],
                'PRM_Date_To': data['date_to'],
            }})

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_End_Date_PDF',
                'datas': data,
            }


class vn_report_sale_order_date(models.TransientModel):
    _name = "vn.report.sale.order.date"
    _inherit = "vn.report.sale.order.end.day"

    type_report = fields.Selection(REPORT_TYPES, required=True,
                                   string="Report types")
    start_date = fields.Date(string="Start date", required=True, default=_get_first_day_month(), )
    end_date = fields.Date(string="End date", required=True, default=_get_last_day_month(), )

    @api.multi
    def exp_report_sale_xls(self):
        data = {}
        data['model'] = 'vn.report.sale.order.date'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1

        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_From_Date_To_Date_XLS',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_From_Date_To_Date_XLS',
                'datas': data,
            }

    @api.multi
    def exp_report_sale_pdf(self):
        data = {}
        data['model'] = 'vn.report.sale.order.date'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1
        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_From_Date_To_Date_PDF',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_From_Date_To_Date_PDF',
                'datas': data,
            }


class vn_report_sale_order_quarter(models.TransientModel):
    _name = "vn.report.sale.order.quarter"
    _inherit = "vn.report.sale.order.date"

    first_quarter = fields.Boolean(string="First quarter", default=True)
    second_quarter = fields.Boolean(string="Second quarter")
    third_quarter = fields.Boolean(string="Third quarter")
    four_quarter = fields.Boolean(string="Four quarter")
    year = fields.Selection(
        [(num, str(num)) for num in range(((datetime.datetime.now().year) - 15), ((datetime.datetime.now().year) + 1))],
        default=datetime.datetime.now().year, required=True, )

    @api.multi
    def get_last_day_from_quarter(self):
        if (self.four_quarter):
            date_to = "-12-31"
        elif (self.third_quarter):
            date_to = "-09-30"
        elif (self.second_quarter):
            date_to = "-06-30"
        elif (self.first_quarter):
            date_to = "-03-31"
        return date_to

    @api.multi
    def get_first_day_from_quarter(self):
        if (self.first_quarter):
            date_from = "-01-01"
        elif (self.second_quarter):
            date_from = "-04-01"
        elif (self.third_quarter):
            date_from = "-07-01"
        elif (self.four_quarter):
            date_from = "-10-01"
        return date_from

    @api.multi
    @api.onchange('first_quarter', 'second_quarter', 'third_quarter', 'four_quarter', 'year')
    def onchange_quarter(self):
        start_date = datetime.datetime.strptime(str(self.year) + self.get_first_day_from_quarter(), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(self.year) + self.get_last_day_from_quarter(), "%Y-%m-%d")
        return {
            'value': {'start_date': start_date,
                      'end_date': end_date,
                      }
        }

    @api.multi
    def exp_report_sale_xls(self):
        data = {}
        data['model'] = 'vn.report.sale.order.quarter'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1
        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_Quarter_XLS',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_Quarter_XLS',
                'datas': data,
            }

    @api.multi
    def exp_report_sale_pdf(self):
        data = {}
        data['model'] = 'vn.report.sale.order.quarter'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1
        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_Quarter_PDF',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_Quarter_PDF',
                'datas': data,
            }


class vn_report_sale_order_year(models.TransientModel):
    _name = "vn.report.sale.order.year"
    _inherit = "vn.report.sale.order.date"

    year = fields.Selection(
        [(num, str(num)) for num in range(((datetime.datetime.now().year) - 15), ((datetime.datetime.now().year) + 1))],
        default=datetime.datetime.now().year, required=True, )

    @api.multi
    @api.onchange('year')
    def onchange_year(self):
        start_date = datetime.datetime.strptime(str(self.year) + '-01-01', "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(self.year) + '-12-31', "%Y-%m-%d")
        return {
            'value': {'start_date': start_date,
                      'end_date': end_date,
                      }
        }

    @api.multi
    def exp_report_sale_xls(self):
        data = {}
        data['model'] = 'vn.report.sale.order.quarter'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1
        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_Year_XLS',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_Year_XLS',
                'datas': data,
            }

    @api.multi
    def exp_report_sale_pdf(self):
        data = {}
        data['model'] = 'vn.report.sale.order.quarter'
        data['ids'] = self.ids[0]
        data['date_from'] = self.start_date
        data['date_to'] = self.end_date
        data['currency'] = self.currency
        if (self.company_id):
            data['company_id'] = self.company_id.id
        else:
            data['company_id'] = -1
        if (self.user_id):
            data['user_id'] = self.user_id.id
        else:
            data['user_id'] = -1
        data.update({'parameters': {
            'PRM_Empl_ID': data['user_id'],
            'PRM_Store_ID': data['company_id'],
            'PRM_Currency': data['currency'],
            'PRM_Date_From': data['date_from'],
            'PRM_Date_To': data['date_to'],
        }})

        if (self.type_report == 'rep_store'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Store_Year_PDF',
                'datas': data,
            }
        elif (self.type_report == 'rep_date'):

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'VN_Report_Sale_Year_PDF',
                'datas': data,
            }
