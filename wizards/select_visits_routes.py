# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class PartnerVisitDay(models.TransientModel):
    _name = 'partner.visit.day'
    _description = 'Partner Visit Day'

    partner_id = fields.Many2one('res.partner')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        data = []
        self.partner_id = [(6, 0, [])]
        for line in self.user_id.move_line_ids:
            data.append((0, False, self.get_dict_line(line)))
        self.partner_id = data

    def get_dict_line(self, line):
        partner_visit_day = {'partner_id': line.product_id,
                           'week_day': line.move_id.week_day,
                           'order': line.move_id.order,
                           'period': line.move_id.period,
                           'next_visit': line.next_visit}


        return partner_visit_day