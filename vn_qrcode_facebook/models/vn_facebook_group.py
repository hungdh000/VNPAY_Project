# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class vn_facebook_group(models.TransientModel):
    _name = "vn.facebook.group"
    _description = "Facebook Group"

    group_id = fields.Integer(string="Facebook Group ID", require=True)
    group_name = fields.Char(string="Facebook Group Name")


