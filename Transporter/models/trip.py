from odoo import models, fields

class FleetTrip(models.Model):
    _name = 'fleet.trip'
    _description = 'Fleet Trip'

    name = fields.Char(string="Trip Name", required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    rig_id = fields.Many2one('fleet.rig', string="Rig")  # Add this field
    date = fields.Date(string="Trip Date", required=True)
    distance = fields.Float(string="Distance (km)")
    fuel_consumption = fields.Float(string="Fuel Consumption (L)")
