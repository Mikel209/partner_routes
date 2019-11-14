from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError

import logging


class Users(models.Model):
    _inherit = "res.users"

    partner_ids = fields.One2many('res.partner', 'user_id')

    @api.multi
    def action_open_visits_routes(self):
        self.ensure_one()
        view = self.env.ref('partner_routes.partner_visit_day')

        return {'name': _('Visit'),
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'partner.visit.day',
                'view_id': view.id,
                'views': [(view.id, 'form')],
                'type': 'ir.actions.act_window',
                'context': {'default_user_id': self.id}}


class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('partner.visit', 'partner_id')


class PartnerVisit(models.Model):
    _name = "partner.visit"
    _description = "Partner Visit"

    partner_id = fields.Many2one('res.partner', string="Partner")
    week_day = fields.Selection(
        [('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'),
         ('0', 'Sunday')], string='Weekday', default="1")
    order = fields.Integer(string="Order", default="1")
    period = fields.Selection([('week', 'week'), ('fortnight', 'fortnight'), ('month', 'month')], string='Period',
                              default="week")
    next_date = fields.Date(string='Next Visit')

    phone = fields.Char(compute='_compute_partner_data', string='Number')
    email = fields.Char(compute='_compute_partner_data', string='Email')

    @api.one
    def _compute_partner_data(self):
        self.phone = self.partner_id.phone
        self.email = self.partner_id.email

    @api.onchange('order')
    def on_change_order(self):
        if self.order > 0:
            return {}
        return {'warning': {'title': _('Error!'), 'message': _('The order number must be greater than 0.')}}

    @api.onchange('week_day')
    def on_change_week_day(self):
        dif = int(self.week_day) - int(date.today().strftime('%w'))

        if dif > 0:
            self.next_date = date.today() + timedelta(days=dif)

        if dif < 0:
            self.next_date = date.today() + timedelta(days=dif + 7)

        if dif == 0:
            self.next_date = date.today() + timedelta(days=7)

    def get_partner_list_to_visit_today(self):
        visited_user_data = self.env["route.visited"].get_visited_partner_current_user_today()

        partner_id_list = []
        for n in visited_user_data:
            partner_id_list.append(n.partner_id.id)

        return self.search([('next_date', '=', date.today()), ('partner_id.user_id.id', '=', self.env.user.id),
                            ('partner_id.id', 'not in', partner_id_list)], order='order', limit=1)
    def get_partner_list_desc_day(self):
        visited_user_data = self.env["route.visited"].get_visited_partner_current_user_today()

        partner_id_list = []
        for n in visited_user_data:
            partner_id_list.append(n.partner_id.id)

        return self.search([('next_date', '=', date.today()), ('partner_id.user_id.id', '=', self.env.user.id),
                            ('partner_id.id', 'not in', partner_id_list)], order='order asc', limit=1)

    # def get_partner_to_visit_today_or_rise(self):
    #     partner_id = self.get_partner_list_to_visit_today()
    #     # if not partner_id:
    #         # self.env['bus.bus'].sendone(
    #         #     (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
    #         #     {'type': 'simple_notification', 'title': _('No more visit'), 'sticky': True, 'warning': True})
    #
    #     return partner_id