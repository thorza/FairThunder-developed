from odoo import models, fields, api

class FleetRig(models.Model):
    _name = 'fleet.rig'
    _description = 'Fleet Rig'

    name = fields.Char(string="Rig Name", required=True)
    rig_number = fields.Char(string="Rig Number", required=True)
    truck_id = fields.Many2one('fleet.vehicle', string="Truck Tractor", domain=[('drive', '=', 'engine')])
    trailer_ids = fields.Many2many('fleet.vehicle', string="Trailers", domain=[('drive', '=', 'no_engine')])
    gcm = fields.Float(string="GCM", compute="_compute_gcm", store=True)
    max_payload = fields.Float(string="Max Payload", compute="_compute_max_payload", store=True)

    total_tare = fields.Float(string="Total Tare Weight", compute="_compute_total_tare", store=True)
    total_gcm = fields.Float(string="Gross Combination Mass (GCM)", compute="_compute_total_gcm", store=True)
    max_load = fields.Float(string="Maximum Load Capacity", compute="_compute_max_load", store=True)

    @api.depends('truck_id', 'trailer_ids')
    def _compute_gcm(self):
        for rig in self:
            rig.gcm = rig.truck_id.gvm + sum(trailer.gvm for trailer in rig.trailer_ids)

    @api.depends('truck_id', 'trailer_ids')
    def _compute_max_payload(self):
        for rig in self:
            total_tare = rig.truck_id.tare + sum(trailer.tare for trailer in rig.trailer_ids)
            rig.max_payload = rig.gcm - total_tare if rig.gcm else 0

    @api.depends('truck_id', 'trailer_ids')
    def _compute_total_tare(self):
        for record in self:
            tractor_tare = record.truck_id.tare or 0
            trailers_tare = sum(trailer.tare or 0 for trailer in record.trailer_ids)
            record.total_tare = tractor_tare + trailers_tare

    @api.depends('truck_id', 'trailer_ids')
    def _compute_total_gcm(self):
        axle_weights = {
            2: 18000,  # 2 axles
            3: 24000,  # 3 axles
            4: 32000,  # 4 axles
            5: 40000,  # 5 axles
            6: 56000,  # 6 axles
        }
        for record in self:
            tractor_axles = record.truck_id.axles or 0
            trailer_axles = sum(trailer.axles or 0 for trailer in record.trailer_ids)
            total_axles = tractor_axles + trailer_axles
            record.total_gcm = axle_weights.get(total_axles, 0)

    @api.depends('total_gcm', 'total_tare')
    def _compute_max_load(self):
        for record in self:
            record.max_load = record.total_gcm - record.total_tare if record.total_gcm and record.total_tare else 0.0
