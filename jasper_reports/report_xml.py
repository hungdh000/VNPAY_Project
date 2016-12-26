# encoding: iso-8859-15
##############################################################################
#
# Copyright (c) 2008-2012 NaN Projectes de Programari Lliure, S.L.
#                         http://www.NaN-tic.com
# Copyright (C) 2013 Tadeus Prastowo <tadeus.prastowo@infi-nity.com>
#                         Vikasa Infinity Anugrah <http://www.infi-nity.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import os
import base64

import odoo
from odoo import release
from odoo import report
from odoo import api, fields, models
from . import jasper_report
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError

import unicodedata
from xml.dom.minidom import getDOMImplementation

src_chars = """ '"()/*-+?¿!&$[]{}@#`'^:;<>=~%,\\"""
src_chars = unicode(src_chars, 'iso-8859-1')
dst_chars = """________________________________"""
dst_chars = unicode(dst_chars, 'iso-8859-1')


class report_xml_file(models.Model):
    _name = 'ir.actions.report.xml.file'

    file = fields.Binary('File', required=True, filters="*.jrxml,*.properties,*.ttf", )
    filename = fields.Char('File Name', size=256)
    report_id = fields.Many2one('ir.actions.report.xml', 'Report', ondelete='cascade')
    default = fields.Boolean('Default')

    @api.model
    def create(self, vals):
        result = super(report_xml_file, self).create(vals)
        self.env['ir.actions.report.xml'].update([vals['report_id']])
        return result

    @api.model
    def write(self, vals):
        result = super(report_xml_file, self).write(vals)
        for attachment in self:
            self.env['ir.actions.report.xml'].update([attachment.report_id.id])
        return result


