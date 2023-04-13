from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Bike(models.Model):
    _name = "bikes.bikes"
    name = fields.Char(string=" Bike Name")
    image = fields.Image(string="Image")
    driver_needed = fields.Boolean(default=False, requests=True)
    driver_id = fields.Many2one('res.partner', string='Driver')
    fuel_type = fields.Selection([('petrol', 'Petrol'), ('ev', 'Ev'), ('diesel', 'Diesel')], string='Fuel Type',
                                 default='petrol')
    price = fields.Integer(string="Price")
    month = fields.Integer(string="Month")
    emi = fields.Integer(string="Emi", compute="calculate_emi_price")
    insurance_expiry = fields.Date(string="Insurance Expiry")
    bike_sequence = fields.Char(string="Sequence")
    status = fields.Selection([('new', 'New'), ('used', 'Used'), ('sold', 'Sold')], string='status', default='new')

    def set_bike_to_used(self):
        self.status = "used"

    def set_bike_to_sold(self):
        self.status = "sold"
        template_id = self.env.ref('bike_module.bike_mail_template')

        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True,
                                  email_values={'email_to': 'mushrafoxiom@gmail.com'})
            print('hi')

    def calculate_emi_price(self):
        self.emi = self.price / self.month

    @api.model
    def create(self, vals):
        vals['bike_sequence'] = self.env['ir.sequence'].next_by_code('bike.sequence')
        if vals['name'] == 'abcd':
            vals['name'] = 'bmw'
        if vals['month'] == 0:
            if vals['price'] == 0:
                raise ValidationError('month and price cant be 0')
            raise ValidationError('price must be greater than 0')
        if vals['month'] < 1:
            raise ValidationError('month must be greater than 0')
        if vals['price'] == 0:
            raise ValidationError('price must be greater than 0')
        result = super(Bike, self).create(vals)
        return result

    def check(self):
        if self.month > 12:
            raise ValidationError('month must be less than 12')
        else:
            if self.price > 100000:
                raise ValidationError('price must be less than 100000')
            else:
                raise ValidationError('all values correct')

    def unlink(self):
        for rec in self:
            if rec.name == 'bmw':
                raise ValidationError("Something went wrong")
        return super(Bike, self).unlink()

