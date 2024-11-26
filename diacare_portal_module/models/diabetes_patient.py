from odoo import api, fields, models
from datetime import datetime, timedelta


class DiabetesPatient(models.Model):
    _name = 'diabetes.patient'
    _description = 'Diabetes Patient Management'

    name = fields.Char(string='Patient Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    contact = fields.Char(string='Contact Number')

    # New fields
    height = fields.Float(string='Height (cm)')
    weight = fields.Float(string='Weight (kg)')
    insulin_type = fields.Selection([
        ('rapid', 'Rapid-Acting'),
        ('short', 'Short-Acting'),
        ('intermediate', 'Intermediate-Acting'),
        ('long', 'Long-Acting'),
        ('mixed', 'Pre-Mixed'),
    ], string='Type of Insulin')

    # Calculated fields
    rate_7_days = fields.Float(string='Rate per 7 Days', compute='_compute_rates', store=True)
    rate_14_days = fields.Float(string='Rate per 14 Days', compute='_compute_rates', store=True)
    cumulative_rate = fields.Float(string='Cumulative Rate', compute='_compute_rates', store=True)

    # Daily entries (One2many relationship)
    daily_entries = fields.One2many(
        'diabetes.patient.day', 'patient_id', string='Daily Entries'
    )

    @api.depends('daily_entries.dose_morning', 'daily_entries.dose_afternoon', 'daily_entries.dose_night')
    def _compute_rates(self):
        for patient in self:
            # Get today's date
            today = datetime.today().date()

            # Initialize sums
            total_7_days = 0.0
            total_14_days = 0.0
            cumulative_total = 0.0

            # Loop through daily entries
            for entry in patient.daily_entries:
                entry_date = fields.Date.from_string(entry.date)
                total_dose = (entry.dose_morning or 0.0) + (entry.dose_afternoon or 0.0) + (entry.dose_night or 0.0)

                # Check date range and sum doses
                if (today - entry_date).days <= 7:
                    total_7_days += total_dose
                if (today - entry_date).days <= 14:
                    total_14_days += total_dose

                # Sum all doses for cumulative total
                cumulative_total += total_dose

            # Assign calculated values
            patient.rate_7_days = total_7_days
            patient.rate_14_days = total_14_days
            patient.cumulative_rate = cumulative_total
