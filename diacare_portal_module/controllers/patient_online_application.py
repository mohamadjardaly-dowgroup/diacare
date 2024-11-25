from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class DiabetesPatientForm(http.Controller):
    @http.route('/diabetes/patient/form', type='http', auth='user', website=True)
    def diabetes_patient_form(self, **kwargs):
        today = datetime.today()
        current_weekday = today.weekday()  # This gives the current day of the week (0=Monday, 1=Tuesday, ..., 6=Sunday)

        # Days of the week in order starting from Sunday
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        days = []
        for i, day in enumerate(days_of_week):
            # Calculate the offset for each day of the week
            day_offset = (i - current_weekday - 1) % 7
            day_date = today + timedelta(days=day_offset)

            # Format the date and store in the list
            days.append({
                'index': i,
                'day': day,
                'date': day_date.strftime('%Y-%m-%d')
            })

        # Fetch the current logged-in user's details
        user = request.env.user
        default_name = user.name
        default_contact = user.partner_id.phone or ""

        return request.render('diacare_portal_module.diabetes_patient_form_template', {
            'days': days,
            'default_name': default_name,
            'default_contact': default_contact,
        })

    @http.route('/diabetes/patient/submit', type='http', auth='public', website=True, csrf=True)
    def diabetes_patient_submit(self, **kwargs):
        print("Submitted Data:", kwargs)  # Debugging

        # Create patient record
        patient = request.env['diabetes.patient'].sudo().create({
            'name': kwargs.get('name'),
            'age': kwargs.get('age'),
            'gender': kwargs.get('gender'),
            'contact': kwargs.get('contact'),
            'height': kwargs.get('height'),
            'weight': kwargs.get('weight'),
        })

        # Manually process the 'days' data
        days_data = []
        for i in range(7):  # Assuming there are 7 days in the week
            day_name = kwargs.get(f'days[{i}][day]')
            day_date = kwargs.get(f'days[{i}][date]')
            dose_morning = kwargs.get(f'days[{i}][dose_morning]')
            dose_afternoon = kwargs.get(f'days[{i}][dose_afternoon]')
            dose_night = kwargs.get(f'days[{i}][dose_night]')
            pre_breakfast = kwargs.get(f'days[{i}][pre_breakfast]')
            post_breakfast = kwargs.get(f'days[{i}][post_breakfast]')
            pre_lunch = kwargs.get(f'days[{i}][pre_lunch]')
            post_lunch = kwargs.get(f'days[{i}][post_lunch]')
            pre_dinner = kwargs.get(f'days[{i}][pre_dinner]')
            post_dinner = kwargs.get(f'days[{i}][post_dinner]')

            if day_name:
                day_name = day_name.lower()  # Convert day name to lowercase

            # Check if any required data is missing
            if day_name and day_date:
                # Add the data for this day into the list
                days_data.append({
                    'day': day_name,
                    'date': day_date,
                    'dose_morning': dose_morning,
                    'dose_afternoon': dose_afternoon,
                    'dose_night': dose_night,
                    'pre_breakfast': pre_breakfast,
                    'post_breakfast': post_breakfast,
                    'pre_lunch': pre_lunch,
                    'post_lunch': post_lunch,
                    'pre_dinner': pre_dinner,
                    'post_dinner': post_dinner,
                })

        print("Processed Days Data:", days_data)

        # Process the weekly data and create entries
        for day_data in days_data:
            day_name = day_data['day']
            day_date = day_data['date']
            dose_morning = day_data['dose_morning']
            dose_afternoon = day_data['dose_afternoon']
            dose_night = day_data['dose_night']
            pre_breakfast = day_data['pre_breakfast']
            post_breakfast = day_data['post_breakfast']
            pre_lunch = day_data['pre_lunch']
            post_lunch = day_data['post_lunch']
            pre_dinner = day_data['pre_dinner']
            post_dinner = day_data['post_dinner']

            print(
                f"Processing {day_name} ({day_date}) - Morning: {dose_morning}, Afternoon: {dose_afternoon}, Night: {dose_night}, "
                f"Pre-breakfast: {pre_breakfast}, Post-breakfast: {post_breakfast}, Pre-lunch: {pre_lunch}, Post-lunch: {post_lunch}, "
                f"Pre-dinner: {pre_dinner}, Post-dinner: {post_dinner}"
            )

            # Create daily entry for the patient
            request.env['diabetes.patient.day'].sudo().create({
                'patient_id': patient.id,
                'day': day_name,  # This will now always be in lowercase
                'date': day_date,
                'dose_morning': dose_morning,
                'dose_afternoon': dose_afternoon,
                'dose_night': dose_night,
                'pre_breakfast': pre_breakfast,
                'post_breakfast': post_breakfast,
                'pre_lunch': pre_lunch,
                'post_lunch': post_lunch,
                'pre_dinner': pre_dinner,
                'post_dinner': post_dinner,
            })

        return request.render('diacare_portal_module.diabetes_patient_success_template')


