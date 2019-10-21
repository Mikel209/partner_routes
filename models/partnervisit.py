from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
import calendar
import logging


class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('partner_visit', 'partner_id')


class PartnerVisit(models.Model):
    _name = "partner_visit"
    _description = "Partner Visit"

    partner_id = fields.Many2one('res.partner', string="Partner")
    week_day = fields.Selection(
        [('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'),
         ('0', 'Sunday')], string='Weekday', default="1")
    order = fields.Integer(string="Order", default="1")
    period = fields.Selection([('week', 'week'), ('fortnight', 'fortnight'), ('month', 'month')], string='Period',
                              default="week")
    next_visit = fields.Date(string='Next Visit')

    @api.onchange('order')
    def on_change_order(self):
        if self.order > 0:
            return {}
        return {'warning': {'title': _('Error!'), 'message': _('The order number must be greater than 0.')}}


    # @api.onchange('week_day', 'period')
    # def on_change_week_day(self):
    #
    #     dif = int(self.week_day) - int(datetime.now().strftime('%w'))
    #     if dif > 0:
    #         self.next_visit = date.today() + timedelta(days=dif - 7 + self.days_to_add())
    #     if dif < 0:
    #         self.next_visit = date.today() + timedelta(days=dif + self.days_to_add())
    #
    #     self.next_visit = date.today() + timedelta(days=self.days_to_add())
    #
    # def days_to_add(self):
    #     if self.period == "week":
    #         return 7
    #     if self.period == "fortnight":
    #         return 14
    #     if self.period == "month":
    #         return calendar.monthrange(int(datetime.now().strftime('%Y')), int(datetime.now().strftime('%m')))[1]

    @api.onchange('week_day', 'period')
    def on_change_week_day(self):

        mesess = date.today() + timedelta(days=self.days_to_add())
        dif = int(self.week_day) - int(mesess.strftime('%w'))
        if dif > 0:
            self.next_visit = mesess + timedelta(days=dif)
        if dif < 0:
            self.next_visit = mesess + timedelta(days=dif + self.days_to_add())

        self.next_visit = mesess + timedelta(days=self.days_to_add())

    def days_to_add(self):
        if self.period == "week":
            return 7
        if self.period == "fortnight":
            return 14
        if self.period == "month":
            return calendar.monthrange(int(datetime.now().strftime('%Y')), int(datetime.now().strftime('%m')))[1]