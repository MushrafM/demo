from odoo import models, fields


class Supermarket(models.Model):
    _name = "supermarket.store"
    name = fields.Char(string="Product Name")
    price = fields.Integer(string="Product Price")
    quantity = fields.Integer(string="Quantity")
    manufacturing_date = fields.Date(string="Manufacturing Date")



# <?xml version="1.0" encoding="utf-8" ?>
# <odoo>
#     <record id="car_wizard_action" model="ir.actions.act_window">
#         <field name="name">Add New Fuel Type For Bike</field>
#         <field name="type">ir.actions.act_window</field>
#         <field name="res_model">wizard</field>
#         <field name="view_mode">form</field>
#         <field name="target">new</field>
#     </record>
#     <record id="car_wizard_form" model="ir.ui.view">
#         <field name="name">car.Wizard.Form</field>
#         <field name="model">wizard</field>
#         <field name="arch" type="xml">
#             <form>
#                 <group>
#                     <group>
#                         <field name="quantity_plus"/>
#                     </group>
#                     <group>
#
#
#
#                     </group>
#                 </group>
#                 <footer>
#                     <button name="asd" string="Confirm" type="object" class="btn-primary"/>
#                     <button string="Cancel" class="btn-default" special="cancel"/>
#                 </footer>
#             </form>
#         </field>
#     </record>
# </odoo>