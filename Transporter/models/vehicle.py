from odoo import models, fields

class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _description = 'Fleet Vehicle'

    name = fields.Char(string="Vehicle Name", required=True)
    make = fields.Char(string="Make", required=True)
    model = fields.Char(string="Model", required=True)
    registration = fields.Char(string="Number Plate")
    vin = fields.Char(string="VIN Number")
    vrn = fields.Char(string="Vehicle Registration Number")
    date_acquired = fields.Date(string="Date Acquired")
    current_kilometer = fields.Float(string="Current Kilometer")
    purchase_price = fields.Float(string="Purchase Price")
    residual_value = fields.Float(string="Residual Value")
    tare = fields.Float(string="Tare (kg)")
    gvm = fields.Float(string="GVM (kg)")
    axles = fields.Integer(string="Axles")
    drive = fields.Selection([('engine', 'Engine'), ('no_engine', 'No Engine')], string="Drive", default='engine')
    fuel_type = fields.Selection([('diesel', 'Diesel'), ('petrol', 'Petrol'), ('electric', 'Electric'), ('none', 'None')],
                                  string="Fuel Type", default='diesel')
    co2_emissions = fields.Float(string="CO2 Emissions (g/km)")
    indexed_fuel_consumption = fields.Float(string="Indexed Fuel Consumption (L/km)")
    next_maintenance = fields.Date(string="Next Maintenance Date")
    next_inspection = fields.Date(string="Next Inspection Date")
    next_license_renewal = fields.Date(string="Next License Renewal Date")

    # Subforms
    depreciation_schedule_ids = fields.One2many('fleet.depreciation', 'vehicle_id', string="Depreciation Schedule")
    maintenance_history_ids = fields.One2many('fleet.maintenance', 'vehicle_id', string="Maintenance History")
    inspection_ids = fields.One2many('fleet.inspection', 'vehicle_id', string="Inspection Records")
