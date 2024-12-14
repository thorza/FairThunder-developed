from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
from geopy.geocoders import Nominatim

_logger = logging.getLogger(__name__)

class FleetDepot(models.Model):
    _name = 'fleet.depot'
    _description = 'Fleet Depot'

    # Fields
    name = fields.Char(string="Depot Name", required=True)  # Name field as the identifier
    address_search = fields.Char(string="Search Address")
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    latitude = fields.Float(string="Latitude", readonly=True)
    longitude = fields.Float(string="Longitude", readonly=True)
    vehicles = fields.Many2many('fleet.vehicle', string="Vehicles")

    # Onchange to handle address search and populate fields
    @api.onchange('address_search')
    def _onchange_address_search(self):
        if self.address_search:
            geolocator = Nominatim(user_agent="odoo_geolocator")
            try:
                # Perform geolocation lookup
                location = geolocator.geocode(self.address_search)
                if location:
                    self.address = location.address
                    self.latitude = location.latitude
                    self.longitude = location.longitude

                    # Reverse geocode for detailed fields (city, state, country)
                    location_detail = geolocator.reverse((location.latitude, location.longitude), exactly_one=True)
                    if location_detail and 'address' in location_detail.raw:
                        address_data = location_detail.raw['address']
                        self.city = address_data.get('city', address_data.get('town', address_data.get('village', '')))
                        self.state_id = self._get_state(address_data.get('state'))
                        self.country_id = self._get_country(address_data.get('country'))
                else:
                    raise UserError(_('Could not find coordinates for the address.'))
            except Exception as e:
                _logger.error(f"Geocoding failed: {e}")
                raise UserError(_('Error occurred during geocoding.'))

    # Helper to find or create state
    def _get_state(self, state_name):
        if state_name:
            state = self.env['res.country.state'].search([('name', '=', state_name)], limit=1)
            if not state:
                # Create state if it doesn't exist (optional)
                country = self.env['res.country'].search([], limit=1)  # Default to a country if none is linked
                state = self.env['res.country.state'].create({'name': state_name, 'country_id': country.id})
            return state.id
        return False

    # Helper to find or create country
    def _get_country(self, country_name):
        if country_name:
            country = self.env['res.country'].search([('name', '=', country_name)], limit=1)
            if not country:
                # Create country if it doesn't exist (optional)
                country = self.env['res.country'].create({'name': country_name})
            return country.id
        return False
