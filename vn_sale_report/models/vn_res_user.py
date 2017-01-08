# -*- coding: utf-8 -*-

from odoo import fields, models, api


class vn_res_user(models.Model):
    _inherit = "res.users"

    name = fields.Char(related='partner_id.name', inherited=True, store=True)

    @api.multi
    @api.depends('name')
    def name_get(self):
        result = []
        for user in self:
            name = str(user.id) + ' - ' + user.name
            result.append((user.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        users = self.browse()
        if name.isdigit():
            users = self.search([('id', '=', name)] + args, limit=limit)
        if not users:
            users = self.search([('name', operator, name)] + args, limit=limit)
        return users.name_get()
