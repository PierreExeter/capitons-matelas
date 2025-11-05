from flask import Flask, render_template, request, jsonify, make_response
import csv
from io import StringIO

app = Flask(__name__)


def calculate_points(x, y):
    """
    Calculate the positions of points on a 2D rectangle with corner-based pattern.
    
    Args:
        x: Width of rectangle in cm
        y: Height of rectangle in cm
    
    Returns:
        List of tuples containing (x_coord, y_coord) for each point
    """
    import math
    
    points = []
    min_dist_x = 30
    min_dist_y = 40
    
    # Step 1: Place the 4 corner points
    corner1 = (15, 15)
    corner2 = (x - 15, 15)
    corner3 = (15, y - 15)
    corner4 = (x - 15, y - 15)
    
    # Step 2: Calculate horizontal spacing
    dx_max = x - 30
    nbx = math.floor(dx_max / min_dist_x)
    
    # Avoid division by zero
    if nbx == 0:
        nbx = 1
    
    dx = dx_max / nbx
    
    # Step 5: Calculate vertical spacing
    dy_max = y - 30
    nby = math.floor(dy_max / min_dist_y)
    
    # Avoid division by zero
    if nby == 0:
        nby = 1
    
    dy = dy_max / nby
    
    # Step 3: Place points on the first row (y = 15)
    points.append(corner1)  # (15, 15)
    for i in range(1, nbx + 1):
        x_pos = 15 + i * dx
        if x_pos < x - 15:  # Don't duplicate corner2
            points.append((round(x_pos, 2), 15))
    points.append(corner2)  # (x-15, 15)
    
    # Step 6: Place points on intermediate rows
    current_y = 15 + dy
    while current_y < y - 15:
        # Add left corner point
        points.append((15, round(current_y, 2)))
        
        # Add intermediate points
        for i in range(1, nbx + 1):
            x_pos = 15 + i * dx
            if x_pos < x - 15:
                points.append((round(x_pos, 2), round(current_y, 2)))
        
        # Add right corner point
        points.append((x - 15, round(current_y, 2)))
        
        current_y += dy
    
    # Step 4: Place points on the last row (y = y-15)
    points.append(corner3)  # (15, y-15)
    for i in range(1, nbx + 1):
        x_pos = 15 + i * dx
        if x_pos < x - 15:  # Don't duplicate corner4
            points.append((round(x_pos, 2), round(y - 15, 2)))
    points.append(corner4)  # (x-15, y-15)
    
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
        
        # Validate inputs
        if x <= 0 or y <= 0:
            return jsonify({'error': 'All dimensions must be positive'}), 400
        
        points = calculate_points(x, y)
        
        return jsonify({
            'points': points,
            'rectangle': {'x': x, 'y': y}
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
        
        points = calculate_points(x, y)
        
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
