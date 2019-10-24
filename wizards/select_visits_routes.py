# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class PartnerVisitDay(models.TransientModel):
    _name = 'partner.visit.day'
    _description = 'Partner Visit Day'

    user_id = fields.Many2one('res.users')
    partner_id = fields.Many2one('res.partner')
    visit_id = fields.Many2one('partner.visit')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        # logging.info("----------------------------------")
        # logging.info(self.user_id.partner_ids.id)
        for partner in self.user_id.partner_ids:
            # logging.info(partner.name)
            for visit in partner.visit_ids:
                self.create({'user_id': self.user_id, 'partner_id': partner.id, 'visit_id': visit.id})
        #         logging.info("--------")
        #         logging.info(visit.week_day)
        #         logging.info(visit.order)
        #         logging.info(visit.period)
        #         logging.info(visit.next_visit)
        # logging.info("----------------------------------")
