# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
import hashlib

_logger = logging.getLogger(__name__)


class vn_social_network(models.TransientModel):
    _name = "vn.social.network.wizard"
    _description = "Social Network"

    # attribute fields
    name = fields.Char('Name', index=True, required=True, translate=True, readonly=True,
                       default=lambda self: self.env.context.get('product_name'))
    list_price = fields.Float('Sale Price', readonly=True, default=lambda self: self.env.context.get('list_price'))
    image = fields.Binary(string="Big-sized image", readonly=True,
                          default=lambda self: self.env.context.get('image'))
    description_sale = fields.Text('Sale Description', translate=True, readonly=True,
                                   default=lambda self: self.env.context.get('description_sale'))
    line_ids = fields.One2many('vn.social.network.line.wizard', 'wizard_id', string='Lines')

    @api.multi
    def _get_data_qrcode(self, line):
        # attributes for create qrcode
        serviceCode = "000003"
        masterMerCode = "VNPAY"
        secretKey = "vnpay @ VnPayment"
        appId = "VNPAYMENT"
        merchantType = ""
        payType = "02"
        txnId = ""
        tipAndFee = ""
        expDate = ""
        ccy = line.env.user.company_id.currency_id.name
        merchantName = line.env.user.company_id.name
        countryCode = line.env.user.company_id.country_id.code
        merchantCode = line.env.user.company_id.vat
        terminalId = line.env['ir.config_parameter'].get_param("facebook")
        amount = line.list_price
        if (line.barcode):
            productId = line.barcode
        else:
            productId = ""
        if (line.description_sale):
            desc = line.description_sale
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
    def default_get(self, fields):
        res = super(vn_social_network, self).default_get(fields)
        context = self._context or {}
        product_tmp_obj = self.env['product.template']
        product_obj = self.env['product.product']
        if (context['active_model'] == "product.product"):
            lines = product_obj.browse(context.get('active_ids', []))
        else:
            lines = product_tmp_obj.browse(context.get('active_ids', []))
        wizard_lines = []
        for line in lines:
            if (context['active_model'] == "product.product"):
                line = product_tmp_obj.browse(line.product_tmpl_id).id
            image_path = product_tmp_obj._get_path_image(line.id)
            content_qrcode = self._get_data_qrcode(line)
            wizard_lines.append(
                self.env['vn.social.network.line.wizard'].create({
                    'product_tmp_id': line.id,
                    'prod_name': line.name,
                    'prod_list_price': line.list_price,
                    'prod_image': product_tmp_obj._get_watermark_image(image_path, content_qrcode),
                    'prod_description': line.description_sale
                })
            )
        res.update({'line_ids': [(line.id) for line in wizard_lines]})

        return res


class vn_social_network_line(models.TransientModel):
    _name = "vn.social.network.line.wizard"
    _description = "Social Network Lines"

    product_tmp_id = fields.Many2one('product.template', string='Product')
    wizard_id = fields.Many2one('vn.social.network.wizard', 'Wizard')
    prod_name = fields.Char('product_tmp_id.name')
    prod_list_price = fields.Float('product_tmp.id.list_price')
    prod_image = fields.Binary('product_tmp.id.image')
    prod_description = fields.Text('product_tmp.id.description')
