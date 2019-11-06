from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
import logging

class RouteSell(models.Model):
    _inherit = "sale.order"

    def run_button(self):
        info = self.env["partner.visit"].search(
            [('next_date', '=', date.today()), ('partner_id.user_id.id', '=', self.env.user.id)], order='order',
            limit=1)

        # self.partner_id = info.partner_id

        self.env["route.visited"].create({
            'user_id': self.env.user.id,
            'partner_id': info.partner_id,
            'date': date.today(),
        })

class RouteVisited(models.Model):
    _name = "route.visited"
    _description = "The Route Visited"

    user_id = fields.Many2one('res.users', string='User')
    partner_id = fields.Many2one('res.partner', string='Partner')
    date = fields.Date(string='Day')
