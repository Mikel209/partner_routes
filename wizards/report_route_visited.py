# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api, _
from datetime import date, datetime, time, timedelta

import logging

_logger = logging.getLogger(__name__)


class PartnerRouteVisited(models.TransientModel):
    _name = 'partner.route.visited'
    _description = 'Partner Route Visited'

    user_id = fields.Many2one('res.users', 'Selection User')
    date_begin = fields.Date(string='Date begin')
    final_date = fields.Date(string='Final date')

    @api.onchange('user_id')
    def onchange_user_id(self):
        self.user_id = self.env.user.id
        self.date_begin = date.today() - timedelta(weeks=1)
        self.final_date = date.today()

    def _get_domain_partner_route_visited(self):
        domain = []
        if self.user_id.id:
            domain.append(('partner_id.user_id', '=', self.user_id.id))
            logging.info(domain)
        if self.date_begin:
            domain.append(('date', '>=', self.date_begin))
            logging.info(domain)
        if self.final_date:
            domain.append(('date', '<=', self.final_date))
            logging.info(domain)
        logging.info(domain)
        return domain

    def run_wizard_partner_route_visited(self):
        self.ensure_one()
        tree_view_id = self.env.ref('partner_routes.view_partner_route_visited_tree').id
        return {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree',
            'name': _('Partner Route Visited'),
            'res_model': 'route.visited',
            'domain': self._get_domain_partner_route_visited()
        }