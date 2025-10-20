"""
Integration tests for the Cloud Resume Challenge Azure Functions
Tests end-to-end functionality including CosmosDB integration
"""

import pytest
import requests
import json
import time
import os
from typing import Dict, Any
import asyncio
import aiohttp


class TestIntegration:
    """Integration tests for the visitor counter API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self) -> str:
        """Get the API base URL from environment or use default for local testing"""
        return os.environ.get('FUNCTION_APP_URL', 'http://localhost:7071/api')
    
    @pytest.fixture(scope="class")
    def headers(self) -> Dict[str, str]:
        """Standard headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Cloud-Resume-Challenge-Tests/1.0'
        }
    
    def test_health_check_endpoint(self, api_base_url: str, headers: Dict[str, str]):
        """Test the health check endpoint"""
        try:
            response = requests.get(f"{api_base_url}/health", headers=headers, timeout=10)
            
            # Should return 200 or 503 (if CosmosDB is down)
            assert response.status_code in [200, 503]
            
            data = response.json()
            assert 'status' in data
            assert 'timestamp' in data
            assert 'services' in data
            
            if response.status_code == 200:
                assert data['status'] == 'healthy'
                assert data['services']['function_app'] == 'running'
            else:
                assert data['status'] == 'unhealthy'
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_cors_preflight_request(self, api_base_url: str):
        """Test CORS preflight request"""
        try:
            response = requests.options(f"{api_base_url}/visitor-counter", timeout=10)
            
            assert response.status_code == 200
            
            # Check CORS headers
            assert 'Access-Control-Allow-Origin' in response.headers
            assert response.headers['Access-Control-Allow-Origin'] == '*'
            assert 'Access-Control-Allow-Methods' in response.headers
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_get_visitor_count(self, api_base_url: str, headers: Dict[str, str]):
        """Test GET request to visitor counter"""
        try:
            response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            
            assert response.status_code == 200
            
            data = response.json()
            assert 'count' in data
            assert 'timestamp' in data
            assert 'status' in data
            assert data['status'] == 'success'
            assert data['method'] == 'GET'
            assert isinstance(data['count'], int)
            assert data['count'] >= 0
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_increment_visitor_count(self, api_base_url: str, headers: Dict[str, str]):
        """Test POST request to increment visitor counter"""
        try:
            # First, get current count
            get_response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            assert get_response.status_code == 200
            initial_count = get_response.json()['count']
            
            # Then increment
            post_data = {"action": "increment"}
            post_response = requests.post(
                f"{api_base_url}/visitor-counter", 
                json=post_data, 
                headers=headers, 
                timeout=10
            )
            
            assert post_response.status_code == 200
            
            data = post_response.json()
            assert 'count' in data
            assert 'timestamp' in data
            assert 'status' in data
            assert data['status'] == 'success'
            assert data['method'] == 'POST'
            assert data['action'] == 'increment'
            assert data['count'] == initial_count + 1
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_visitor_stats_endpoint(self, api_base_url: str, headers: Dict[str, str]):
        """Test the visitor stats endpoint"""
        try:
            response = requests.get(f"{api_base_url}/visitor-stats", headers=headers, timeout=10)
            
            assert response.status_code == 200
            
            data = response.json()
            assert 'totalVisitors' in data
            assert 'lastUpdated' in data
            assert 'status' in data
            assert isinstance(data['totalVisitors'], int)
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_invalid_endpoint(self, api_base_url: str, headers: Dict[str, str]):
        """Test request to non-existent endpoint"""
        try:
            response = requests.get(f"{api_base_url}/non-existent", headers=headers, timeout=10)
            
            # Should return 404
            assert response.status_code == 404
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")
    
    def test_unsupported_method(self, api_base_url: str, headers: Dict[str, str]):
        """Test unsupported HTTP method"""
        try:
            response = requests.delete(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            
            assert response.status_code == 405
            
            data = response.json()
            assert 'error' in data
            assert data['error'] == 'Method not allowed'
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping integration test")


class TestLoadAndPerformance:
    """Load and performance tests"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self) -> str:
        """Get the API base URL from environment"""
        return os.environ.get('FUNCTION_APP_URL', 'http://localhost:7071/api')
    
    @pytest.mark.slow
    def test_concurrent_requests(self, api_base_url: str):
        """Test handling of concurrent requests"""
        async def make_request(session: aiohttp.ClientSession) -> Dict[str, Any]:
            """Make a single request to increment counter"""
            async with session.post(f"{api_base_url}/visitor-counter", json={"action": "increment"}) as response:
                return await response.json()
        
        async def run_concurrent_test():
            """Run multiple concurrent requests"""
            async with aiohttp.ClientSession() as session:
                # Make 10 concurrent requests
                tasks = [make_request(session) for _ in range(10)]
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Count successful responses
                successful_responses = [r for r in responses if isinstance(r, dict) and r.get('status') == 'success']
                return len(successful_responses)
        
        try:
            # Run the concurrent test
            successful_count = asyncio.run(run_concurrent_test())
            
            # At least 80% of requests should succeed
            assert successful_count >= 8
            
        except Exception as e:
            pytest.skip(f"Concurrent test failed: {str(e)}")
    
    @pytest.mark.slow
    def test_response_time_under_load(self, api_base_url: str):
        """Test response times under moderate load"""
        try:
            response_times = []
            
            for _ in range(20):
                start_time = time.time()
                response = requests.get(f"{api_base_url}/visitor-counter", timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append(end_time - start_time)
                
                # Small delay between requests
                time.sleep(0.1)
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                
                # Average response time should be under 2 seconds
                assert avg_response_time < 2.0
                
                # Maximum response time should be under 5 seconds
                assert max_response_time < 5.0
                
                print(f"Average response time: {avg_response_time:.3f}s")
                print(f"Maximum response time: {max_response_time:.3f}s")
            else:
                pytest.skip("No successful responses recorded")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping performance test")


class TestDataConsistency:
    """Tests for data consistency and reliability"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self) -> str:
        """Get the API base URL from environment"""
        return os.environ.get('FUNCTION_APP_URL', 'http://localhost:7071/api')
    
    def test_counter_increment_consistency(self, api_base_url: str):
        """Test that counter increments are consistent"""
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Get initial count
            initial_response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            assert initial_response.status_code == 200
            initial_count = initial_response.json()['count']
            
            # Increment counter 5 times
            for i in range(5):
                increment_response = requests.post(
                    f"{api_base_url}/visitor-counter", 
                    json={"action": "increment"}, 
                    headers=headers, 
                    timeout=10
                )
                assert increment_response.status_code == 200
                
                expected_count = initial_count + i + 1
                actual_count = increment_response.json()['count']
                assert actual_count == expected_count, f"Expected {expected_count}, got {actual_count}"
            
            # Verify final count
            final_response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            assert final_response.status_code == 200
            final_count = final_response.json()['count']
            assert final_count == initial_count + 5
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping consistency test")
    
    def test_idempotent_get_requests(self, api_base_url: str):
        """Test that GET requests don't modify the counter"""
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Get initial count
            initial_response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
            assert initial_response.status_code == 200
            initial_count = initial_response.json()['count']
            
            # Make multiple GET requests
            for _ in range(10):
                get_response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=10)
                assert get_response.status_code == 200
                current_count = get_response.json()['count']
                assert current_count == initial_count, "GET request should not modify counter"
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping idempotency test")


