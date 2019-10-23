from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
import logging


class Users(models.Model):
    _inherit = "res.users"

    partner_ids = fields.One2many('res.partner', 'user_id')

    @api.multi
    def action_open_visits_routes(self):
        # logging.info("@"*80)
        # for visit in self.partner_ids.visit_ids:
        #     logging.info(visit.next_visit)

        # logging.info(self.partner_ids)
        # for partner in self.partner_ids:
        #     logging.info(partner.name)
        #     for visit in partner.visit_ids:
        #         logging.info(visit.next_visit)

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

    # partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
    #                              string='Related Partner', help='Partner-related data of the user')


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
    next_visit = fields.Date(string='Next Visit')

    @api.onchange('order')
    def on_change_order(self):
        if self.order > 0:
            return {}
        return {'warning': {'title': _('Error!'), 'message': _('The order number must be greater than 0.')}}

    # @api.onchange('week_day', 'period')
    # def on_change_week_day(self):
    #
    #     mesess = date.today() + timedelta(days=self.days_to_add())
    #
    #     logging.info("Meses")
    #     logging.info(mesess)
    #
    #     dif = int(self.week_day) - int(mesess.strftime('%w'))
    #
    #     logging.info("Diferencia")
    #     logging.info(dif)
    #     logging.info("wee_day")
    #     logging.info(self.week_day)
    #
    #     if dif > 0:
    #         logging.info("NextVisit>")
    #         logging.info(self.next_visit)
    #         self.next_visit = mesess + timedelta(days=dif)
    #
    #     if dif < 0:
    #         logging.info("NextVisit<")
    #         logging.info(self.next_visit)
    #         self.next_visit = mesess + timedelta(days=dif + 7)
    #
    #     if dif == 0:
    #         logging.info("NextVisit")
    #         logging.info(self.next_visioooooot)
    #         self.next_visit = mesess + timedelta(days=7)
    #
    # def days_to_add(self):
    #     if self.period == "week":
    #         return 7
    #     if self.period == "fortnight":
    #         return 14
    #     if self.period == "month":
    #         return calendar.monthrange(int(datetime.now().strftime('%Y')), int(datetime.now().strftime('%m')))[1]

    @api.onchange('week_day')
    def on_change_week_day(self):
        dif = int(self.week_day) - int(date.today().strftime('%w'))

        if dif > 0:
            self.next_visit = date.today() + timedelta(days=dif)

        if dif < 0:
            self.next_visit = date.today() + timedelta(days=dif + 7)

        if dif == 0:
            self.next_visit = date.today() + timedelta(days=7)