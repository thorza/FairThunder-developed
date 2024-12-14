from odoo import models, fields

class FleetDepreciation(models.Model):
    _name = 'fleet.depreciation'
    _description = 'Fleet Depreciation'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    date = fields.Date(string="Depreciation Date", required=True)
    value = fields.Float(string="Depreciation Value")