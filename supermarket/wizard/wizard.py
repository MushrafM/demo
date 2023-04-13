from odoo import models, fields, api


class SupermarketWizard(models.TransientModel):
    _name = "supermarket.wizard"
    description = "SuperMarket Wizard"
    price_plus = fields.Integer(string="New Price")

    def ads(self):
        self.env['supermarket.store'].browse(self.env.context.get('active_id')).write({
            'price': self.price_plus
        })

