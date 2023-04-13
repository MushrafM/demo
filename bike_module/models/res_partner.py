from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    messages = fields.Char(string="status")
    other_information = fields.Char(string="Other Messages")
    age = fields.Integer(string="Age")
    car_count = fields.Integer(string='Count', compute='get_car_number')

    def get_car_number(self):
        for rec in self:
            rec.car_count = self.env['bikes.bikes'].search_count([('driver_id', '=', self.id)])

    def get_cars(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bike',
            'view_mode': 'tree',
            'res_model': 'bikes.bikes',
            'domain': [('driver_id', '=', self.id)],
            'context': "{'create':False}"
        }
