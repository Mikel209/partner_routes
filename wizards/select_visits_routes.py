# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class PartnerVisitDay(models.TransientModel):
    _name = 'partner.visit.day'
    _description = 'Partner Visit Day'

    user_id = fields.Many2one('res.users', 'Selection User')
    date_visit = fields.Date(string='Next Visit')

    # @api.onchange('user_id')
    # def _onchange_user_id(self):
    #     logging.info("----------------------------------")
    #     logging.info(self.user_id)
    #     for partner in self.user_id.partner_ids:
    #         # logging.info(partner.name)
    #         for visit in partner.visit_ids:
    #             logging.info("----------------------------------")
    #             logging.info(partner.name)
    #             self.create({'user_id': self.user_id.id, 'partner_name':
    #             partner.name, 'visit_next_day': visit.next_visit})
    #
    #              logging.info("--------")
    #              logging.info(visit.week_day)
    #              logging.info(visit.order)
    #              logging.info(visit.period)
    #              logging.info(visit.next_visit)

    def _get_domain(self):
        domain = []
        if self.user_id.id:
            domain.append(('user_id', '=', self.user_id.id))
        return domain

    def run_wizard(self):
        self.ensure_one()
        tree_view_id = self.env.ref('partner_routes.view_partner_visit_tree').id
        return {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree',
            'name': _('Partner Visit Day'),
            'res_model': 'partner.visit',
            'domain': self._get_domain()
        }