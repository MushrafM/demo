{
    'name': "bike_module",
    'summary': "",
    'description': "",
    'author': "",
    'website': "",
    'category': "",
    'version': "0.1",
    'depends': ['base', 'mail'],
    'data':  [
        'security/ir.model.access.csv',
        'views/bike.xml',
        'views/sequence.xml',
        'data/bike_temp_mail.xml',
        'views/res_partner_inherit_form.xml',
        'views/security.xml',
        'views/rules.xml',

    ],
    'demo': [
        'demo/demo.xml',
    ]
}