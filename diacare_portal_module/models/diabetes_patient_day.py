from odoo import models, fields


class DiabetesPatientDay(models.Model):
    _name = 'diabetes.patient.day'
    _description = 'Daily Diabetes Patient Data'

    patient_id = fields.Many2one(
        'diabetes.patient', string='Patient', required=True, ondelete='cascade'
    )
    day = fields.Selection([
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ], string='Day', required=True)
    date = fields.Date(string='Date', required=True)
    dose_morning = fields.Float(string='Morning Dose (Units)')
    dose_afternoon = fields.Float(string='Afternoon Dose (Units)')
    dose_night = fields.Float(string='Night Dose (Units)')
    pre_breakfast = fields.Float(string='Pre-Breakfast (mg/dL)')
    post_breakfast = fields.Float(string='Post-Breakfast (mg/dL)')
    pre_lunch = fields.Float(string='Pre-Lunch (mg/dL)')
    post_lunch = fields.Float(string='Post-Lunch (mg/dL)')
    pre_dinner = fields.Float(string='Pre-Dinner (mg/dL)')
    post_dinner = fields.Float(string='Post-Dinner (mg/dL)')
    bedtime = fields.Float(string='Bedtime Glucose (mg/dL)')
    early_morning = fields.Float(string='4-3 AM Glucose (mg/dL)')
