from odoo import api, fields, models
from datetime import date
import logging


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def get_default(self, fields):
        logging.info('-----------------------Hola------------------------')
        result = super(SaleOrder, self).get_default(fields)
        result['partner_id'] = self.env["partner.visit"].get_partner_list_to_visit_today()
        return result


    def run_button(self):
        next_partner_to_visit = self.env["partner.visit"].get_partner_list_to_visit_today()

        self.partner_id = next_partner_to_visit.partner_id

        self.env["route.visited"].create({
            'user_id': self.env.user.id,
            'partner_id': next_partner_to_visit.partner_id.id,
            'date': date.today(),
        })


class RouteVisited(models.Model):
    _name = "route.visited"
    _description = "The Route Visited"

    user_id = fields.Many2one('res.users', 'User ID')
    partner_id = fields.Many2one('res.partner', 'Partner ID')
    date = fields.Date(string='Day')

    def get_visited_partner_current_user_today(self):

        return self.search([('date', '=', date.today()), ('user_id', '=', self.env.user.id)])
