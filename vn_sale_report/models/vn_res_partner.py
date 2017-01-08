# -*- coding: utf-8 -*-

from odoo import fields, models, api


class vn_res_partner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''

            if partner.company_name or partner.parent_id:
                if not name and partner.type in ['invoice', 'delivery', 'other']:
                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
                if not partner.is_company:
                    name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')

            name = str(partner.id) + ' - ' + name
            res.append((partner.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        res = super(vn_res_partner, self).name_search(name, args, operator=operator, limit=limit)
        if not res and name.isdigit():
            partner = self.search([('id', '=', name)] + args, limit=limit)
            return partner.name_get()
        else:
            return super(vn_res_partner, self).name_search(name, args, operator=operator, limit=limit)
