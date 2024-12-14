from odoo import models, fields

class FleetMaintenance(models.Model):
    _name = 'fleet.maintenance'
    _description = 'Fleet Maintenance'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    date = fields.Date(string="Maintenance Date", required=True)
    description = fields.Text(string="Description")
    cost = fields.Float(string="Cost")