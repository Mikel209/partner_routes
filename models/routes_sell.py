from odoo import api, fields, models, _
from datetime import date
import logging


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_outstanding = fields.Boolean(compute='_compute_data')
    button_next_costumer = fields.Boolean('Next Costumer')

    @api.multi
    @api.onchange('button_next_costumer')
    def onchange_button_next_costumer(self, sale_id=0):
        if sale_id != 0:
            self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id, sale_id)

        elif self.partner_id.id:
            self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id, sale_id)
            next_partner_visit = self.env["partner.visit"].get_partner_list_to_visit_today().partner_id.id

            if next_partner_visit:
                self.partner_id = next_partner_visit
            else:
                self.partner_id = self.env.user.id

        if not self.partner_id.id:
            self.partner_id = self.env["partner.visit"].get_partner_list_to_visit_today().partner_id.id
            # self.payment_term_id = 1

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.onchange_button_next_costumer(res.id)
        return res

    @api.depends('partner_id')
    def _compute_data(self):
        if self.partner_id.id == self.env.user.id:
            logging.info("+++++++++++FINISH+++++++++++")
            self.has_outstanding = True


class RouteVisited(models.Model):
    _name = "route.visited"
    _description = "The Route Visited"

    user_id = fields.Many2one('res.users', 'User ID')
    partner_id = fields.Many2one('res.partner', 'Partner ID')
    date = fields.Date(string='Day')
    sale_order_id = fields.Many2one('sale.order', 'Reference')

    hour = fields.Char(compute='_compute_route_visited', string='Hour')

    # sale_order_id_y_or_n = fields.Char(compute='_compute_route_visited', string='Did it visit?')

    @api.one
    def _compute_route_visited(self):
        self.hour = self.create_date.strftime("%H:%M:%S")
        if self.sale_order_id:
            self.sale_order_id_y_or_n = 'Visitado'
        else:
            self.sale_order_id_y_or_n = 'No Visitado'

    def get_visited_partner_current_user_today(self):
        return self.search([('date', '=', date.today()), ('user_id', '=', self.env.user.id)])

    def get_visited_partner_testing(self, partner_id):
        return self.search(
            [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)])

    def is_record_creation_of_the_costumer_visited(self, partner_id, sale_id):
        if not self.search(
                [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)]):
            self.create([{'user_id': self.env.user.id, 'partner_id': partner_id, 'date': date.today(),
                          'sale_order_id': sale_id}])

            self.env["partner.visit"].calculate_next_visit_depend_period(partner_id)
