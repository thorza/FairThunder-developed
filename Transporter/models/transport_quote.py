from odoo import models, fields, api
from geopy.distance import geodesic


class TransportQuote(models.Model):
    _name = 'transport.quote'
    _description = 'Transport Quote'

    # Basic Fields
    name = fields.Char(string="Quote Name", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Assigned Vehicle")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    total_cost = fields.Float(string="Total Cost")

    # Geolocation Fields
    pickup_address = fields.Char(string='Pickup Address')
    pickup_lat = fields.Float(string='Pickup Latitude')
    pickup_lon = fields.Float(string='Pickup Longitude')
    dropoff_address = fields.Char(string='Dropoff Address')
    dropoff_lat = fields.Float(string='Dropoff Latitude')
    dropoff_lon = fields.Float(string='Dropoff Longitude')

    # Consignor/Consignee Fields
    consignor_id = fields.Many2one('res.partner', string='Consignor')
    consignee_id = fields.Many2one('res.partner', string='Consignee')

    # Load Details
    load_type_id = fields.Many2one('load.type', string='Load Type')
    load_weight = fields.Float(string='Load Weight')
    load_volume = fields.Float(string='Load Volume')

    # Computed Field for Route Distance
    route_distance_km = fields.Float(string='Route Distance (km)', compute='_compute_route_distance', store=True)

    # Trip Linking Field
    trip_id = fields.Many2one('transport.trip', string='Linked Trip')

    # State Field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft', readonly=True)

    @api.depends('pickup_lat', 'pickup_lon', 'dropoff_lat', 'dropoff_lon')
    def _compute_route_distance(self):
        for quote in self:
            if all([quote.pickup_lat, quote.pickup_lon, quote.dropoff_lat, quote.dropoff_lon]):
                pickup_coords = (quote.pickup_lat, quote.pickup_lon)
                dropoff_coords = (quote.dropoff_lat, quote.dropoff_lon)
                quote.route_distance_km = geodesic(pickup_coords, dropoff_coords).km
            else:
                quote.route_distance_km = 0

    def action_confirm(self):
        """Confirm the transport quote and send the email."""
        for record in self:
            record.state = 'confirmed'
            record.send_transport_quote_email()

    def send_transport_quote_email(self):
        """Send transport quote confirmation email."""
        self.ensure_one()  # Ensure the method is called on a single record
        email_template = self.env.ref('Transporter.transport_quote_email_template')
        if email_template:
            email_template.send_mail(self.id, force_send=True)
