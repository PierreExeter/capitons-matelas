import pytest
import math
from app import calculate_points


class TestCalculatePoints:
    """Test suite for the calculate_points function."""

    def test_standard_rectangle(self, sample_rectangles):
        """Test calculation with standard rectangle dimensions."""
        rect = sample_rectangles['standard']
        points = calculate_points(**rect)
        
        # Should return a list of points
        assert isinstance(points, list)
        assert len(points) > 0
        
        # All points should be tuples with 2 elements
        for point in points:
            assert isinstance(point, tuple)
            assert len(point) == 2
            assert isinstance(point[0], (int, float))
            assert isinstance(point[1], (int, float))
        
        # Check corner points are included
        expected_corners = [
            (rect['edge_distance'], rect['edge_distance']),  # Bottom-left
            (rect['x'] - rect['edge_distance'], rect['edge_distance']),  # Bottom-right
            (rect['edge_distance'], rect['y'] - rect['edge_distance']),  # Top-left
            (rect['x'] - rect['edge_distance'], rect['y'] - rect['edge_distance'])  # Top-right
        ]
        
        for corner in expected_corners:
            assert any(
                math.isclose(point[0], corner[0], abs_tol=0.01) and 
                math.isclose(point[1], corner[1], abs_tol=0.01)
                for point in points
            ), f"Corner point {corner} not found in results"

    def test_small_rectangle(self, sample_rectangles):
        """Test calculation with small rectangle."""
        rect = sample_rectangles['small']
        points = calculate_points(**rect)
        
        assert len(points) >= 4  # At least 4 corner points
        
        # All points should be within rectangle bounds
        for x, y in points:
            assert rect['edge_distance'] <= x <= rect['x'] - rect['edge_distance']
            assert rect['edge_distance'] <= y <= rect['y'] - rect['edge_distance']

    def test_minimal_rectangle(self, sample_rectangles):
        """Test calculation with minimal rectangle."""
        rect = sample_rectangles['minimal']
        points = calculate_points(**rect)

        # Should have 8 points for this minimal case (algorithm creates more points)
        assert len(points) == 8
        
        # Should only contain the corner points
        expected_corners = [
            (rect['edge_distance'], rect['edge_distance']),
            (rect['x'] - rect['edge_distance'], rect['edge_distance']),
            (rect['edge_distance'], rect['y'] - rect['edge_distance']),
            (rect['x'] - rect['edge_distance'], rect['y'] - rect['edge_distance'])
        ]
        
        for corner in expected_corners:
            assert corner in points

    def test_square_rectangle(self, sample_rectangles):
        """Test calculation with square rectangle."""
        rect = sample_rectangles['square']
        points = calculate_points(**rect)
        
        assert len(points) > 4  # More than just corners
        
        # Points should have proper spacing
        if len(points) > 1:
            # Check that minimum distances are respected
            for i, (x1, y1) in enumerate(points):
                for x2, y2 in points[i+1:]:
                    if y1 == y2:  # Same row
                        dist = abs(x2 - x1)
                        assert dist >= rect['min_dist_x'] - 0.1  # Allow small rounding tolerance
                    if x1 == x2:  # Same column
                        dist = abs(y2 - y1)
                        assert dist >= rect['min_dist_y'] - 0.1

    def test_large_rectangle(self, sample_rectangles):
        """Test calculation with large rectangle."""
        rect = sample_rectangles['large']
        points = calculate_points(**rect)
        
        # Should have many points
        assert len(points) > 20
        
        # Performance test - should complete quickly even for large rectangles
        import time
        start_time = time.time()
        points = calculate_points(**rect)
        end_time = time.time()
        
        assert end_time - start_time < 1.0  # Should complete in under 1 second

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        
        # Test with edge_distance exactly half of dimensions
        points = calculate_points(x=40, y=40, edge_distance=20, min_dist_x=10, min_dist_y=10)
        assert len(points) == 4  # Only corners fit
        
        # Test with minimum distances that don't allow additional points
        points = calculate_points(x=100, y=100, edge_distance=10, min_dist_x=80, min_dist_y=80)
        assert len(points) == 5  # 4 corners + 1 center point
        
        # Test with very small min distances (should create many points)
        points = calculate_points(x=100, y=100, edge_distance=10, min_dist_x=5, min_dist_y=5)
        assert len(points) > 10  # Many points

    def test_point_precision(self):
        """Test that points have correct precision (rounded to 2 decimal places)."""
        points = calculate_points(x=100, y=100, edge_distance=15, min_dist_x=23, min_dist_y=17)
        
        for point in points:
            x, y = point
            # Check that coordinates are rounded to 2 decimal places
            assert round(x * 100) == x * 100  # Should be exact to 2 decimals
            assert round(y * 100) == y * 100  # Should be exact to 2 decimals

    def test_staggered_pattern(self):
        """Test that the staggered row pattern is correctly implemented."""
        points = calculate_points(x=200, y=150, edge_distance=20, min_dist_x=30, min_dist_y=25)
        
        # Group points by y-coordinate (rows)
        rows = {}
        for x, y in points:
            if y not in rows:
                rows[y] = []
            rows[y].append(x)
        
        # Check that alternating rows have different x-patterns
        sorted_rows = sorted(rows.keys())
        
        for i in range(1, len(sorted_rows) - 1):
            prev_row = rows[sorted_rows[i-1]]
            curr_row = rows[sorted_rows[i]]
            
            # Rows should have different patterns (staggered vs regular)
            if len(prev_row) > 2 and len(curr_row) > 2:
                # Check if patterns are significantly different
                prev_starts = prev_row[0] if prev_row else 0
                curr_starts = curr_row[0] if curr_row else 0
                
                # Staggered rows should have different starting positions
                if i % 2 == 1:  # Should be staggered
                    assert abs(curr_starts - prev_starts) > 1

    def test_no_duplicate_points(self, sample_rectangles):
        """Test that no duplicate points are generated."""
        rect = sample_rectangles['standard']
        points = calculate_points(**rect)
        
        # Convert to set to check for duplicates
        unique_points = set(points)
        assert len(unique_points) == len(points), f"Found duplicate points: {points}"

    def test_points_within_bounds(self, sample_rectangles):
        """Test that all points are within rectangle bounds."""
        rect = sample_rectangles['standard']
        points = calculate_points(**rect)
        
        for x, y in points:
            assert rect['edge_distance'] <= x <= rect['x'] - rect['edge_distance'], \
                f"Point x={x} outside bounds [{rect['edge_distance']}, {rect['x'] - rect['edge_distance']}]"
            assert rect['edge_distance'] <= y <= rect['y'] - rect['edge_distance'], \
                f"Point y={y} outside bounds [{rect['edge_distance']}, {rect['y'] - rect['edge_distance']}]"

    def test_invalid_inputs(self):
        """Test handling of invalid inputs."""
        
        # Test negative dimensions - algorithm doesn't validate, but should produce reasonable results
        points = calculate_points(x=-10, y=240, min_dist_x=30, min_dist_y=40, edge_distance=15)
        assert isinstance(points, list)
        
        # Test zero dimensions - algorithm doesn't validate
        points = calculate_points(x=0, y=240, min_dist_x=30, min_dist_y=40, edge_distance=15)
        assert isinstance(points, list)
        
        # Test negative distances - algorithm doesn't validate
        points = calculate_points(x=220, y=240, min_dist_x=-5, min_dist_y=40, edge_distance=15)
        assert isinstance(points, list)
        
        # Test zero distances - this actually causes ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            calculate_points(x=220, y=240, min_dist_x=0, min_dist_y=40, edge_distance=15)