# Inherit ir.actions.report.xml and add an action to be able to store .jrxml and .properties
# files attached to the report so they can be used as reports in the application.
class report_xml(models.Model):
    _inherit = 'ir.actions.report.xml'

    jasper_output = fields.Selection(
        [('html', 'HTML'), ('csv', 'CSV'), ('xls', 'XLS'), ('rtf', 'RTF'), ('odt', 'ODT'), ('ods', 'ODS'),
         ('txt', 'Text'), ('pdf', 'PDF')], 'Jasper Output',
        default=lambda self: self.env.context and self.env.context.get('jasper_report') and 'pdf' or False, )
    jasper_file_ids = fields.One2many('ir.actions.report.xml.file', 'report_id', 'Files', help='')
    jasper_model_id = fields.Many2one('ir.model', 'Model', help='')  # We use jas-er_model
    jasper_report = fields.Boolean('Is Jasper Report?')

    @api.model
    def write(self, vals):
        if self.env.context and 'jasper_report' in self.env.context:
            if 'jasper_model_id' in vals:
                vals['model'] = self.env['ir.model'].browse(vals['jasper_model_id']).model
            vals['type'] = 'ir.actions.report.xml'
            vals['report_type'] = 'pdf'
            vals['jasper_report'] = True
        return super(report_xml, self).write(vals)

    @api.model
    def create(self, vals):
        if self.env.context and 'jasper_report' in self.env.context:
            vals['model'] = self.env['ir.model'].browse(vals['jasper_model_id']).model
            vals['type'] = 'ir.actions.report.xml'
            vals['report_type'] = 'pdf'
            vals['jasper_report'] = True
        return super(report_xml, self).create(vals)

    @api.multi
    def update(self):
        pool_values = self.env['ir.values']
        for report in self:
            has_default = False
            # Browse attachments and store .jrxml and .properties into jasper_reports/custom_reports
            # directory. Also add or update ir.values data so they're shown on model views.
            # for attachment in self.pool.get('ir.attachment').browse( cr, uid, attachmentIds ):
            for attachment in report.jasper_file_ids:
                content = attachment.file
                fileName = attachment.filename
                if not fileName or not content:
                    continue
                path = self.save_file(fileName, content)
                if '.jrxml' in fileName:
                    if attachment.default:
                        if has_default:
                            raise UserError(_('There is more than one report marked as default'))
                        has_default = True
                        # Update path into report_rml field.
                        self.write([report.id], {
                            'report_rml': path
                        })
                        valuesId = self.env['ir.values'].search([
                            ('value', '=', 'ir.actions.report.xml,%s' % report.id)])
                        data = {
                            'name': report.name,
                            'model': report.model,
                            'key': 'action',
                            'object': True,
                            'key2': 'client_print_multi',
                            'value': 'ir.actions.report.xml,%s' % report.id
                        }
                        if not valuesId:
                            valuesId = pool_values.create(data)
                        else:
                            pool_values.write(valuesId, data)
                            valuesId = valuesId[0]

            if not has_default:
                raise UserError(_('No report has been marked as default! You need atleast one jrxml report!'))

            # Ensure the report is registered so it can be used immediately
            jasper_report.register_jasper_report(report.report_name, report.model)
        return True

    def save_file(self, name, value):
        path = os.path.abspath(os.path.dirname(__file__))
        path += '/custom_reports/%s' % name
        f = open(path, 'wb+')
        try:
            f.write(base64.decodestring(value))
        finally:
            f.close()
        path = 'jasper_reports/custom_reports/%s' % name
        return path

    def normalize(self, text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        return text

    def unaccent(self, text):
        if isinstance(text, str):
            text = unicode(text, 'utf-8')
        output = text
        for c in xrange(len(src_chars)):
            if c >= len(dst_chars):
                break
            output = output.replace(src_chars[c], dst_chars[c])
        output = unicodedata.normalize('NFKD', output).encode('ASCII', 'ignore')
        return output.strip('_').encode('utf-8')

    def generate_xml(self, modelName, parentNode, document, depth, first_call):
        # First of all add "id" field
        fieldNode = document.createElement('id')
        parentNode.appendChild(fieldNode)
        valueNode = document.createTextNode('1')
        fieldNode.appendChild(valueNode)
        language = self.env.context.get('lang')
        if language == 'en_US':
            language = False
        # Then add all fields in alphabetical order
        print modelName
        model = self.env[modelName]
        print model
        print "***********************"
        fields = model._columns.keys()
        fields += model._inherit_fields.keys()
        # Remove duplicates because model may have fields with the
        # same name as it's parent
        fields = sorted(list(set(fields)))
        for field in fields:
            name = False
            if language:
                # Obtain field string for user's language.
                name = self.env['ir.translation']._get_source(modelName + ',' + field, 'field', language)
            if not name:
                # If there's not description in user's language, use default (english) one.
                if field in model._columns.keys():
                    name = model._columns[field].string
                else:
                    name = model._inherit_fields[field][2].string

            if name:
                name = self.unaccent(name)
            # After unaccent the name might result in an empty string
            if name:
                name = '%s-%s' % (self.unaccent(name), field)
            else:
                name = field
            fieldNode = document.createElement(name)

            parentNode.appendChild(fieldNode)
            if field in self.env[modelName]._columns:
                fieldType = model._columns[field]._type
            else:
                fieldType = model._inherit_fields[field][2]._type
            if fieldType in ('many2one', 'one2many', 'many2many'):
                if depth <= 1:
                    continue
                if field in model._columns:
                    newName = model._columns[field]._obj
                else:
                    newName = model._inherit_fields[field][2]._obj
                self.generate_xml(newName, fieldNode, document, depth - 1, False)
                continue

            value = field
            if fieldType == 'float':
                value = '12345.67'
            elif fieldType == 'integer':
                value = '12345'
            elif fieldType == 'date':
                value = '2009-12-31 00:00:00'
            elif fieldType == 'time':
                value = '12:34:56'
            elif fieldType == 'datetime':
                value = '2009-12-31 12:34:56'

            valueNode = document.createTextNode(value)
            fieldNode.appendChild(valueNode)

        if depth > 1 and modelName != 'Attachments':
            # Create relation with attachments
            fieldNode = document.createElement('%s-Attachments' % self.unaccent(_('Attachments')))
            parentNode.appendChild(fieldNode)
            self.generate_xml('ir.attachment', fieldNode, document, depth - 1, False)

        if first_call:
            # Create relation with user
            fieldNode = document.createElement('%s-User' % self.unaccent(_('User')))
            parentNode.appendChild(fieldNode)
            self.generate_xml('res.users', fieldNode, document, depth - 1, False)

            # Create special entries
            fieldNode = document.createElement('%s-Special' % self.unaccent(_('Special')))
            parentNode.appendChild(fieldNode)

            newNode = document.createElement('copy')
            fieldNode.appendChild(newNode)
            valueNode = document.createTextNode('1')
            newNode.appendChild(valueNode)

            newNode = document.createElement('sequence')
            fieldNode.appendChild(newNode)
            valueNode = document.createTextNode('1')
            newNode.appendChild(valueNode)

            newNode = document.createElement('subsequence')
            fieldNode.appendChild(newNode)
            valueNode = document.createTextNode('1')
            newNode.appendChild(valueNode)

    def create_xml(self, model, depth):
        document = getDOMImplementation().createDocument(None, 'data', None)
        topNode = document.documentElement
        recordNode = document.createElement('record')
        topNode.appendChild(recordNode)
        self.generate_xml(model, recordNode, document, depth, True)
        topNode.toxml()
        return topNode.toxml()
