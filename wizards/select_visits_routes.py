# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class SelectVisitsRoutes(models.TransientModel):
    _name = 'select.visits.routes'
    _description = 'Select Visits Routes Wizard'

    user_ids = fields.One2many('res.users', 'partner_visit')
    visits_routes_ids = fields.Many2many('select.visits.routes.line')


class SelectVisitsRoutesLine(models.TransientModel):
    _name = 'select.visits.routes.line'
    _description = 'Select Visits Routes Line Wizard'

    # selected = fields.Boolean(string='Selected', default=True, help='Indicate this line is coming to change')
    # product_id = fields.Many2one('product.product', string='Product')
    # previous_purchase_date = fields.Datetime('Previous Purchase Date', required=False)
    # previous_purchase_price = fields.Float('Previous Purchase Price', digits=dp.get_precision('Product Price'))
    # previous_cost_price = fields.Float('Previous Cost', digits=dp.get_precision('Product Price'))
    # current_cost_price = fields.Float('Current Cost', digits=dp.get_precision('Product Price'))
    # purchase_price = fields.Float('Purchase Price', digits=dp.get_precision('Product Price'))
    # cost_price = fields.Float('Cost Price', digits=dp.get_precision('Product Price'))
    # standard_price = fields.Float('Standard Price', digits=dp.get_precision('Product Price'))

