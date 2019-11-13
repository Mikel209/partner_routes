from xxlimited import Null

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
import logging


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _get_default_partner(self):
        default_partner_to_visit = self.env["partner.visit"].get_partner_list_to_visit_today()

        return default_partner_to_visit.partner_id.id

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True,
                                 change_default=True, index=True, track_visibility='always', track_sequence=1,
                                 help="You can find a customer by its Name, TIN, Email or Internal Reference.",
                                 default=_get_default_partner)

    def run_button(self):
        logging.info("self.partner_id.id")
        logging.info(self.partner_id.id)

        self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id)
        last_partner_visit = self.env["partner.visit"].get_last_partner_list().partner_id.id
        next_partner_visit = self.env["partner.visit"].get_partner_list_to_visit_today().partner_id.id

        logging.info("next_partner_visit")
        logging.info(next_partner_visit)

        logging.info("last_partner_visit")
        logging.info(last_partner_visit)

        if last_partner_visit != self.partner_id.id:
            self.partner_id = next_partner_visit
        else:
            self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id)
            self.partner_id = self.partner_id.id

        # next_partner_visit = self.env["partner.visit"].get_partner_list_to_visit_today()
        # if next_partner_visit.partner_id.id == self.env["partner.visit"].get_last_partner_list().partner_id.id:
        #     self.partner_id = next_partner_visit.partner_id.id
        #     self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id)
        #     raise UserError(_("No more visits"))
        # elif next_partner_visit:
        #     self.partner_id = next_partner_visit.partner_id.id


class RouteVisited(models.Model):
    _name = "route.visited"
    _description = "The Route Visited"

    user_id = fields.Many2one('res.users', 'User ID')
    partner_id = fields.Many2one('res.partner', 'Partner ID')
    date = fields.Date(string='Day')

    def get_visited_partner_current_user_today(self):
        return self.search([('date', '=', date.today()), ('user_id', '=', self.env.user.id)])

    def get_visited_partner_testing(self, partner_id):
        return self.search(
            [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)])

    def is_record_creation_of_the_costumer_visited(self, partner_id):
    #     if self.search(
    #             [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)]):
        # logging.info("existeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        # logging.info(partner_id)

        self.create({'user_id': self.env.user.id, 'partner_id': partner_id, 'date': date.today()})
        # logging.info("no existeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        # logging.info(partner_id)
