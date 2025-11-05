from flask import Flask, render_template, request, jsonify, make_response
import csv
from io import StringIO

app = Flask(__name__)


def calculate_points(x, y, D):
    """
    Calculate the positions of points on a 2D rectangle with staggered rows.
    
    Args:
        x: Width of rectangle in cm
        y: Height of rectangle in cm
        D: Distance between points in cm
    
    Returns:
        List of tuples containing (x_coord, y_coord) for each point
    """
    # Calculate d as the shortest dimension divided by D
    d = min(x, y) / D
    
    points = []
    
    # Start from bottom-left at (d, d)
    y_pos = d
    row_number = 1
    
    # Fill rows from bottom to top
    while y_pos <= y - d:
        # For even rows, offset the starting x position by 0.5*d
        if row_number % 2 == 0:
            x_pos = 1.5 * d  # Start at 1.5*d for even rows
        else:
            x_pos = d  # Start at d for odd rows
        
        # Fill columns from left to right
        while x_pos <= x - d:
            points.append((round(x_pos, 2), round(y_pos, 2)))
            x_pos += d
        
        y_pos += d
        row_number += 1
    
    return points


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate point coordinates based on user input"""
    try:
        data = request.get_json()
        x = float(data['x'])
        y = float(data['y'])
        D = float(data['D'])
        
        # Validate inputs
        if x <= 0 or y <= 0 or D <= 0:
            return jsonify({'error': 'All dimensions must be positive'}), 400
        
        if D > min(x, y):
            return jsonify({'error': 'Distance D must be smaller than the shortest dimension'}), 400
        
        points = calculate_points(x, y, D)
        
        return jsonify({
            'points': points,
            'rectangle': {'x': x, 'y': y},
            'd': min(x, y) / D
        })
    
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data'}), 400


@app.route('/download_csv', methods=['POST'])
def download_csv():
    """Generate and download CSV file with point coordinates"""
    try:
        data = request.get_json()
        x = float(data['x'])
        y = float(data['y'])
        D = float(data['D'])
        
        points = calculate_points(x, y, D)
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Point #', 'X (cm)', 'Y (cm)'])
        
        # Write points
        for i, (px, py) in enumerate(points, start=1):
            writer.writerow([i, px, py])
        
        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=rectangle_points.csv'
        
        return response
    
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
