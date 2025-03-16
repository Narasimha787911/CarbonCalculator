from datetime import datetime
from app import db

class CarbonFootprint(db.Model):
    """Model for storing carbon footprint calculation data"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Transportation
    car_miles = db.Column(db.Float, default=0)
    car_efficiency = db.Column(db.Float, default=0) 
    public_transit_miles = db.Column(db.Float, default=0)
    flights_short = db.Column(db.Integer, default=0)  # < 1000 miles
    flights_medium = db.Column(db.Integer, default=0) # 1000-3000 miles
    flights_long = db.Column(db.Integer, default=0)   # > 3000 miles
    
    # Home energy
    electricity_kwh = db.Column(db.Float, default=0)
    natural_gas_therms = db.Column(db.Float, default=0)
    heating_oil_gallons = db.Column(db.Float, default=0)
    
    # Food & consumption
    diet_type = db.Column(db.String(50), default="omnivore")
    
    # Results
    transportation_footprint = db.Column(db.Float, default=0)
    home_energy_footprint = db.Column(db.Float, default=0)
    food_footprint = db.Column(db.Float, default=0)
    total_footprint = db.Column(db.Float, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CarbonFootprint {self.id}: {self.total_footprint} kg CO2e>'
