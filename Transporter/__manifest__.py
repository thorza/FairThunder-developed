{
    'name': 'Fleet Transport Management',
    'version': '0.0.1',
    'category': 'Transport',
    'summary': 'Manage fleet, vehicles, transport rigs, trips, and transport quotes.',
    'depends': ['base', 'web', 'mail'],  # Add 'mail' for email templates and notifications
    'data': [
        'security/ir.model.access.csv',  
        'views/menu_views.xml',
        'views/vehicle_views.xml',
        'views/rig_views.xml',
        'views/trip_views.xml',
        'views/transport_quote_views.xml',
        'views/depot_views.xml',
        'reports/depot_trucks_report.xml',
        'data/transport_quote_model.xml',
        'views/quote_email_templates.xml',  # Load the QWeb template first
        'data/mail_quote_template.xml',     # Then load the email template
    ], 
    'test': [
        'tests/test_transport_quote.py',
    ],
    'assets': {
        'web.assets_backend': [
            '/Transporter/static/src/js/address_autocomplete.js',
            '/Transporter/static/src/img/company_logo.png',  # Include the company logo in assets
        ],
        'web.assets_qweb': [
            '/Transporter/static/src/xml/qweb_templates.xml',  # For additional frontend XML templates if needed
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}

