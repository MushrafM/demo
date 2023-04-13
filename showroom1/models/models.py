from odoo import models, fields


class Showroom(models.Model):
    _name = "showroom.car"
    name = fields.Char(string='Bike Name')
    fuel_type = fields.Selection([('petrol', 'Petrol'), ('ev', 'EV'), ('diesel', 'Diesel')], string='Fuel Type',
                                 default="petrol")
    model_brand = fields.Char(string="Model Brand")
    year = fields.Integer(string="Year")
    price = fields.Integer(string="Price")




