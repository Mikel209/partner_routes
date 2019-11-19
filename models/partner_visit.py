from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta

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

    def _get_next_date_adjust(self, sum_date):
        dif = int(self.week_day) - int(sum_date.strftime('%w'))
        if dif > 0:
            self.next_date = sum_date + timedelta(days=dif)
        elif dif < 0:
            self.next_date = sum_date + timedelta(days=dif + 7)
        elif dif == 0:
            self.next_date = sum_date

    @api.onchange('week_day', 'period')
    def on_change_week_day_or_period(self):
        if self.period == 'week':
            sum_date = date.today() + timedelta(days=7)
            self._get_next_date_adjust(sum_date)

        elif self.period == 'fortnight':
            sum_date = date.today() + timedelta(days=14)
            self._get_next_date_adjust(sum_date)

        elif self.period == 'month':
            sum_date = date.today() + relativedelta(months=+1)
            self._get_next_date_adjust(sum_date)

    @api.onchange('next_date')
    def on_change_next_date(self):
        self.week_day = self.next_date.strftime('%w')

    def get_partner_list_to_visit_today(self):
        visited_user_data = self.env["route.visited"].get_visited_partner_current_user_today()

        partner_id_list = []
        for n in visited_user_data:
            partner_id_list.append(n.partner_id.id)

        return self.search([('next_date', '=', date.today()), ('partner_id.user_id.id', '=', self.env.user.id),
                            ('partner_id.id', 'not in', partner_id_list)], order='order', limit=1)

    def _get_new_next_date_adjust(self, week_day, next_date):
        dif = int(week_day) - int(next_date.strftime('%w'))

        if dif > 0:
            next_date = next_date + timedelta(days=dif)
        if dif < 0:
            next_date = next_date + timedelta(days=dif + 7)
        if dif == 0:
            next_date = next_date
        return next_date

    def calculate_day(self, next_date, period, week_day):

        if period == 'week':
            return self._get_new_next_date_adjust(week_day, next_date + timedelta(days=7))

        if period == 'fortnight':
            return self._get_new_next_date_adjust(week_day, next_date + timedelta(days=14))

        if period == 'month':
            return self._get_new_next_date_adjust(week_day, next_date + relativedelta(months=+1))

    def calculate_next_visit_depend_period(self, partner_id):
        for visit in self.search_read([('next_date', '=', date.today()), ('partner_id.id', '=', partner_id),
                                 ('partner_id.user_id.id', '=', self.env.user.id)], fields=['next_date', 'order',
                                                                                            'week_day', 'period']):
           next_visit = self.calculate_day(visit['next_date'], visit['period'], visit['week_day'])

           if self.search_count(([('next_date', '=', date.today()), ('partner_id.id', '=', partner_id),
                                 ('partner_id.user_id.id', '=', self.env.user.id)])) != 0:

                self.create([{'partner_id': partner_id,
                              'week_day': visit['week_day'],
                              'order': visit['order'],
                              'period':  visit['period'],
                              'next_date': next_visit}])