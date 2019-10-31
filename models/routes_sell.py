from odoo import models, fields, api, _
import logging

class RouteSell(models.Model):
    _name = "route.sell"
    _description = "Routes of Sell"

    user_id = fields.Many2one('res.users')
    partner_id = fields.Many2one('partner.visit')
    date = fields.Date(string='Day')

    def run_button(self):
        logging.info("*"*90)
        logging.info(self.partner_id)