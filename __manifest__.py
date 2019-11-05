# Copyright 2018 QubiQ (http://www.qubiq.es)
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Routes',
    'version': '1.0',
    'category': 'Partner Routes',
    'author': 'Watchdog',
    'website': 'https://www.Watchdog.es',
    'license': 'AGPL-3',
    'summary': 'Partner Routes',
    'depends': [
        'base', 'sale',
    ],
    'data': [
        'wizards/wizards_select_visits_routes.xml',
        # 'views/view_routes_sell.xml',
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
