from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTransportQuote(TransactionCase):

    def setUp(self):
        super(TestTransportQuote, self).setUp()

        # Create a partner for testing
        self.customer = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@example.com',
        })

        # Create a vehicle for testing
        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'Test Vehicle',
        })

        # Create a load type for testing
        self.load_type = self.env['load.type'].create({
            'name': 'General Cargo',
        })

        # Create a transport quote
        self.transport_quote = self.env['transport.quote'].create({
            'name': 'Test Quote',
            'customer_id': self.customer.id,
            'vehicle_id': self.vehicle.id,
            'pickup_address': 'Pickup Address',
            'dropoff_address': 'Dropoff Address',
            'load_type_id': self.load_type.id,
            'load_weight': 1000.0,
            'load_volume': 10.0,
            'total_cost': 5000.0,
        })

    def test_transport_quote_creation(self):
        """Test the creation of a transport quote."""
        self.assertEqual(self.transport_quote.name, 'Test Quote')
        self.assertEqual(self.transport_quote.customer_id, self.customer)
        self.assertEqual(self.transport_quote.vehicle_id, self.vehicle)
        self.assertEqual(self.transport_quote.load_type_id, self.load_type)
        self.assertEqual(self.transport_quote.total_cost, 5000.0)

    def test_route_distance_computation(self):
        """Test the computation of route distance."""
        self.transport_quote.write({
            'pickup_lat': 40.712776,
            'pickup_lon': -74.005974,
            'dropoff_lat': 34.052235,
            'dropoff_lon': -118.243683,
        })
        self.transport_quote._compute_route_distance()
        self.assertGreater(self.transport_quote.route_distance_km, 0)

    def test_confirm_quote(self):
        """Test confirming a transport quote."""
        self.assertEqual(self.transport_quote.state, 'draft')
        self.transport_quote.action_confirm()
        self.assertEqual(self.transport_quote.state, 'confirmed')

    def test_email_sending(self):
        """Test email sending on confirmation."""
        email_template = self.env.ref('Transporter.transport_quote_email_template')
        self.assertTrue(email_template, "Email template not found")

        # Confirm the quote to trigger the email
        self.transport_quote.action_confirm()

        # Check if an email has been queued
        mail = self.env['mail.mail'].search([('state', '=', 'outgoing')], limit=1)
        self.assertTrue(mail, "No email was sent")
        self.assertEqual(mail.email_to, self.customer.email)
