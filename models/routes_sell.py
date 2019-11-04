from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
import logging


# class RouteSell(models.Model):
#     _name = "route.sell"
#     _description = "Routes of Sell"
#
#     user_id = fields.Many2one('res.users')
#     partner_id = fields.Many2one('partner.visit')
#     date = fields.Date(string='Day')
#
#     def run_button(self):
#         logging.info("*"*90)
#         logging.info("Hola")
#         # logging.info(self.partner_id)

class RouteSell(models.Model):
    _inherit = "sale.order"

    def run_button(self):
        info = self.env["partner.visit"].search(
            [('next_date', '=', date.today()), ('user_id', '=', self.env.user.id)], order='order', limit=1)

        for r in info:
            logging.info(r)

        logging.info(info.partner_id)

        self.partner_id = info.partner_id

        # read_group(domain, fields, groupby, offset=0, limit=1, orderby=False, lazy=True)
        # project_so_1_stat = self.env['project.profitability.report'].read_group([('project_id', 'in', project_so_1.ids)], ['project_id', 'amount_untaxed_to_invoice', 'amount_untaxed_invoiced', 'timesheet_unit_amount', 'timesheet_cost', 'expense_cost', 'expense_amount_untaxed_to_invoice', 'expense_amount_untaxed_invoiced'], ['project_id'])[0]

        # for visit in self.env["partner.visit"].search([['next_date', '=', date.today()]]):
        #     logging.info(visit)
