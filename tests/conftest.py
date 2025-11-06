import pytest
from app import app, calculate_points


@pytest.fixture
def client():
    """Create a test client for Flask application."""
    app.config['TESTING'] = True
    
    # Create app context for all tests
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def sample_rectangles():
    """Provide sample rectangle data for testing."""
    return {
        'standard': {'x': 220, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15},
        'small': {'x': 50, 'y': 60, 'min_dist_x': 15, 'min_dist_y': 20, 'edge_distance': 10},
        'large': {'x': 500, 'y': 800, 'min_dist_x': 50, 'min_dist_y': 60, 'edge_distance': 25},
        'minimal': {'x': 20, 'y': 30, 'min_dist_x': 10, 'min_dist_y': 10, 'edge_distance': 5},
        'square': {'x': 200, 'y': 200, 'min_dist_x': 25, 'min_dist_y': 25, 'edge_distance': 20},
    }


@pytest.fixture
def expected_point_counts():
    """Expected point counts for different scenarios."""
    return {
        'standard_220x240': 25,  # Based on current algorithm
        'small_50x60': 9,
        'minimal_20x30': 4,
    }


@pytest.fixture
def invalid_inputs():
    """Provide invalid input data for testing error handling."""
    return {
        'negative_dimensions': {'x': -10, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15},
        'zero_dimensions': {'x': 0, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15},
        'negative_distances': {'x': 220, 'y': 240, 'min_dist_x': -5, 'min_dist_y': 40, 'edge_distance': 15},
        'zero_distances': {'x': 220, 'y': 240, 'min_dist_x': 0, 'min_dist_y': 40, 'edge_distance': 15},
        'edge_too_large': {'x': 220, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 150},
    }
