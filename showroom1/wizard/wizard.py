from odoo import models, fields


class WizardShowroom(models.TransientModel):
    _name = 'wizard.showroom'
    description = "Wizard Showroom"
    new_price = fields.Integer(string="New Price", default=lambda self: self.env['showroom.car'].browse(
        self.env.context.get('active_id')).price)

    def confirm(self):
        self.env['showroom.car'].browse(self.env.context.get('active_id')).write({
            'price': self.new_price
        })
