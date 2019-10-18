from odoo import models, fields, api, _
from  datetime import date, datetime, time, timedelta
import logging

class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('partner_visit', 'partner_id')


class PartnerVisit(models.Model):
    _name = "partner_visit"
    _description = "Partner Visit"

    partner_id = fields.Many2one('res.partner', string="Partner")
    week_day = fields.Selection([('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], string='Weekday', default="1" )
    order = fields.Integer(string="Order", default="1")
    period = fields.Selection([('week', 'week'), ('fortnight', 'fortnight'), ('month', 'month')], string='Period', default="week" )
    next_visit = fields.Date(string='Next Visit', default="on_change_week_day(week_day)")
#7-dia+objetivo
    @api.onchange('order')
    def on_change_order(self):
        logging.getLogger(__name__).info("*"*80)
        logging.getLogger(__name__).info(self.order)
        if self.order > 0:
            return {}
        return {'warning': { 'title': _('Error!'), 'message': _('The order number must be greater than 0.')}}

    @api.onchange('week_day')
    def on_change_week_day(self):
        now = datetime.now()
        day = now.day
        result = 7 - self.week_day + 1:
            return result + day