# -*- coding: utf-8 -*-

{
    "name": "VNPAY Sale Report",
    'version': '1.0',
    'description': """
        Sale Report on POS
    """,
    'author': 'VNPAY TEAM',
    'category': 'Report',
    'website': 'n/a',
    'license': 'AGPL-3',
    'depends': ['sale', 'jasper_reports', 'product', 'point_of_sale'],
    'data': [
        'wizard/vn_sale_report_wizard_view.xml',
        'reports/vn_report_list.xml',
    ],
    "installable": True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
