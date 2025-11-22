#!/usr/bin/env python3
"""
Backend API Testing for Pool Management Software (PoolPro)
Phase 2: Tests Job Management Workflow (Quotes, Jobs, Invoices)
"""

import requests
import json
import sys
from datetime import datetime, timezone, timedelta

# Backend URL from environment
BACKEND_URL = "https://swimsys.preview.emergentagent.com/api"

class PoolProAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.created_quote_id = None
        self.created_job_id = None
        self.created_invoice_id = None
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_data": response_data
        })
    
    def test_get_all_quotes(self):
        """Test GET /api/quotes - should return 4 seeded quotes"""
        try:
            response = self.session.get(f"{self.base_url}/quotes")
            
            if response.status_code == 200:
                quotes = response.json()
                if len(quotes) == 4:
                    # Verify quote structure
                    quote = quotes[0]
                    required_fields = ['id', 'customer_id', 'customer_name', 'status', 'items', 'subtotal', 'tax', 'total']
                    missing_fields = [field for field in required_fields if field not in quote]
                    
                    if not missing_fields:
                        # Check for various statuses
                        statuses = [q['status'] for q in quotes]
                        expected_statuses = ['pending', 'approved', 'declined']
                        has_expected_statuses = any(status in statuses for status in expected_statuses)
                        
                        if has_expected_statuses:
                            self.log_test("GET All Quotes", True, f"Retrieved {len(quotes)} quotes with correct structure and various statuses")
                            return True
                        else:
                            self.log_test("GET All Quotes", False, f"Missing expected statuses. Found: {statuses}")
                    else:
                        self.log_test("GET All Quotes", False, f"Missing fields in quote: {missing_fields}")
                else:
                    self.log_test("GET All Quotes", False, f"Expected 4 quotes, got {len(quotes)}")
            else:
                self.log_test("GET All Quotes", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Quotes", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_quote_by_id(self):
        """Test GET /api/quotes/{quote_id} with existing quote"""
        try:
            # Test with seeded quote "quote-001"
            response = self.session.get(f"{self.base_url}/quotes/quote-001")
            
            if response.status_code == 200:
                quote = response.json()
                if quote['id'] == 'quote-001' and quote['status'] == 'pending':
                    # Verify quote items and calculations
                    if 'items' in quote and len(quote['items']) > 0:
                        item = quote['items'][0]
                        if 'description' in item and 'unit_price' in item and 'total' in item:
                            # Verify total calculation
                            if quote['total'] == 1620.00 and quote['subtotal'] == 1500.00:
                                self.log_test("GET Quote by ID", True, "Retrieved quote with correct items and calculations")
                                return True
                            else:
                                self.log_test("GET Quote by ID", False, f"Incorrect calculations: total={quote['total']}, subtotal={quote['subtotal']}")
                        else:
                            self.log_test("GET Quote by ID", False, "Quote items missing required fields")
                    else:
                        self.log_test("GET Quote by ID", False, "Quote missing items data")
                else:
                    self.log_test("GET Quote by ID", False, f"Unexpected quote data: {quote.get('id', 'Unknown')}")
            else:
                self.log_test("GET Quote by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Quote by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_nonexistent_customer(self):
        """Test GET /api/customers/{customer_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/customers/nonexistent-id")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Customer", True, "Correctly returned 404 for non-existent customer")
                return True
            else:
                self.log_test("GET Non-existent Customer", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Customer", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_customer(self):
        """Test POST /api/customers - create new customer with pool"""
        try:
            new_customer = {
                "name": "Test Customer",
                "email": "test.customer@poolpro.com",
                "phone": "(555) 999-0000",
                "address": "123 Test Street, Austin, TX 78701",
                "status": "active",
                "account_balance": 0.0,
                "service_day": "Friday",
                "route_position": 1,
                "autopay": True,
                "pools": [
                    {
                        "name": "Test Pool",
                        "type": "In-Ground",
                        "color": "#3B82F6",
                        "gallons": 20000,
                        "equipment": ["Pump", "Filter"],
                        "last_service": "2025-01-16"
                    }
                ]
            }
            
            response = self.session.post(f"{self.base_url}/customers/", json=new_customer)
            
            if response.status_code == 200:
                customer = response.json()
                if customer['name'] == 'Test Customer' and customer['id'].startswith('cust-'):
                    # Store for later tests
                    self.created_customer_id = customer['id']
                    
                    # Verify pool was created with ID
                    if len(customer['pools']) == 1 and customer['pools'][0]['id'].startswith('pool-'):
                        self.log_test("POST Create Customer", True, f"Created customer {customer['id']} with pool {customer['pools'][0]['id']}")
                        return True
                    else:
                        self.log_test("POST Create Customer", False, "Pool not created correctly")
                else:
                    self.log_test("POST Create Customer", False, f"Unexpected customer data: {customer}")
            else:
                self.log_test("POST Create Customer", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Customer", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_customer(self):
        """Test PUT /api/customers/{customer_id} - update customer details"""
        try:
            # Use the created customer or fallback to cust-1
            customer_id = self.created_customer_id or "cust-1"
            
            update_data = {
                "name": "Updated Test Customer",
                "email": "updated.test@poolpro.com",
                "status": "paused",
                "autopay": False
            }
            
            response = self.session.put(f"{self.base_url}/customers/{customer_id}", json=update_data)
            
            if response.status_code == 200:
                customer = response.json()
                if (customer['name'] == 'Updated Test Customer' and 
                    customer['email'] == 'updated.test@poolpro.com' and
                    customer['status'] == 'paused' and
                    customer['autopay'] == False):
                    self.log_test("PUT Update Customer", True, f"Successfully updated customer {customer_id}")
                    return True
                else:
                    self.log_test("PUT Update Customer", False, f"Update not reflected correctly: {customer}")
            else:
                self.log_test("PUT Update Customer", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Customer", False, f"Exception: {str(e)}")
        
        return False
    
    def test_add_pool_to_customer(self):
        """Test POST /api/customers/{customer_id}/pools - add pool to existing customer"""
        try:
            # Use cust-1 (John Anderson) who has 1 pool initially
            customer_id = "cust-1"
            
            new_pool = {
                "name": "New Test Pool",
                "type": "Above-Ground",
                "color": "#10B981",
                "gallons": 15000,
                "equipment": ["Pump", "Filter", "Heater"],
                "last_service": "2025-01-16"
            }
            
            response = self.session.post(f"{self.base_url}/customers/{customer_id}/pools", json=new_pool)
            
            if response.status_code == 200:
                customer = response.json()
                # Should now have 2 pools
                if len(customer['pools']) == 2:
                    # Find the new pool
                    new_pool_found = False
                    for pool in customer['pools']:
                        if pool['name'] == 'New Test Pool' and pool['type'] == 'Above-Ground':
                            new_pool_found = True
                            break
                    
                    if new_pool_found:
                        self.log_test("POST Add Pool", True, f"Successfully added pool to customer {customer_id}")
                        return True
                    else:
                        self.log_test("POST Add Pool", False, "New pool not found in customer data")
                else:
                    self.log_test("POST Add Pool", False, f"Expected 2 pools, got {len(customer['pools'])}")
            else:
                self.log_test("POST Add Pool", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Add Pool", False, f"Exception: {str(e)}")
        
        return False
    
    def test_add_chemical_reading(self):
        """Test POST /api/customers/{customer_id}/pools/{pool_id}/readings - add chemical reading"""
        try:
            # Use cust-1 and pool-1
            customer_id = "cust-1"
            pool_id = "pool-1"
            
            new_reading = {
                "date": "2025-01-16",
                "fc": 3.5,
                "ph": 7.3,
                "ta": 118,
                "ch": 255,
                "cya": 52
            }
            
            response = self.session.post(f"{self.base_url}/customers/{customer_id}/pools/{pool_id}/readings", json=new_reading)
            
            if response.status_code == 200:
                customer = response.json()
                # Find the pool and check if reading was added
                for pool in customer['pools']:
                    if pool['id'] == pool_id:
                        # Check if last_service was updated
                        if pool['last_service'] == '2025-01-16':
                            # Check if reading was added
                            reading_found = False
                            for reading in pool['chem_readings']:
                                if (reading['date'] == '2025-01-16' and 
                                    reading['fc'] == 3.5 and 
                                    reading['ph'] == 7.3):
                                    reading_found = True
                                    break
                            
                            if reading_found:
                                self.log_test("POST Add Chemical Reading", True, f"Successfully added chemical reading to pool {pool_id}")
                                return True
                            else:
                                self.log_test("POST Add Chemical Reading", False, "Chemical reading not found in pool data")
                        else:
                            self.log_test("POST Add Chemical Reading", False, f"Last service not updated: {pool['last_service']}")
                        break
                else:
                    self.log_test("POST Add Chemical Reading", False, f"Pool {pool_id} not found")
            else:
                self.log_test("POST Add Chemical Reading", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Add Chemical Reading", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_chemical_readings(self):
        """Test GET /api/customers/{customer_id}/pools/{pool_id}/readings - get all readings"""
        try:
            # Use cust-1 and pool-1
            customer_id = "cust-1"
            pool_id = "pool-1"
            
            response = self.session.get(f"{self.base_url}/customers/{customer_id}/pools/{pool_id}/readings")
            
            if response.status_code == 200:
                readings = response.json()
                if len(readings) >= 3:  # Should have at least 3 seeded readings
                    # Verify reading structure
                    reading = readings[0]
                    required_fields = ['date', 'fc', 'ph', 'ta', 'ch', 'cya']
                    missing_fields = [field for field in required_fields if field not in reading]
                    
                    if not missing_fields:
                        self.log_test("GET Chemical Readings", True, f"Retrieved {len(readings)} chemical readings with correct structure")
                        return True
                    else:
                        self.log_test("GET Chemical Readings", False, f"Missing fields in reading: {missing_fields}")
                else:
                    self.log_test("GET Chemical Readings", False, f"Expected at least 3 readings, got {len(readings)}")
            else:
                self.log_test("GET Chemical Readings", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Chemical Readings", False, f"Exception: {str(e)}")
        
        return False
    
    def test_invalid_pool_id(self):
        """Test chemical reading with invalid pool ID"""
        try:
            customer_id = "cust-1"
            invalid_pool_id = "nonexistent-pool"
            
            new_reading = {
                "date": "2025-01-16",
                "fc": 3.0,
                "ph": 7.4,
                "ta": 120,
                "ch": 250,
                "cya": 50
            }
            
            response = self.session.post(f"{self.base_url}/customers/{customer_id}/pools/{invalid_pool_id}/readings", json=new_reading)
            
            if response.status_code == 404:
                self.log_test("Invalid Pool ID Test", True, "Correctly returned 404 for invalid pool ID")
                return True
            else:
                self.log_test("Invalid Pool ID Test", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Invalid Pool ID Test", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_customer(self):
        """Test DELETE /api/customers/{customer_id} - delete customer"""
        try:
            # Only delete if we created a test customer
            if self.created_customer_id:
                response = self.session.delete(f"{self.base_url}/customers/{self.created_customer_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "deleted successfully" in result.get('message', ''):
                        # Verify customer is actually deleted
                        verify_response = self.session.get(f"{self.base_url}/customers/{self.created_customer_id}")
                        if verify_response.status_code == 404:
                            self.log_test("DELETE Customer", True, f"Successfully deleted customer {self.created_customer_id}")
                            return True
                        else:
                            self.log_test("DELETE Customer", False, "Customer still exists after deletion")
                    else:
                        self.log_test("DELETE Customer", False, f"Unexpected response: {result}")
                else:
                    self.log_test("DELETE Customer", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Customer", True, "Skipped - no test customer was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Customer", False, f"Exception: {str(e)}")
        
        return False
    
    def test_customer_status_validation(self):
        """Test customer status validation (active, paused, inactive)"""
        try:
            # Test valid status values
            valid_statuses = ["active", "paused", "inactive"]
            
            for status in valid_statuses:
                test_customer = {
                    "name": f"Status Test Customer {status}",
                    "email": f"status.{status}@poolpro.com",
                    "phone": "(555) 888-0000",
                    "address": "123 Status Street, Austin, TX 78701",
                    "status": status,
                    "service_day": "Monday",
                    "pools": []
                }
                
                response = self.session.post(f"{self.base_url}/customers/", json=test_customer)
                
                if response.status_code == 200:
                    customer = response.json()
                    if customer['status'] == status:
                        # Clean up - delete the test customer
                        self.session.delete(f"{self.base_url}/customers/{customer['id']}")
                        continue
                    else:
                        self.log_test("Customer Status Validation", False, f"Status {status} not set correctly")
                        return False
                else:
                    self.log_test("Customer Status Validation", False, f"Failed to create customer with status {status}: {response.status_code}")
                    return False
            
            self.log_test("Customer Status Validation", True, "All valid status values accepted")
            return True
                
        except Exception as e:
            self.log_test("Customer Status Validation", False, f"Exception: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print(f"🧪 Starting PoolPro Backend API Tests")
        print(f"🔗 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_get_all_customers,
            self.test_get_customer_by_id,
            self.test_get_nonexistent_customer,
            self.test_create_customer,
            self.test_update_customer,
            self.test_add_pool_to_customer,
            self.test_add_chemical_reading,
            self.test_get_chemical_readings,
            self.test_invalid_pool_id,
            self.test_customer_status_validation,
            self.test_delete_customer
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()  # Add spacing between tests
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Backend APIs are working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Check the issues above.")
            return False

def main():
    """Main test execution"""
    tester = PoolProAPITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()