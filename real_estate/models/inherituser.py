from odoo import models, fields


class InheritUser(models.Model):
    _inherit = "res.users"

    salesperson = fields.One2many("real.estate", "salesperson", "RealEstate")
