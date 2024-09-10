{
    'name': 'SSI Event',
    'version': '1.0',
    'category': 'Marketing/Events',
    'summary': 'SSI Events Management',
    'description': """Modify Events Organization Module and other related module""",
    'depends': ['base','event','mail','web','website_event','website_event_track','spreadsheet_dashboard','sale','mass_mailing_event','auth_oauth','portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/inherit_event_event_views.xml',
        'views/inherit_event_stage_views.xml',
        'views/event_track_templates_list_custom.xml',
        'views/inherit_loyalty_program_views.xml',
        'views/ssi_menu.xml',
        'views/inherit_res_partner_views.xml',
        'views/event_templates_page_registration_custom.xml',
        'views/inherit_event_track_views.xml',
        'data/mail_template_data_custom.xml',
        'views/auth_oauth_templates_custom.xml',
        'views/website_template_custom.xml',
        'views/portal_templates_custom.xml',
        'report/event_event_templates_custom.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ssi_event/static/src/css/style.css',
            'ssi_event/static/src/js/main.js'
        ],
    },
    'installable': True,
    'auto_install': False,
}
