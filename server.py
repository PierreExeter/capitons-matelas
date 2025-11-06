"""Flask application with Waitress for Vercel deployment."""
from flask import Flask, render_template, request, jsonify
import math
from waitress import serve


def calculate_points(x, y, min_dist_x=30, min_dist_y=40, edge_distance=15):
    """
    Calculate positions of points on a 2D rectangle with corner-based pattern.
    
    Args:
        x: Width of rectangle in cm
        y: Height of rectangle in cm
        min_dist_x: Minimum distance between points along x-axis (default 30)
        min_dist_y: Minimum distance between points along y-axis (default 40)
        edge_distance: Distance from rectangle edges for corner points (default 15)
    
    Returns:
        List of tuples containing (x_coord, y_coord) for each point
    """
    
    points = []
    
    # Step 1: Place 4 corner points
    corner1 = (edge_distance, edge_distance)
    corner2 = (x - edge_distance, edge_distance)
    corner3 = (edge_distance, y - edge_distance)
    corner4 = (x - edge_distance, y - edge_distance)
    
    # Step 2: Calculate horizontal spacing
    dx_max = x - 2 * edge_distance
    nbx = math.floor(dx_max / min_dist_x)
    
    # Avoid division by zero
    if nbx == 0:
        nbx = 1
    
    dx = dx_max / nbx
    
    # Step 5: Calculate vertical spacing
    dy_max = y - 2 * edge_distance
    nby = math.floor(dy_max / min_dist_y)
    
    # Avoid division by zero
    if nby == 0:
        nby = 1
    
    dy = dy_max / nby
    
    # Step 3: Place points on first row (y = edge_distance) - EVEN ROW
    points.append(corner1)  # (edge_distance, edge_distance)
    for i in range(1, nbx + 1):
        x_pos = edge_distance + i * dx
        if x_pos < x - edge_distance:  # Don't duplicate corner2
            points.append((round(x_pos, 2), edge_distance))
    points.append(corner2)  # (x-edge_distance, edge_distance)
    
    # Step 6: Place points on intermediate rows (alternating even and odd/staggered rows)
    current_y = edge_distance + 0.5 * dy
    row_counter = 0
    
    while current_y < y - edge_distance:
        is_odd_row = (row_counter % 2 == 0)  # First iteration is odd row (staggered)
        
        if is_odd_row:
            # ODD ROW (staggered): Offset horizontally by 0.5*dx
            # No corner points on staggered rows
            for i in range(nbx + 1):
                x_pos = edge_distance + (i + 0.5) * dx
                if x_pos < x - edge_distance:
                    points.append((round(x_pos, 2), round(current_y, 2)))
        else:
            # EVEN ROW (regular): Include corner points
            points.append((edge_distance, round(current_y, 2)))
            
            for i in range(1, nbx + 1):
                x_pos = edge_distance + i * dx
                if x_pos < x - edge_distance:
                    points.append((round(x_pos, 2), round(current_y, 2)))
            
            points.append((x - edge_distance, round(current_y, 2)))
        
        current_y += 0.5 * dy
        row_counter += 1
    
    # Step 4: Place points on last row (y = y-edge_distance) - EVEN ROW
    points.append(corner3)  # (edge_distance, y-edge_distance)
    for i in range(1, nbx + 1):
        x_pos = edge_distance + i * dx
        if x_pos < x - edge_distance:  # Don't duplicate corner4
            points.append((round(x_pos, 2), round(y - edge_distance, 2)))
    points.append(corner4)  # (x-edge_distance, y-edge_distance)
    
    return points


app = Flask(__name__)


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate point coordinates based on user input."""
    try:
        data = request.get_json()
        x = float(data['x'])
        y = float(data['y'])
        min_dist_x = float(data.get('min_dist_x', 30))
        min_dist_y = float(data.get('min_dist_y', 40))
        edge_distance = float(data.get('edge_distance', 15))
        
        # Validate inputs
        if x <= 0 or y <= 0:
            return jsonify({'error': 'All dimensions must be positive'}), 400
        if min_dist_x <= 0 or min_dist_y <= 0 or edge_distance <= 0:
            return jsonify({'error': 'All distances must be positive'}), 400
        
        points = calculate_points(x, y, min_dist_x, min_dist_y, edge_distance)
        
        return jsonify({
            'points': points,
            'rectangle': {'x': x, 'y': y}
        })
    
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data'}), 400


@app.route('/health')
def health():
    """Health check endpoint for production monitoring."""
    return jsonify({'status': 'healthy', 'service': 'matelas-calc'}), 200


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Production server with Waitress
    serve(app, host='0.0.0.0', port=8000)
