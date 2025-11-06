# Testing Guide for Mattress Button Point Calculator

This document provides comprehensive guidelines for testing the mattress button point calculator web application.

## Overview

The testing strategy follows a multi-layered approach:

1. **Unit Tests** - Test individual functions and components in isolation
2. **Integration Tests** - Test complete workflows and API endpoints
3. **UI Tests** - Test frontend HTML template and user interface
4. **End-to-End Tests** - Test the complete application in Docker

## Test Structure

```
tests/
├── __init__.py                 # Test configuration
├── conftest.py                # Shared fixtures and configuration
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_calculate_points.py  # Core algorithm tests
│   └── test_api_endpoints.py   # Flask endpoint tests
├── integration/                 # Integration tests
│   ├── __init__.py
│   └── test_full_workflow.py   # End-to-end workflow tests
└── ui/                         # UI tests
    ├── __init__.py
    └── test_html_template.py     # HTML template tests
```

## Running Tests

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/     # Integration tests only
pytest tests/ui/              # UI tests only

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_calculate_points.py

# Run specific test method
pytest tests/unit/test_calculate_points.py::TestCalculatePoints::test_standard_rectangle
```

### Docker Testing

```bash
# Build and test Docker container
docker-compose up --build

# Run tests inside Docker
docker-compose exec app pytest
```

## Test Categories

### Unit Tests

**Purpose**: Test individual functions and components in isolation.

**Key Tests**:
- `test_calculate_points.py` - Core point calculation algorithm
  - Standard rectangles
  - Edge cases and boundary conditions
  - Point precision and validity
  - Performance with large inputs
  - Invalid input handling

- `test_api_endpoints.py` - Flask API endpoints
  - Valid request handling
  - Error responses and validation
  - Content type handling
  - Response headers and structure
  - Performance and concurrency

**Coverage Target**: 85% minimum

### Integration Tests

**Purpose**: Test complete workflows from user interaction to visualization.

**Key Tests**:
- End-to-end calculation workflow
- API response to canvas rendering pipeline
- Real-time parameter updates
- Data integrity across request cycles
- Performance of complete workflow
- Error propagation through system

### UI Tests

**Purpose**: Test frontend HTML template and user interface elements.

**Key Tests**:
- Required HTML elements presence
- Form validation and attributes
- Canvas element configuration
- JavaScript functionality integration
- Responsive design elements
- Accessibility features
- Performance optimization hints

## Test Data and Fixtures

### Standard Test Rectangles

```python
'standard': {'x': 220, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15}
'small': {'x': 50, 'y': 60, 'min_dist_x': 15, 'min_dist_y': 20, 'edge_distance': 10}
'large': {'x': 500, 'y': 800, 'min_dist_x': 50, 'min_dist_y': 60, 'edge_distance': 25}
'minimal': {'x': 20, 'y': 30, 'min_dist_x': 10, 'min_dist_y': 10, 'edge_distance': 5}
'square': {'x': 200, 'y': 200, 'min_dist_x': 25, 'min_dist_y': 25, 'edge_distance': 20}
```

### Invalid Input Cases

```python
'negative_dimensions': {'x': -10, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15}
'zero_dimensions': {'x': 0, 'y': 240, 'min_dist_x': 30, 'min_dist_y': 40, 'edge_distance': 15}
'negative_distances': {'x': 220, 'y': 240, 'min_dist_x': -5, 'min_dist_y': 40, 'edge_distance': 15}
```

## Continuous Integration

### GitHub Actions Workflow

The `.github/workflows/test.yml` file defines CI/CD pipeline:

#### Jobs

1. **Test Job**
   - Runs on Python 3.8, 3.9, 3.10, 3.11
   - Executes full test suite with coverage
   - Uploads results to Codecov

2. **Lint Job**
   - Code quality checks with flake8
   - Code formatting with black
   - Import sorting with isort

3. **Security Job**
   - Security vulnerability scan with bandit
   - Generates security reports

4. **Docker Test Job**
   - Builds Docker image
   - Tests container functionality
   - Validates API endpoints

#### Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` branch

## Test Environment Setup

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov pytest-flask black flake8 isort bandit
```

### Environment Variables

Tests can be configured with environment variables:

```bash
export FLASK_ENV=testing
export TESTING=true
```

## Performance Benchmarks

### Expected Performance

- **API Response Time**: < 1 second
- **Point Calculation**: < 0.5 seconds for large rectangles
- **Canvas Rendering**: < 0.1 seconds for typical point sets
- **Full Workflow**: < 1 second end-to-end

### Load Testing

For stress testing, use tools like:

```bash
# Using curl for basic load testing
for i in {1..100}; do
  curl -X POST -H "Content-Type: application/json" \
    -d '{"x":220,"y":240,"min_dist_x":30,"min_dist_y":40,"edge_distance":15}' \
    http://localhost:5000/calculate &
done
wait
```

## Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with detailed output
pytest -v -s tests/unit/test_calculate_points.py

# Run with Python debugger
pytest --pdb tests/unit/test_calculate_points.py

# Stop on first failure
pytest -x tests/

# Show local variables on failure
pytest -l tests/
```

### Common Issues and Solutions

1. **Import Errors**: Ensure all dependencies in `requirements.txt`
2. **Test Database Issues**: Clean test cache: `pytest --cache-clear`
3. **Port Conflicts**: Stop other services on port 5000
4. **Docker Issues**: Rebuild image: `docker-compose build --no-cache`

## Adding New Tests

### Unit Test Template

```python
def test_new_functionality(self, sample_rectangles):
    """Test description of what this test validates."""
    # Arrange
    test_data = sample_rectangles['standard']
    
    # Act
    result = function_to_test(**test_data)
    
    # Assert
    assert isinstance(result, expected_type)
    assert len(result) > 0
    # Add specific assertions for this functionality
```

### Integration Test Template

```python
def test_new_workflow(self, client, sample_rectangles):
    """Test complete workflow for new feature."""
    # Setup
    rect = sample_rectangles['standard']
    
    # Execute workflow
    response = client.post('/calculate',
                        data=json.dumps(rect),
                        content_type='application/json')
    
    # Verify results
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'points' in data
```

## Coverage Requirements

### Minimum Coverage

- **Overall**: 85%
- **Core Logic**: 95%
- **API Endpoints**: 90%

### Coverage Exclusions

The following can be excluded from coverage:
- Test files (`tests/`)
- Configuration files
- Debug code paths
- Exception handling for unlikely scenarios

## Release Testing

Before releasing:

1. **Full Test Suite**: `pytest --cov=app --cov-report=html`
2. **Integration Tests**: `pytest tests/integration/`
3. **Docker Tests**: `docker-compose up --build && docker-compose exec app pytest`
4. **Manual Testing**: Test UI in multiple browsers
5. **Performance Testing**: Validate against benchmarks
6. **Security Scan**: `bandit -r app.py`

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Flask testing guide](https://flask.palletsprojects.com/en/latest/testing/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Docker testing best practices](https://docs.docker.com/develop/dev-best-practices/)
