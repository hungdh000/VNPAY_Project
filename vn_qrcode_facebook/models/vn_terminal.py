# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging
from odoo import tools, _
from odoo.tools import config

_logger = logging.getLogger(__name__)


class vn_terminal(models.Model):
    _name = "vn.terminal"
    _description = "Desciption terminal information"

    terminal_id = fields.Integer(string="Terminal ID", require=True)
    terminal_name = fields.Char(string="Terminal name")
