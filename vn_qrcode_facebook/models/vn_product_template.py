# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging
import os
import re
from vn_qrcode import vn_qrcode
from odoo import tools, _
from odoo.tools import config
import hashlib

_logger = logging.getLogger(__name__)
qrcode = vn_qrcode()


class vn_product_template(models.Model):
    _inherit = "product.template"

    @api.model
    def _filestore(self):
        return config.filestore(self._cr.dbname)

    @api.model
    def _full_path(self, path):
        # sanitize path
        path = re.sub('[.]', '', path)
        path = path.strip('/\\')
        return os.path.join(self._filestore(), path)

    @api.model
    def _get_data_qrcode(self):
        # attributes for create qrcode
        serviceCode = "000003"
        masterMerCode = "VNPAY"
        secretKey = "vnpay@VnPayment"
        appId = "VNPAYMENT"
        merchantType = ""
        payType = "02"
        txnId = ""
        tipAndFee = ""
        expDate = ""
        ccy = self.env.user.company_id.currency_id.name
        merchantName = self.env.user.company_id.name
        countryCode = self.env.user.company_id.country_id.code
        merchantCode = self.env.user.company_id.vat
        terminalId = self.env['ir.config_parameter'].get_param("facebook")
        amount = self.list_price
        if (self.barcode):
            productId = self.barcode
        else:
            productId = ""
        if (self.description_sale):
            desc = self.description_sale
        else:
            desc = ""

        # create data for hash md5
        data_hash = appId + "|" + merchantName + "|" + serviceCode + "|" + countryCode + "|" \
                    + masterMerCode + "|" + merchantType + "|" + merchantCode + "|" \
                    + terminalId + "|" + payType + "|" + productId + "|" + txnId + "|" \
                    + str(amount) + "|" + tipAndFee + "|" + ccy + "|" + expDate + "|" + secretKey
        # execute hash md5
        hash_md5 = hashlib.md5()
        hash_md5.update(data_hash)
        checksum = hash_md5.hexdigest()
        _logger.info("checksum: " + checksum)
        # string data for qrcode
        content_qrcode = data_hash + "|" + checksum

        return content_qrcode

    @api.model
    def _get_watermark_image(self, image_path, content_qrcode):
        # create watermark for image
        image = qrcode.watermark_image_with_qrcode(image_path, content_qrcode)

        return image

    @api.model
    def _get_path_image(self, product_tmpl_id):
        sql_query = """SELECT store_fname
                    FROM ir_attachment
                    WHERE res_id = %s AND res_field = 'image' AND res_model = 'product.template'
                    """
        self.env.cr.execute(sql_query, (product_tmpl_id,))
        store_fname = self.env.cr.fetchone()
        if store_fname is not None:
            store_fname = store_fname[0] or False
        full_path = self._full_path(store_fname)
        return full_path

    @api.multi
    def open_social_network_form(self):
        """Open a social network form that share product on social network( facebook, zalo,...)"""
        image_path = self._get_path_image(self.id)
        content_qrcode = self._get_data_qrcode()
        ctx = {
            'product_name': self.name,
            'image': self._get_watermark_image(image_path, content_qrcode),
            'list_price': self.list_price,
            'description_sale': self.description_sale,
        }

        return {
            'name': _('Share Social Network'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'vn.social.network.wizard',
            'view_id': self.env.ref('vn_qrcode_facebook.vn_social_network_product_form_view').id,
            'target': 'new',
            'context': ctx,
        }
