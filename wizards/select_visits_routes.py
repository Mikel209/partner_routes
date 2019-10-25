# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
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
