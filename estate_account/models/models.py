from odoo import models, fields, api


# class Account(models.Model):
#     _inherit = "account.move"
#     _description = "Account Move"
#
#
# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"
#     _description = "Account Move Line"


class InheritModel(models.Model):
    _inherit = "real.estate"

    def sell(self):
        res = super(InheritModel, self).sell()

        invoice_line = []
        invoice_line.append((0, 0, {
            'name': self.name,
            'quantity': 1.0,
            'price_unit': self.selling_price,
        }))
        invoice_line.append((0, 0, {
            'name': 'property sale(6%)',
            'quantity': 1.0,
            'price_unit': self.selling_price * 0.6,

        }))
        invoice_line.append((0, 0, {
            'name': 'administrative fees',
            'quantity': 1.0,
            'price_unit': 100.00
        }))
        invoice_vals = {
            'partner_id': self.buyer,
            'move_type': 'out_invoice',
            'l10n_in_gst_treatment': 'consumer',
            'invoice_line_ids': invoice_line,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return invoice
