# -*- coding: utf-8 -*-

{
    "name": "Jasper Report Example",
    'version': '1.0',
    'description': """
        Report Sales Order
    """,
    'author': 'VNPAY TEAM',
    'category': 'VNPAY Team',
    'website': 'n/a',
    'license': 'AGPL-3',
    'depends': ['sale', 'jasper_reports', 'product'],
    'data': [
        'wizard/vn_jasper_report_wizard_view.xml',
        'reports/jasper_report_list.xml',
    ],
    "installable": True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
