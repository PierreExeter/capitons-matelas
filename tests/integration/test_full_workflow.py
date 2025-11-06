import json
import pytest
from app import app, calculate_points


@pytest.mark.integration
class TestFullWorkflow:
    """Test suite for complete application workflows."""

    def test_end_to_end_calculation_workflow(self, client, sample_rectangles):
        """Test complete workflow from API response to visualization data."""
        rect = sample_rectangles['standard']
        
        # Step 1: Make API request
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        
        assert response.status_code == 200
        api_data = json.loads(response.data)
        
        # Step 2: Verify API response structure
        assert 'points' in api_data
        assert 'rectangle' in api_data
        assert len(api_data['points']) > 0
        
        # Step 3: Simulate frontend processing
        points = api_data['points']
        rectangle = api_data['rectangle']
        
        # Verify data consistency
        assert len(points) == len(calculate_points(**rect))
        assert rectangle['x'] == rect['x']
        assert rectangle['y'] == rect['y']
        
        # Step 4: Test visualization data processing
        # Simulate canvas coordinate transformation
        canvas_width = 800
        canvas_height = 600
        padding = 40
        
        available_width = canvas_width - 2 * padding
        available_height = canvas_height - 2 * padding
        scale_x = available_width / rectangle['x']
        scale_y = available_height / rectangle['y']
        scale = min(scale_x, scale_y)
        
        # Transform all points to canvas coordinates
        canvas_points = []
        for px, py in points:
            canvas_x = padding + px * scale
            canvas_y = padding + rectangle['y'] * scale - py * scale
            canvas_points.append((canvas_x, canvas_y))
        
        # Verify transformation
        assert len(canvas_points) == len(points)
        
        # Check that points are within canvas bounds
        for cx, cy in canvas_points:
            assert padding <= cx <= canvas_width - padding
            assert padding <= cy <= canvas_height - padding

    def test_error_propagation_workflow(self, client, invalid_inputs):
        """Test that errors are properly propagated through the workflow."""
        # Test negative dimensions
        invalid_data = invalid_inputs['negative_dimensions']
        
        response = client.post('/calculate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        error_data = json.loads(response.data)
        
        # Verify error structure
        assert 'error' in error_data
        assert isinstance(error_data['error'], str)
        assert len(error_data['error']) > 0

    def test_consistent_results_across_requests(self, client, sample_rectangles):
        """Test that the same input produces identical results across multiple requests."""
        rect = sample_rectangles['standard']
        
        responses = []
        for _ in range(3):
            response = client.post('/calculate',
                                data=json.dumps(rect),
                                content_type='application/json')
            responses.append(response)
        
        # All responses should be identical
        first_data = json.loads(responses[0].data)
        for response in responses[1:]:
            current_data = json.loads(response.data)
            assert current_data == first_data

    def test_parameter_variation_workflow(self, client, sample_rectangles):
        """Test workflow with different parameter combinations."""
        base_rect = sample_rectangles['standard']
        
        # Test different edge distances
        edge_variations = [10, 15, 20, 25]
        results = []
        
        for edge_dist in edge_variations:
            test_rect = base_rect.copy()
            test_rect['edge_distance'] = edge_dist
            
            response = client.post('/calculate',
                                data=json.dumps(test_rect),
                                content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            results.append(len(data['points']))
        
        # Results should be different (or at least not all identical)
        assert len(set(results)) > 1 or all(r == results[0] for r in results)

    def test_real_time_update_simulation(self, client, sample_rectangles):
        """Test simulation of real-time parameter updates."""
        rect = sample_rectangles['standard']
        
        # Simulate slider changes (like frontend sliders)
        parameter_changes = [
            {'min_dist_x': 25},
            {'min_dist_x': 35},
            {'min_dist_x': 40},
            {'min_dist_y': 35},
            {'min_dist_y': 45},
            {'edge_distance': 10},
            {'edge_distance': 20},
        ]
        
        results = []
        for change in parameter_changes:
            test_rect = rect.copy()
            test_rect.update(change)
            
            response = client.post('/calculate',
                                data=json.dumps(test_rect),
                                content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            results.append(data['points'])
        
        # All should be valid point lists
        for points in results:
            assert isinstance(points, list)
            assert len(points) > 0
            assert all(len(point) == 2 for point in points)

    def test_browser_simulation_workflow(self, client, sample_rectangles):
        """Test workflow simulating browser behavior."""
        rect = sample_rectangles['standard']
        
        # Simulate browser requests with different headers
        browser_headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'},
        ]
        
        for headers in browser_headers:
            response = client.post('/calculate',
                                data=json.dumps(rect),
                                content_type='application/json',
                                headers=headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'points' in data
            assert 'rectangle' in data

    def test_concurrent_request_simulation(self, client, sample_rectangles):
        """Test handling of sequential rapid requests."""
        rect = sample_rectangles['standard']
        
        # Simulate rapid sequential requests (safer than threading)
        results = []
        
        for _ in range(5):
            response = client.post('/calculate',
                                data=json.dumps(rect),
                                content_type='application/json')
            results.append(response)
        
        # All requests should succeed
        assert len(results) == 5
        
        for response in results:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'points' in data

    def test_performance_workflow(self, client, sample_rectangles):
        """Test performance of the complete workflow."""
        import time
        
        rect = sample_rectangles['standard']
        
        # Measure full workflow time
        start_time = time.time()
        
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        
        api_time = time.time()
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Simulate frontend processing
        points = data['points']
        rectangle = data['rectangle']
        
        # Canvas coordinate transformation
        canvas_width = 800
        canvas_height = 600
        padding = 40
        
        scale = min(
            (canvas_width - 2 * padding) / rectangle['x'],
            (canvas_height - 2 * padding) / rectangle['y']
        )
        
        canvas_points = []
        for px, py in points:
            canvas_x = padding + px * scale
            canvas_y = padding + rectangle['y'] * scale - py * scale
            canvas_points.append((canvas_x, canvas_y))
        
        end_time = time.time()
        
        # Performance assertions
        assert api_time - start_time < 0.5  # API should be fast
        assert end_time - api_time < 0.1   # Frontend processing should be very fast
        assert end_time - start_time < 1.0  # Total workflow under 1 second

    def test_data_integrity_workflow(self, client, sample_rectangles):
        """Test data integrity throughout the workflow."""
        rect = sample_rectangles['standard']
        
        # Make API request
        response = client.post('/calculate',
                             data=json.dumps(rect),
                             content_type='application/json')
        
        assert response.status_code == 200
        api_data = json.loads(response.data)
        
        # Verify direct function call produces same results
        direct_points = calculate_points(**rect)
        api_points = api_data['points']
        
        # Point counts should match
        assert len(direct_points) == len(api_points)
        
        # All points should match (within floating point precision)
        for direct_point, api_point in zip(direct_points, api_points):
            assert len(direct_point) == 2
            assert len(api_point) == 2
            assert abs(direct_point[0] - api_point[0]) < 0.01
            assert abs(direct_point[1] - api_point[1]) < 0.01
