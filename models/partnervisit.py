from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    visit_ids = fields.One2many('partner_visit', 'partner_id')


class PartnerVisit(models.Model):
    _name = "partner_visit"
    _description = "Partner Visit"

    partner_id = fields.Many2one('res.partner', string="Partner")
    week_day = fields.Selection([('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday'), ('1', 'Sunday')], string='Weekday')
    order = fields.Integer(string="Order")
    period = fields.Selection([('week', 'week'), ('fortnight', 'fortnight'), ('month', 'month')], string='Period')
    next_visit = fields.Datetime(string='Next Visit')

