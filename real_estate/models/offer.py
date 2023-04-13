from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _order = "new_price desc"
    new_price = fields.Integer(string="Price")
    partner = fields.Many2one('res.partner', string="Partner", required=True)
    status = fields.Selection([('refused', 'Refused'), ('accepted', 'Accepted'), ('pending', 'Pending')]
                              )
    offer_id = fields.Many2one("real.estate")
    create_date = fields.Date(string="Current Date", default=fields.Date.today(), readonly=True)
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    accept = fields.Boolean()
    refuse = fields.Boolean()

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.deadline and record.create_date:
                record.validity = (record.deadline - record.create_date).days
            elif record.deadline and record.validity:
                record.create_date = record.deadline - timedelta(days=record.validity)

