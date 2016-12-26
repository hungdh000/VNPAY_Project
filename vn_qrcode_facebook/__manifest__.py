# -*- coding: utf-8 -*-
{
    'name': 'QRCode and Share Facebook',
    'version': '1.0',
    'author': 'VNPAY TEAM',
    'summary': 'Create QRCode and Share Facebook',
    'sequence': 30,
    'description': """
     Create QRCode and Share Facebook in product
    """,
    'depends': ['product', 'purchase', 'sale', 'point_of_sale',
                'stock', 'account_accountant', 'web_tree_image',],
    'data': [
        'views/vn_product_views.xml',
        'views/vn_share_social_network_views.xml',
        'views/vn_facebook_share_template.xml',
        'views/vn_terminal_view.xml',
        'data/vn_qrcode_facebook_data.xml',
    ],
    # 'js': ['static/src/js/vn_facebook_share.js',],
    #        'static/src/js/vn_facebook_share_multi_product.js'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}
