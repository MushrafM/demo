from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "real estate"
    _order = "name desc"
    status1 = fields.Selection(
        [('new', 'New'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default="new",
        string="Status")
    # title = fields.Char(string="Title", readonly=True, required=True)
    location = fields.Char(string="Location")
    name = fields.Char(string="Name")
    active = fields.Boolean(default=True, string="Active")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(string="Date Availability", default=fields.date.today())
    expected_price = fields.Float(string="Expected Price", default="1")
    selling_price = fields.Integer(string="Selling Price", default=1)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    property_type = fields.Many2one("properties.properties", string="Property Type")
    property_tag = fields.Many2many("property.property", string='Property Tags')
    buyer = fields.Many2one('res.partner', string='Buyer')
    salesperson = fields.Many2one('res.users', string="SalesPerson", index=True, tracking=True,
                                  default=lambda self: self.env.user)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(default=False, requests=True)
    garden = fields.Boolean(default=False, requests=True)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
                                          string="Garden orientation")
    new_price = fields.Integer(string="Price")
    partner = fields.Many2one('res.partner', string="Partner")
    status = fields.Selection([('refused', 'Refused'), ('accepted', 'Accepted')])
    offers = fields.One2many('estate.property.offer', 'offer_id', 'PropertyOffer')
    best_offer = fields.Integer(string="Best offer", compute="calculate")
    total_area = fields.Integer(string="Total Area", compute="calculate_area")
    status2 = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold')],
        default="new")

    def sell(self):
        if self.status1 == 'cancelled':
            raise ValidationError("cannot sell the canceled property")
        self.status1 = 'sold'
        self.status2 = 'sold'
        print("jsf")

    def cancel(self):
        if self.status1 == 'sold':
            raise ValidationError("cannot cancel the sold property")
        self.status1 = 'cancelled'

    @api.onchange("date_availability")
    def change(self):
        today_date = fields.date.today()
        max_date = (today_date + timedelta(days=90)).strftime("%Y-%m-%d")
        if str(self.date_availability) > max_date:
            raise ValidationError("date must be within the next 90 days")
        else:
            store = True

    @api.onchange("garden_area")
    def calculate_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange("offers")
    def calculate(self):
        best_offer = 0
        for rec in self.offers:
            if rec.new_price > best_offer:
                best_offer = rec.new_price
        self.best_offer = best_offer

    @api.onchange("offers")
    def calc(self):
        for rec in self.offers:
            if rec.new_price == 0:
                raise ValidationError("price must be strictly positive")

    @api.onchange("expected_price")
    def exp_price(self):
        if self.expected_price == 0:
            raise ValidationError("the expected price must be strictly positive")
        elif self.expected_price < 0:
            raise ValidationError("price cant be negative")
        else:
            store = True

    @api.onchange("selling_price")
    def sell_price(self):
        for rec in self:
            if rec.selling_price < 0.9 * rec.expected_price:
                raise ValidationError(
                    "selling price must be at least of 90% of expected price.you must reduce this price if you want to accept this offer")

    @api.onchange("offers")
    def sold(self):
        for rec in self.offers:
            if rec.accept is True:
                rec.status = 'accepted'
                self.selling_price = rec.new_price
                self.buyer = rec.partner
            if rec.refuse is True:
                rec.status = 'refused'
            if rec.accept is False and rec.refuse is False:
                rec.status = 'pending'

    @api.onchange("offers")
    def stat_check(self):
        for rec in self.offers:
            if rec is not None:
                self.status2 = 'offer_received'
            if rec.status is 'accepted':
                self.status2 = 'offer_accepted'

    @api.onchange("offers")
    def tick(self):
        for record in self.offers:
            if record.status == 'accepted':
                for recc in self.offers:
                    if recc.status != 'accepted':
                        recc.refuse = True

    def unlink(self):
        for rec in self:
            if rec.status2 == 'offer_accepted':
                raise ValidationError("only new can be delete")
        return super(RealEstate, self).unlink()

    @api.onchange("offers")
    def cross(self):
        for che in self.offers:
            if che.accept is True:
                print("g")
                che.status = 'accepted'
                self.selling_price = che.new_price
                self.buyer = che.partner
            if che.accept is not True:
                che.status = 'refused'
            if che.refuse is True:
                che.status = 'refused'
            if che.accept is False and che.refuse is False:
                che.status = 'pending'

    @api.onchange("offers")
    def ticking(self):
        for check in self.offers:
            if check.status == 'accepted':
                for checking in self.offers:
                    if checking.status != 'accepted':
                        checking.refuse = True


class PropertiesType(models.Model):
    _name = "properties.properties"
    _order = "name desc"
    name = fields.Char(string="type")
    sequence = fields.Integer('Sequence', default=1)
    property_id = fields.One2many("real.estate", 'property_type', 'RealEstate')
    offer_count = fields.Integer(string="Offers", compute="offer")
    _sql_constraints = [
        ('unique_property_estate_name', 'unique(name)', 'A property type with this name already exists.'),
    ]

    def offer(self):
        var = 0
        for rec in self.property_id:
            var += 1
            self.offer_count = var


class PropertiesTags(models.Model):
    _name = "property.property"
    _order = "name desc"
    name = fields.Char(string="Tags")
    color = fields.Integer()

    _sql_constraints = [
        ('unique_property_property_name', 'unique(name)', 'A property tag with this name already exist.')
    ]
