# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class vn_product_product(models.Model):
    _inherit = "product.product"

    @api.multi
    def open_social_network_form(self):
        """Open a social network form that share product on social network( facebook, zalo,...)"""
        return self.product_tmpl_id.open_social_network_form()
