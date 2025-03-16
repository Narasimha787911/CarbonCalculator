from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import CarbonFootprint
from calculator import calculate_carbon_footprint

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """Carbon footprint calculator form and submission"""
    if request.method == 'POST':
        try:
            # Create a new carbon footprint record
            footprint = CarbonFootprint(
                # Transportation
                car_miles=float(request.form.get('car_miles', 0)),
                car_efficiency=float(request.form.get('car_efficiency', 25)),
                public_transit_miles=float(request.form.get('public_transit_miles', 0)),
                flights_short=int(request.form.get('flights_short', 0)),
                flights_medium=int(request.form.get('flights_medium', 0)),
                flights_long=int(request.form.get('flights_long', 0)),
                
                # Home energy
                electricity_kwh=float(request.form.get('electricity_kwh', 0)),
                natural_gas_therms=float(request.form.get('natural_gas_therms', 0)),
                heating_oil_gallons=float(request.form.get('heating_oil_gallons', 0)),
                
                # Food & consumption
                diet_type=request.form.get('diet_type', 'omnivore')
            )
            
            # Calculate carbon footprint
            calculate_carbon_footprint(footprint)
            
            # Save to database
            db.session.add(footprint)
            db.session.commit()
            
            # Store ID in session for results page
            session['footprint_id'] = footprint.id
            
            return redirect(url_for('results'))
            
        except Exception as e:
            app.logger.error(f"Error processing form: {str(e)}")
            flash(f"An error occurred: {str(e)}", "danger")
    
    return render_template('calculator.html')

@app.route('/results')
def results():
    """Display carbon footprint calculation results"""
    footprint_id = session.get('footprint_id')
    
    if not footprint_id:
        flash("Please complete the calculator first", "warning")
        return redirect(url_for('calculator'))
    
    footprint = CarbonFootprint.query.get(footprint_id)
    
    if not footprint:
        flash("Could not find your calculation results", "danger")
        return redirect(url_for('calculator'))
    
    # Calculate percentages for chart
    total = footprint.total_footprint
    if total > 0:
        transport_percent = round((footprint.transportation_footprint / total) * 100)
        home_percent = round((footprint.home_energy_footprint / total) * 100)
        food_percent = round((footprint.food_footprint / total) * 100)
    else:
        transport_percent = home_percent = food_percent = 0
    
    return render_template(
        'results.html', 
        footprint=footprint,
        transport_percent=transport_percent,
        home_percent=home_percent,
        food_percent=food_percent
    )

@app.route('/about')
def about():
    """About page with information on methodology"""
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('base.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    app.logger.error(f"Server error: {str(e)}")
    return render_template('base.html', error="Internal server error"), 500
