import json
import pytest
from app import app


class TestAPIEndpoints:
    """Test suite for Flask API endpoints."""

    def test_index_route(self, client):
        """Test that the main page loads correctly."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'html' in response.data.lower()
        assert b'calculateur' in response.data.lower()

    def test_calculate_route_valid_request(self, client, sample_rectangles):
        """Test calculate endpoint with valid data."""
        rect = sample_rectangles['standard']
        
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check response structure
        assert 'points' in data
        assert 'rectangle' in data
        
        # Check points structure
        assert isinstance(data['points'], list)
        assert len(data['points']) > 0
        
        # Check rectangle structure
        assert 'x' in data['rectangle']
        assert 'y' in data['rectangle']
        assert data['rectangle']['x'] == rect['x']
        assert data['rectangle']['y'] == rect['y']

    def test_calculate_route_default_values(self, client):
        """Test calculate endpoint with missing optional parameters."""
        minimal_data = {'x': 220, 'y': 240}
        
        response = client.post('/calculate',
                             data=json.dumps(minimal_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should use default values for missing parameters
        assert len(data['points']) > 0

    def test_calculate_route_invalid_json(self, client):
        """Test calculate endpoint with malformed JSON."""
        response = client.post('/calculate',
                             data='invalid json',
                             content_type='application/json')
        
        # Flask returns HTML error page for invalid JSON, not JSON error
        assert response.status_code == 400
        # Don't try to parse HTML as JSON
        assert b'Bad Request' in response.data or b'error' in response.data.lower()

    def test_calculate_route_missing_required_fields(self, client):
        """Test calculate endpoint with missing required fields."""
        incomplete_data = {'x': 220}  # Missing 'y'
        
        response = client.post('/calculate',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_calculate_route_negative_dimensions(self, client):
        """Test calculate endpoint with negative dimensions."""
        invalid_data = {
            'x': -10,
            'y': 240,
            'min_dist_x': 30,
            'min_dist_y': 40,
            'edge_distance': 15
        }
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'positive' in data['error'].lower()

    def test_calculate_route_zero_dimensions(self, client):
        """Test calculate endpoint with zero dimensions."""
        invalid_data = {
            'x': 0,
            'y': 240,
            'min_dist_x': 30,
            'min_dist_y': 40,
            'edge_distance': 15
        }
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'positive' in data['error'].lower()

    def test_calculate_route_negative_distances(self, client):
        """Test calculate endpoint with negative distances."""
        invalid_data = {
            'x': 220,
            'y': 240,
            'min_dist_x': -5,
            'min_dist_y': 40,
            'edge_distance': 15
        }
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'positive' in data['error'].lower()

    def test_calculate_route_zero_distances(self, client):
        """Test calculate endpoint with zero distances."""
        invalid_data = {
            'x': 220,
            'y': 240,
            'min_dist_x': 0,
            'min_dist_y': 40,
            'edge_distance': 15
        }
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'positive' in data['error'].lower()

    def test_calculate_route_content_type(self, client, sample_rectangles):
        """Test calculate endpoint with wrong content type."""
        rect = sample_rectangles['standard']
        
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='text/plain')
        
        # Flask returns 415 for unsupported content type
        assert response.status_code == 415

    def test_calculate_route_empty_request(self, client):
        """Test calculate endpoint with empty request body."""
        response = client.post('/calculate',
                             data='',
                             content_type='application/json')
        
        assert response.status_code == 400

    def test_calculate_route_large_values(self, client):
        """Test calculate endpoint with large dimension values."""
        large_data = {
            'x': 5000,
            'y': 3000,
            'min_dist_x': 100,
            'min_dist_y': 150,
            'edge_distance': 50
        }
        
        response = client.post('/calculate',
                             data=json.dumps(large_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should handle large values without issues
        assert 'points' in data
        assert len(data['points']) > 0

    def test_calculate_route_decimal_values(self, client):
        """Test calculate endpoint with decimal values."""
        decimal_data = {
            'x': 220.5,
            'y': 240.7,
            'min_dist_x': 30.2,
            'min_dist_y': 40.8,
            'edge_distance': 15.3
        }
        
        response = client.post('/calculate',
                             data=json.dumps(decimal_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should handle decimal values correctly
        assert 'points' in data
        assert 'rectangle' in data
        assert data['rectangle']['x'] == 220.5
        assert data['rectangle']['y'] == 240.7

    def test_calculate_route_string_values(self, client):
        """Test calculate endpoint with string values (should be converted)."""
        string_data = {
            'x': '220',
            'y': '240',
            'min_dist_x': '30',
            'min_dist_y': '40',
            'edge_distance': '15'
        }
        
        response = client.post('/calculate',
                             data=json.dumps(string_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should convert string values to numbers
        assert 'points' in data
        assert data['rectangle']['x'] == 220.0
        assert data['rectangle']['y'] == 240.0

    def test_calculate_route_non_numeric_values(self, client):
        """Test calculate endpoint with non-numeric values."""
        invalid_data = {
            'x': 'not_a_number',
            'y': 240,
            'min_dist_x': 30,
            'min_dist_y': 40,
            'edge_distance': 15
        }
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_response_time(self, client, sample_rectangles):
        """Test that API responses are fast enough."""
        import time
        
        rect = sample_rectangles['standard']
        
        start_time = time.time()
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        end_time = time.time()
        
        assert response.status_code == 200
        # Should respond in under 1 second
        assert end_time - start_time < 1.0

    def test_response_headers(self, client, sample_rectangles):
        """Test that response has correct headers."""
        rect = sample_rectangles['standard']
        
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # Flask test client may not include charset, that's OK

    def test_multiple_requests(self, client, sample_rectangles):
        """Test handling multiple concurrent-like requests."""
        rect = sample_rectangles['standard']
        
        responses = []
        for _ in range(5):
            response = client.post('/calculate',
                                data=json.dumps(rect),
                                content_type='application/json')
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'points' in data
            assert len(data['points']) > 0
        
        # All responses should be identical
        first_data = json.loads(responses[0].data)
        for response in responses[1:]:
            current_data = json.loads(response.data)
            assert current_data == first_data
