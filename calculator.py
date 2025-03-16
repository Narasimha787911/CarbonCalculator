def calculate_carbon_footprint(footprint):
    """Calculate carbon footprint based on input data
    
    Args:
        footprint: CarbonFootprint model instance with input data
        
    Returns:
        Updated footprint object with calculated emissions
    """
    # Transportation calculations
    # Car: EPA average is ~0.404 kg CO2e per mile (depends on fuel efficiency)
    car_emissions = (footprint.car_miles / footprint.car_efficiency) * 8.887 if footprint.car_efficiency > 0 else 0
    
    # Public transit: ~0.14 kg CO2e per passenger mile (bus)
    public_transit_emissions = footprint.public_transit_miles * 0.14
    
    # Flights (kg CO2e per flight)
    flight_short_emissions = footprint.flights_short * 500  # ~500kg per short flight
    flight_medium_emissions = footprint.flights_medium * 1200  # ~1200kg per medium flight
    flight_long_emissions = footprint.flights_long * 3000  # ~3000kg per long flight
    
    # Sum transportation emissions
    transportation_footprint = (
        car_emissions + 
        public_transit_emissions + 
        flight_short_emissions + 
        flight_medium_emissions + 
        flight_long_emissions
    )
    
    # Home energy calculations
    # Electricity: ~0.45 kg CO2e per kWh (US average)
    electricity_emissions = footprint.electricity_kwh * 0.45
    
    # Natural gas: ~5.3 kg CO2e per therm
    natural_gas_emissions = footprint.natural_gas_therms * 5.3
    
    # Heating oil: ~10.15 kg CO2e per gallon
    heating_oil_emissions = footprint.heating_oil_gallons * 10.15
    
    # Sum home energy emissions
    home_energy_footprint = (
        electricity_emissions + 
        natural_gas_emissions + 
        heating_oil_emissions
    )
    
    # Food & consumption calculations (simplified based on diet type)
    diet_emissions = {
        'vegan': 1500,  # Annual kg CO2e for vegan diet
        'vegetarian': 2000,  # Annual kg CO2e for vegetarian diet
        'pescatarian': 2500,  # Annual kg CO2e for pescatarian diet
        'omnivore': 3000,  # Annual kg CO2e for average omnivore diet
        'high_meat': 4000  # Annual kg CO2e for high meat diet
    }
    
    # Get annual diet emissions and convert to daily (divide by 365)
    food_footprint = diet_emissions.get(footprint.diet_type, 3000)
    
    # Calculate total footprint
    total_footprint = transportation_footprint + home_energy_footprint + food_footprint
    
    # Update footprint object
    footprint.transportation_footprint = round(transportation_footprint, 2)
    footprint.home_energy_footprint = round(home_energy_footprint, 2)
    footprint.food_footprint = round(food_footprint, 2)
    footprint.total_footprint = round(total_footprint, 2)
    
    return footprint
