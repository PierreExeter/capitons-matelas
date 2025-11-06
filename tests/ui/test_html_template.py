import pytest
from flask import Flask
from app import app


class TestHTMLTemplate:
    """Test suite for HTML template rendering."""

    def test_index_page_contains_required_elements(self, client):
        """Test that index page contains all required HTML elements."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        # Check for essential HTML elements
        html_content = response.data.decode('utf-8').lower()
        
        # Check for form elements
        assert 'form' in html_content
        assert 'input' in html_content
        assert 'button' in html_content
        assert 'label' in html_content
        
        # Check for required input fields
        assert 'x' in html_content  # Rectangle width
        assert 'y' in html_content  # Rectangle height
        assert 'dist_x' in html_content  # Distance X
        assert 'dist_y' in html_content  # Distance Y
        assert 'edge' in html_content  # Edge distance
        
        # Check for canvas element
        assert 'canvas' in html_content
        assert 'id="canvas"' in html_content
        
        # Check for JavaScript
        assert 'script' in html_content
        assert 'fetch' in html_content  # API calls
        assert 'canvas.getcontext' in html_content  # Canvas drawing

    def test_page_has_proper_structure(self, client):
        """Test that page has proper HTML5 structure."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for proper HTML structure
        assert '<!doctype html>' in html_content
        assert '<html' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content
        
        # Check for meta tags
        assert 'charset' in html_content
        assert 'viewport' in html_content
        
        # Check for title
        assert '<title>' in html_content
        assert 'calculateur' in html_content

    def test_form_has_correct_attributes(self, client):
        """Test that form elements have correct attributes."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8')
        
        # Check for form id
        assert 'id=' in html_content.lower()
        
        # Check for input types
        assert 'type="number"' in html_content.lower()
        assert 'min=' in html_content.lower()
        assert 'step=' in html_content.lower()
        
        # Check for proper validation attributes
        assert 'required' in html_content.lower()

    def test_canvas_has_correct_attributes(self, client):
        """Test that canvas element has correct attributes."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for canvas attributes
        assert 'width=' in html_content
        assert 'height=' in html_content
        assert 'id="canvas"' in html_content

    def test_javascript_functionality_present(self, client):
        """Test that required JavaScript functionality is present."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for key JavaScript functions
        assert 'function' in html_content
        assert 'addeventlistener' in html_content
        assert 'visualizepoints' in html_content
        assert 'updateinfo' in html_content
        assert 'updatevisualization' in html_content
        
        # Check for event handling
        assert 'input' in html_content
        assert 'click' in html_content
        
        # Check for API integration
        assert '/calculate' in html_content
        assert 'json' in html_content

    def test_responsive_design_elements(self, client):
        """Test that responsive design elements are present."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for responsive design elements
        assert 'viewport' in html_content
        assert 'width=device-width' in html_content
        
        # Check for CSS styling
        assert 'style' in html_content
        assert 'margin' in html_content
        assert 'padding' in html_content
        assert 'display' in html_content

    def test_error_handling_elements(self, client):
        """Test that error handling elements are present."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for error display elements
        assert 'error' in html_content or 'alert' in html_content
        
        # Check for validation feedback
        assert 'console.error' in html_content or 'console.log' in html_content

    def test_accessibility_elements(self, client):
        """Test that accessibility elements are present."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for accessibility features
        assert 'label' in html_content
        assert 'for=' in html_content  # Label-for attribute
        
        # Check for semantic HTML
        assert 'main' in html_content or 'section' in html_content
        assert 'header' in html_content

    def test_performance_optimization_hints(self, client):
        """Test that performance optimization hints are present."""
        response = client.get('/')
        
        assert response.status_code == 200
        
        html_content = response.data.decode('utf-8').lower()
        
        # Check for performance optimizations
        assert 'requestanimationframe' in html_content or 'settimeout' in html_content
        assert 'clearrect' in html_content  # Canvas optimization
        
        # Check for efficient DOM manipulation
        assert 'addeventlistener' in html_content