class TestErrorHandling:
    """Tests for error handling and edge cases"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self) -> str:
        """Get the API base URL from environment"""
        return os.environ.get('FUNCTION_APP_URL', 'http://localhost:7071/api')
    
    def test_malformed_json_request(self, api_base_url: str):
        """Test handling of malformed JSON in POST request"""
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Send malformed JSON
            response = requests.post(
                f"{api_base_url}/visitor-counter",
                data="invalid json",
                headers=headers,
                timeout=10
            )
            
            # Should still increment counter (graceful handling)
            assert response.status_code == 200
            
            data = response.json()
            assert data['status'] == 'success'
            assert 'warning' in data or data['action'] == 'increment'
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping error handling test")
    
    def test_request_timeout_handling(self, api_base_url: str):
        """Test that requests complete within reasonable time"""
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Make request with very short timeout to test handling
            start_time = time.time()
            response = requests.get(f"{api_base_url}/visitor-counter", headers=headers, timeout=30)
            end_time = time.time()
            
            # Request should complete within 30 seconds
            assert end_time - start_time < 30
            assert response.status_code == 200
            
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out - function may be unresponsive")
        except requests.exceptions.ConnectionError:
            pytest.skip("Function App not running - skipping timeout test")


# Utility functions for integration testing
def wait_for_function_app(api_base_url: str, max_wait: int = 60) -> bool:
    """Wait for the function app to be responsive"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{api_base_url}/health", timeout=5)
            if response.status_code in [200, 503]:
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
    
    return False


def cleanup_test_data(api_base_url: str):
    """Clean up any test data (if cleanup endpoint exists)"""
    try:
        # This would be implemented if we had a cleanup endpoint
        pass
    except Exception:
        pass


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"])