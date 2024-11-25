{
    'name': 'Diabetes patient Portal & Online Admission',
    'version': '17.0.1.0.0',
    'description': '',
    'category': 'Industries/Website',
    'author': '',
    'company': '',
    'maintainer': '',
    'depends': ['base', 'website', 'auth_signup', 'website_slides', 'mail','website_sale','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/online_application_menu.xml',
        'views/diabetes_patient_views.xml',
        'views/online_application_template.xml',
        'views/student_portal_template.xml',
        'views/auth_signup_template.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'diacare_portal_module/static/src/scss/education_backend.scss',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
