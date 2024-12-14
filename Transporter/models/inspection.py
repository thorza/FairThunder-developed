from odoo import models, fields

class FleetInspection(models.Model):
    _name = 'fleet.inspection'
    _description = 'Fleet Inspection'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    date = fields.Date(string="Inspection Date", required=True)
    inspector = fields.Char(string="Inspector")
    remarks = fields.Text(string="Remarks")