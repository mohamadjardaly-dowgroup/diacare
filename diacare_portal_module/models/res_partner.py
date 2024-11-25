
from odoo import api, fields, models, tools, _
from datetime import date
from dateutil.relativedelta import relativedelta

class ResPartner(models.Model):
    """Inherited model for adding two fields to determine
                        whether the partner student or parent"""
    _inherit = 'res.partner'


    is_patient = fields.Boolean(string="Is a Patient",
                               help="Enable if the partner is a patient")

    birthday = fields.Date(string=_('Birth Day'))
    age = fields.Integer(string=_("age"), compute='_compute_age')

    gender_1 = fields.Selection(
        selection=[('male', _('Male')),
                   ('female', _('Female'))])

    nickname = fields.Char(string=_('Nickname'), translate=True, tracking=True)


    @api.depends('birthday')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.birthday:
                age = relativedelta(today, record.birthday).years
                record.age = age
            else:
                record.age = 0
