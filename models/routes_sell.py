from odoo import api, fields, models, _
from datetime import date
import logging


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_outstanding = fields.Boolean(compute='_compute_data')
    button_next_costumer = fields.Boolean('Next Costumer')

    @api.model
    def _get_default_partner(self):
        default_partner_to_visit = self.env["partner.visit"].get_partner_list_to_visit_today()

        return default_partner_to_visit.partner_id.id

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True,
                                 change_default=True, index=True, track_visibility='always', track_sequence=1,
                                 help="You can find a customer by its Name, TIN, Email or Internal Reference.",
                                 default=_get_default_partner)

    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #     res.button_next_costumer()
    #     # logging.info("---------------dewsde create---------------------------------")
    #     return res

    @api.multi
    @api.onchange('button_next_costumer')
    def onchange_button_next_costumer(self):
        if self.partner_id.id != self.env.user.id:
            self.env["route.visited"].is_record_creation_of_the_costumer_visited(self.partner_id.id)

            next_partner_visit = self.env["partner.visit"].get_partner_list_to_visit_today()

            if next_partner_visit:
                self.partner_id = next_partner_visit.partner_id.id
            else:
                self.partner_id = self.env.user.id
        # logging.info("---------------------desde run button--------------------")

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
    # id_boolean = fields.One2many('sale.order', 'id')

    def get_visited_partner_current_user_today(self):
        return self.search([('date', '=', date.today()), ('user_id', '=', self.env.user.id)])

    def get_visited_partner_testing(self, partner_id):
        return self.search(
            [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)])

    def is_record_creation_of_the_costumer_visited(self, partner_id):
        if not self.search(
                [('date', '=', date.today()), ('user_id', '=', self.env.user.id), ('partner_id', '=', partner_id)]):
            self.create([{'user_id': self.env.user.id, 'partner_id': partner_id, 'date': date.today()}])

            self.env["partner.visit"].calculate_next_visit_depend_period(partner_id)