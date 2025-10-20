"""
Unit tests for the Cloud Resume Challenge Azure Functions API
Tests the visitor counter functionality and CosmosDB operations
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import azure.functions as func
from azure.cosmos import exceptions

# Import our function app
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))
from function_app import visitor_counter, CosmosDBManager, health_check, visitor_stats


class TestCosmosDBManager:
    """Test cases for CosmosDB operations"""
    
    @patch.dict(os.environ, {
        'COSMOS_DB_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_DB_KEY': 'test-key',
        'COSMOS_DB_DATABASE': 'TestDB',
        'COSMOS_DB_CONTAINER': 'TestContainer'
    })
    @patch('function_app.CosmosClient')
    def test_cosmos_manager_initialization_success(self, mock_cosmos_client):
        """Test successful CosmosDB manager initialization"""
        # Mock the client and its methods
        mock_client_instance = Mock()
        mock_cosmos_client.return_value = mock_client_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Initialize manager
        manager = CosmosDBManager()
        
        # Assertions
        assert manager.cosmos_endpoint == 'https://test.documents.azure.com:443/'
        assert manager.cosmos_key == 'test-key'
        assert manager.database_name == 'TestDB'
        assert manager.container_name == 'TestContainer'
        mock_cosmos_client.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_cosmos_manager_initialization_missing_env_vars(self):
        """Test CosmosDB manager initialization with missing environment variables"""
        with pytest.raises(ValueError, match="CosmosDB connection details not found"):
            CosmosDBManager()

    @patch.dict(os.environ, {
        'COSMOS_DB_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_DB_KEY': 'test-key'
    })
    @patch('function_app.CosmosClient')
    def test_get_visitor_count_existing_counter(self, mock_cosmos_client):
        """Test retrieving existing visitor count"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_cosmos_client.return_value = mock_client_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Mock query result
        mock_container.query_items.return_value = [{'id': 'visitor-counter', 'count': 42}]
        
        manager = CosmosDBManager()
        count = manager.get_visitor_count()
        
        assert count == 42
        mock_container.query_items.assert_called_once()

    @patch.dict(os.environ, {
        'COSMOS_DB_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_DB_KEY': 'test-key'
    })
    @patch('function_app.CosmosClient')
    def test_get_visitor_count_no_existing_counter(self, mock_cosmos_client):
        """Test retrieving visitor count when counter doesn't exist"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_cosmos_client.return_value = mock_client_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Mock empty query result
        mock_container.query_items.return_value = []
        mock_container.create_item.return_value = None
        
        manager = CosmosDBManager()
        count = manager.get_visitor_count()
        
        assert count == 1  # Should initialize to 1
        mock_container.create_item.assert_called_once()

    @patch.dict(os.environ, {
        'COSMOS_DB_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_DB_KEY': 'test-key'
    })
    @patch('function_app.CosmosClient')
    def test_increment_visitor_count_existing_counter(self, mock_cosmos_client):
        """Test incrementing existing visitor count"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_cosmos_client.return_value = mock_client_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Mock existing counter
        mock_container.read_item.return_value = {'id': 'visitor-counter', 'count': 10}
        mock_container.upsert_item.return_value = None
        
        manager = CosmosDBManager()
        new_count = manager.increment_visitor_count()
        
        assert new_count == 11
        mock_container.upsert_item.assert_called_once()

    @patch.dict(os.environ, {
        'COSMOS_DB_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_DB_KEY': 'test-key'
    })
    @patch('function_app.CosmosClient')
    def test_increment_visitor_count_new_counter(self, mock_cosmos_client):
        """Test incrementing visitor count when counter doesn't exist"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_cosmos_client.return_value = mock_client_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Mock missing counter
        mock_container.read_item.side_effect = exceptions.CosmosResourceNotFoundError(
            message="Not found",
            response=Mock()
        )
        mock_container.upsert_item.return_value = None
        
        manager = CosmosDBManager()
        new_count = manager.increment_visitor_count()
        
        assert new_count == 1
        mock_container.upsert_item.assert_called_once()


class TestVisitorCounterFunction:
    """Test cases for the visitor counter Azure Function"""
    
    def test_visitor_counter_options_request(self):
        """Test CORS preflight OPTIONS request"""
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "OPTIONS"
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 200
        headers = dict(response.headers)
        assert "Access-Control-Allow-Origin" in headers
        assert headers["Access-Control-Allow-Origin"] == "*"
        assert "Access-Control-Allow-Methods" in headers

    @patch('function_app.cosmos_manager')
    def test_visitor_counter_get_request(self, mock_cosmos_manager):
        """Test GET request to visitor counter"""
        # Setup mock
        mock_cosmos_manager.get_visitor_count.return_value = 25
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "GET"
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 200
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["count"] == 25
        assert response_data["status"] == "success"
        assert response_data["method"] == "GET"
        
        mock_cosmos_manager.get_visitor_count.assert_called_once()

    @patch('function_app.cosmos_manager')
    def test_visitor_counter_post_request(self, mock_cosmos_manager):
        """Test POST request to visitor counter"""
        # Setup mock
        mock_cosmos_manager.increment_visitor_count.return_value = 26
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "POST"
        req.get_json.return_value = {"action": "increment"}
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 200
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["count"] == 26
        assert response_data["status"] == "success"
        assert response_data["method"] == "POST"
        assert response_data["action"] == "increment"
        
        mock_cosmos_manager.increment_visitor_count.assert_called_once()

    @patch('function_app.cosmos_manager')
    def test_visitor_counter_post_request_invalid_json(self, mock_cosmos_manager):
        """Test POST request with invalid JSON body"""
        # Setup mock
        mock_cosmos_manager.increment_visitor_count.return_value = 27
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "POST"
        req.get_json.side_effect = ValueError("Invalid JSON")
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 200
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["count"] == 27
        assert response_data["status"] == "success"
        assert "warning" in response_data
        
        mock_cosmos_manager.increment_visitor_count.assert_called_once()

    def test_visitor_counter_unsupported_method(self):
        """Test unsupported HTTP method"""
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "DELETE"
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 405
        
        response_data = json.loads(response.get_body().decode())
        assert "error" in response_data
        assert response_data["error"] == "Method not allowed"

    @patch('function_app.cosmos_manager')
    def test_visitor_counter_cosmos_error(self, mock_cosmos_manager):
        """Test handling of CosmosDB errors"""
        # Setup mock to raise exception
        mock_cosmos_manager.get_visitor_count.side_effect = Exception("CosmosDB error")
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "GET"
        
        # Call function
        response = visitor_counter(req)
        
        # Assertions
        assert response.status_code == 500
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["status"] == "error"
        assert "error" in response_data


class TestHealthCheckFunction:
    """Test cases for the health check function"""
    
    @patch('function_app.cosmos_manager')
    def test_health_check_success(self, mock_cosmos_manager):
        """Test successful health check"""
        # Setup mock
        mock_cosmos_manager.get_visitor_count.return_value = 10
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        
        # Call function
        response = health_check(req)
        
        # Assertions
        assert response.status_code == 200
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["status"] == "healthy"
        assert response_data["services"]["cosmosdb"] == "connected"
        assert response_data["services"]["function_app"] == "running"

    @patch('function_app.cosmos_manager')
    def test_health_check_cosmos_error(self, mock_cosmos_manager):
        """Test health check with CosmosDB error"""
        # Setup mock to raise exception
        mock_cosmos_manager.get_visitor_count.side_effect = Exception("CosmosDB connection failed")
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        
        # Call function
        response = health_check(req)
        
        # Assertions
        assert response.status_code == 503
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["status"] == "unhealthy"
        assert response_data["services"]["cosmosdb"] == "error"
        assert "error" in response_data


class TestVisitorStatsFunction:
    """Test cases for the visitor stats function"""
    
    @patch('function_app.cosmos_manager')
    def test_visitor_stats_success(self, mock_cosmos_manager):
        """Test successful visitor stats retrieval"""
        # Setup mock
        mock_stats = {
            "totalVisitors": 100,
            "lastUpdated": "2024-01-01T12:00:00Z",
            "status": "active"
        }
        mock_cosmos_manager.get_visitor_stats.return_value = mock_stats
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        
        # Call function
        response = visitor_stats(req)
        
        # Assertions
        assert response.status_code == 200
        
        response_data = json.loads(response.get_body().decode())
        assert response_data["totalVisitors"] == 100
        assert response_data["status"] == "active"

    @patch('function_app.cosmos_manager')
    def test_visitor_stats_error(self, mock_cosmos_manager):
        """Test visitor stats with error"""
        # Setup mock to raise exception
        mock_cosmos_manager.get_visitor_stats.side_effect = Exception("Stats error")
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        
        # Call function
        response = visitor_stats(req)
        
        # Assertions
        assert response.status_code == 500
        
        response_data = json.loads(response.get_body().decode())
        assert "error" in response_data


# Integration test fixtures
@pytest.fixture
def mock_cosmos_client():
    """Fixture for mocking CosmosClient"""
    with patch('function_app.CosmosClient') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        mock_database = Mock()
        mock_container = Mock()
        mock_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        yield {
            'client': mock_instance,
            'database': mock_database,
            'container': mock_container
        }


@pytest.fixture
def sample_http_request():
    """Fixture for creating sample HTTP requests"""
    def _create_request(method="GET", body=None, headers=None):
        req = Mock(spec=func.HttpRequest)
        req.method = method
        req.get_json.return_value = body
        req.headers = headers or {}
        return req
    
    return _create_request


# Performance and load testing helpers
class TestPerformance:
    """Performance-related tests"""
    
    @patch('function_app.cosmos_manager')
    def test_visitor_counter_response_time(self, mock_cosmos_manager):
        """Test that visitor counter responds within acceptable time"""
        import time
        
        # Setup mock
        mock_cosmos_manager.get_visitor_count.return_value = 1
        
        # Create mock request
        req = Mock(spec=func.HttpRequest)
        req.method = "GET"
        
        # Measure response time
        start_time = time.time()
        response = visitor_counter(req)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assertions
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])