from flask import Flask, render_template, request, jsonify, make_response
import csv
from io import StringIO

app = Flask(__name__)


def calculate_points(x, y, min_dist_x=30, min_dist_y=40):
    """
    Calculate positions of points on a 2D rectangle with corner-based pattern.
    
    Args:
        x: Width of rectangle in cm
        y: Height of rectangle in cm
        min_dist_x: Minimum distance between points along x-axis (default 30)
        min_dist_y: Minimum distance between points along y-axis (default 40)
    
    Returns:
        List of tuples containing (x_coord, y_coord) for each point
    """
    import math
    
    points = []
    
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
    
    # Step 3: Place points on the first row (y = 15) - EVEN ROW
    points.append(corner1)  # (15, 15)
    for i in range(1, nbx + 1):
        x_pos = 15 + i * dx
        if x_pos < x - 15:  # Don't duplicate corner2
            points.append((round(x_pos, 2), 15))
    points.append(corner2)  # (x-15, 15)
    
    # Step 6: Place points on intermediate rows (alternating even and odd/staggered rows)
    current_y = 15 + 0.5 * dy
    row_counter = 0
    
    while current_y < y - 15:
        is_odd_row = (row_counter % 2 == 0)  # First iteration is odd row (staggered)
        
        if is_odd_row:
            # ODD ROW (staggered): Offset horizontally by 0.5*dx
            # No corner points on staggered rows
            for i in range(nbx + 1):
                x_pos = 15 + (i + 0.5) * dx
                if x_pos < x - 15:
                    points.append((round(x_pos, 2), round(current_y, 2)))
        else:
            # EVEN ROW (regular): Include corner points
            points.append((15, round(current_y, 2)))
            
            for i in range(1, nbx + 1):
                x_pos = 15 + i * dx
                if x_pos < x - 15:
                    points.append((round(x_pos, 2), round(current_y, 2)))
            
            points.append((x - 15, round(current_y, 2)))
        
        current_y += 0.5 * dy
        row_counter += 1
    
    # Step 4: Place points on the last row (y = y-15) - EVEN ROW
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
        min_dist_x = float(data.get('min_dist_x', 30))
        min_dist_y = float(data.get('min_dist_y', 40))
        
        # Validate inputs
        if x <= 0 or y <= 0:
            return jsonify({'error': 'All dimensions must be positive'}), 400
        if min_dist_x <= 0 or min_dist_y <= 0:
            return jsonify({'error': 'Minimum distances must be positive'}), 400
        
        points = calculate_points(x, y, min_dist_x, min_dist_y)
        
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
        min_dist_x = float(data.get('min_dist_x', 30))
        min_dist_y = float(data.get('min_dist_y', 40))
        
        points = calculate_points(x, y, min_dist_x, min_dist_y)
        
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
