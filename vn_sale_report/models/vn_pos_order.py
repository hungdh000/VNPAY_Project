# -*- coding: utf-8 -*-

from odoo import fields, models, api


class vn_pos_order(models.Model):
    _inherit = "pos.order"

    amount_tax = fields.Float(compute='_compute_amount_all', string='Taxes', digits=0, store=True)
    amount_total = fields.Float(compute='_compute_amount_all', string='Total', digits=0, store=True)
    amount_paid = fields.Float(compute='_compute_amount_all', string='Paid', states={'draft': [('readonly', False)]},
                               readonly=True, digits=0, store=True)
    amount_return = fields.Float(compute='_compute_amount_all', string='Returned', digits=0, store=True)