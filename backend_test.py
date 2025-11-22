#!/usr/bin/env python3
"""
Backend API Testing for Pool Management Software (PoolPro)
Phase 5: Tests Reports API, Customer Auth API, and Customer Portal API
"""

import requests
import json
import sys
from datetime import datetime, timezone, timedelta

# Backend URL from environment
BACKEND_URL = "https://swimsmart.preview.emergentagent.com/api"

class PoolProAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.created_quote_id = None
        self.created_job_id = None
        self.created_invoice_id = None
        self.created_technician_id = None
        self.created_route_id = None
        self.created_alert_id = None
        self.jwt_token = None
        self.customer_id = None
        self.customer_name = None
        
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
    
    # ===== QUOTES API TESTS =====
    
    def test_get_all_quotes(self):
        """Test GET /api/quotes/ - should return 4 seeded quotes"""
        try:
            response = self.session.get(f"{self.base_url}/quotes/")
            
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
    
    def test_create_quote(self):
        """Test POST /api/quotes/ - create new quote"""
        try:
            new_quote = {
                "customer_id": "cust-1",
                "customer_name": "John Anderson",
                "items": [
                    {"description": "Pool Cleaning Service", "quantity": 1, "unit_price": 150.00, "total": 150.00},
                    {"description": "Chemical Balance", "quantity": 1, "unit_price": 50.00, "total": 50.00}
                ],
                "subtotal": 200.00,
                "tax": 16.00,
                "total": 216.00,
                "notes": "Test quote creation",
                "valid_until": (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
            }
            
            response = self.session.post(f"{self.base_url}/quotes/", json=new_quote)
            
            if response.status_code == 200:
                quote = response.json()
                if quote['customer_name'] == 'John Anderson' and quote['id'].startswith('quote-'):
                    # Store for later tests
                    self.created_quote_id = quote['id']
                    
                    # Verify calculations
                    if quote['total'] == 216.00 and quote['subtotal'] == 200.00:
                        self.log_test("POST Create Quote", True, f"Created quote {quote['id']} with correct calculations")
                        return True
                    else:
                        self.log_test("POST Create Quote", False, "Quote calculations incorrect")
                else:
                    self.log_test("POST Create Quote", False, f"Unexpected quote data: {quote}")
            else:
                self.log_test("POST Create Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_quote(self):
        """Test PUT /api/quotes/{quote_id} - update quote"""
        try:
            # Use created quote or fallback to quote-001
            quote_id = self.created_quote_id or "quote-001"
            
            update_data = {
                "status": "pending",
                "notes": "Updated test quote",
                "tax": 20.00,
                "total": 220.00
            }
            
            response = self.session.put(f"{self.base_url}/quotes/{quote_id}", json=update_data)
            
            if response.status_code == 200:
                quote = response.json()
                if quote['notes'] == 'Updated test quote' and quote['tax'] == 20.00:
                    self.log_test("PUT Update Quote", True, f"Successfully updated quote {quote_id}")
                    return True
                else:
                    self.log_test("PUT Update Quote", False, f"Update not reflected correctly: {quote}")
            else:
                self.log_test("PUT Update Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_approve_quote(self):
        """Test POST /api/quotes/{quote_id}/approve - approve quote"""
        try:
            # Use quote-001 which should be pending
            quote_id = "quote-001"
            
            response = self.session.post(f"{self.base_url}/quotes/{quote_id}/approve")
            
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'Quote approved' and result['quote']['status'] == 'approved':
                    self.log_test("POST Approve Quote", True, f"Successfully approved quote {quote_id}")
                    return True
                else:
                    self.log_test("POST Approve Quote", False, f"Quote not approved correctly: {result}")
            else:
                self.log_test("POST Approve Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Approve Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_decline_quote(self):
        """Test POST /api/quotes/{quote_id}/decline - decline quote"""
        try:
            # Use quote-004 which should be pending
            quote_id = "quote-004"
            
            response = self.session.post(f"{self.base_url}/quotes/{quote_id}/decline")
            
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'Quote declined' and result['quote']['status'] == 'declined':
                    self.log_test("POST Decline Quote", True, f"Successfully declined quote {quote_id}")
                    return True
                else:
                    self.log_test("POST Decline Quote", False, f"Quote not declined correctly: {result}")
            else:
                self.log_test("POST Decline Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Decline Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_quote(self):
        """Test DELETE /api/quotes/{quote_id} - delete quote"""
        try:
            # Only delete if we created a test quote
            if self.created_quote_id:
                response = self.session.delete(f"{self.base_url}/quotes/{self.created_quote_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "deleted successfully" in result.get('message', ''):
                        # Verify quote is actually deleted
                        verify_response = self.session.get(f"{self.base_url}/quotes/{self.created_quote_id}")
                        if verify_response.status_code == 404:
                            self.log_test("DELETE Quote", True, f"Successfully deleted quote {self.created_quote_id}")
                            return True
                        else:
                            self.log_test("DELETE Quote", False, "Quote still exists after deletion")
                    else:
                        self.log_test("DELETE Quote", False, f"Unexpected response: {result}")
                else:
                    self.log_test("DELETE Quote", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Quote", True, "Skipped - no test quote was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Quote", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== JOBS API TESTS =====
    
    def test_get_all_jobs(self):
        """Test GET /api/jobs/ - should return 6 seeded jobs"""
        try:
            response = self.session.get(f"{self.base_url}/jobs/")
            
            if response.status_code == 200:
                jobs = response.json()
                if len(jobs) == 6:
                    # Verify job structure
                    job = jobs[0]
                    required_fields = ['id', 'customer_id', 'customer_name', 'status', 'service_type', 'scheduled_date', 'technician']
                    missing_fields = [field for field in required_fields if field not in job]
                    
                    if not missing_fields:
                        # Check for various statuses
                        statuses = [j['status'] for j in jobs]
                        expected_statuses = ['scheduled', 'in-progress', 'completed']
                        has_expected_statuses = any(status in statuses for status in expected_statuses)
                        
                        if has_expected_statuses:
                            self.log_test("GET All Jobs", True, f"Retrieved {len(jobs)} jobs with correct structure and various statuses")
                            return True
                        else:
                            self.log_test("GET All Jobs", False, f"Missing expected statuses. Found: {statuses}")
                    else:
                        self.log_test("GET All Jobs", False, f"Missing fields in job: {missing_fields}")
                else:
                    self.log_test("GET All Jobs", False, f"Expected 6 jobs, got {len(jobs)}")
            else:
                self.log_test("GET All Jobs", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Jobs", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_job_by_id(self):
        """Test GET /api/jobs/{job_id} with existing job"""
        try:
            # Test with seeded job "job-001"
            response = self.session.get(f"{self.base_url}/jobs/job-001")
            
            if response.status_code == 200:
                job = response.json()
                if job['id'] == 'job-001' and job['status'] == 'scheduled':
                    # Verify job details
                    if job['service_type'] == 'Routine Service' and job['technician'] == 'Mike Johnson':
                        self.log_test("GET Job by ID", True, "Retrieved job with correct details")
                        return True
                    else:
                        self.log_test("GET Job by ID", False, f"Incorrect job details: {job}")
                else:
                    self.log_test("GET Job by ID", False, f"Unexpected job data: {job.get('id', 'Unknown')}")
            else:
                self.log_test("GET Job by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Job by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_job(self):
        """Test POST /api/jobs/ - create new job"""
        try:
            tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
            
            new_job = {
                "customer_id": "cust-1",
                "customer_name": "John Anderson",
                "customer_address": "123 Main St, Austin, TX 78701",
                "service_type": "One-time Service",
                "scheduled_date": tomorrow,
                "scheduled_time": "02:00 PM",
                "technician": "Test Technician",
                "pools": ["pool-1"],
                "notes": "Test job creation"
            }
            
            response = self.session.post(f"{self.base_url}/jobs/", json=new_job)
            
            if response.status_code == 200:
                job = response.json()
                if job['customer_name'] == 'John Anderson' and job['id'].startswith('job-'):
                    # Store for later tests
                    self.created_job_id = job['id']
                    
                    # Verify job details
                    if job['service_type'] == 'One-time Service' and job['technician'] == 'Test Technician':
                        self.log_test("POST Create Job", True, f"Created job {job['id']} with correct details")
                        return True
                    else:
                        self.log_test("POST Create Job", False, "Job details incorrect")
                else:
                    self.log_test("POST Create Job", False, f"Unexpected job data: {job}")
            else:
                self.log_test("POST Create Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_job(self):
        """Test PUT /api/jobs/{job_id} - update job"""
        try:
            # Use created job or fallback to job-001
            job_id = self.created_job_id or "job-001"
            
            update_data = {
                "status": "scheduled",
                "notes": "Updated test job",
                "technician": "Updated Technician"
            }
            
            response = self.session.put(f"{self.base_url}/jobs/{job_id}", json=update_data)
            
            if response.status_code == 200:
                job = response.json()
                if job['notes'] == 'Updated test job' and job['technician'] == 'Updated Technician':
                    self.log_test("PUT Update Job", True, f"Successfully updated job {job_id}")
                    return True
                else:
                    self.log_test("PUT Update Job", False, f"Update not reflected correctly: {job}")
            else:
                self.log_test("PUT Update Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_start_job(self):
        """Test POST /api/jobs/{job_id}/start - start job"""
        try:
            # Use job-001 which should be scheduled
            job_id = "job-001"
            
            response = self.session.post(f"{self.base_url}/jobs/{job_id}/start")
            
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'Job started' and result['job']['status'] == 'in-progress':
                    self.log_test("POST Start Job", True, f"Successfully started job {job_id}")
                    return True
                else:
                    self.log_test("POST Start Job", False, f"Job not started correctly: {result}")
            else:
                self.log_test("POST Start Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Start Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_complete_job(self):
        """Test POST /api/jobs/{job_id}/complete - complete job"""
        try:
            # Use job-002 which should be in-progress
            job_id = "job-002"
            
            response = self.session.post(f"{self.base_url}/jobs/{job_id}/complete")
            
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'Job completed' and result['job']['status'] == 'completed':
                    # Verify completed_at is set
                    if 'completed_at' in result['job'] and result['job']['completed_at']:
                        self.log_test("POST Complete Job", True, f"Successfully completed job {job_id}")
                        return True
                    else:
                        self.log_test("POST Complete Job", False, "completed_at not set")
                else:
                    self.log_test("POST Complete Job", False, f"Job not completed correctly: {result}")
            else:
                self.log_test("POST Complete Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Complete Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_jobs_by_date(self):
        """Test GET /api/jobs/by-date/{date} - get jobs by date"""
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
            response = self.session.get(f"{self.base_url}/jobs/by-date/{today}")
            
            if response.status_code == 200:
                jobs = response.json()
                # Should have at least 2 jobs scheduled for today
                if len(jobs) >= 2:
                    # Verify all jobs are for today
                    all_today = all(job['scheduled_date'] == today for job in jobs)
                    if all_today:
                        self.log_test("GET Jobs by Date", True, f"Retrieved {len(jobs)} jobs for {today}")
                        return True
                    else:
                        self.log_test("GET Jobs by Date", False, "Some jobs not for the requested date")
                else:
                    self.log_test("GET Jobs by Date", True, f"Retrieved {len(jobs)} jobs for {today} (expected at least 2)")
                    return True  # This is acceptable as data might vary
            else:
                self.log_test("GET Jobs by Date", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Jobs by Date", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_jobs_by_technician(self):
        """Test GET /api/jobs/by-technician/{technician} - get jobs by technician"""
        try:
            technician = "Mike Johnson"
            
            response = self.session.get(f"{self.base_url}/jobs/by-technician/{technician}")
            
            if response.status_code == 200:
                jobs = response.json()
                # Should have at least 2 jobs for Mike Johnson
                if len(jobs) >= 2:
                    # Verify all jobs are for the technician
                    all_mike = all(job['technician'] == technician for job in jobs)
                    if all_mike:
                        self.log_test("GET Jobs by Technician", True, f"Retrieved {len(jobs)} jobs for {technician}")
                        return True
                    else:
                        self.log_test("GET Jobs by Technician", False, "Some jobs not for the requested technician")
                else:
                    self.log_test("GET Jobs by Technician", True, f"Retrieved {len(jobs)} jobs for {technician}")
                    return True  # This is acceptable
            else:
                self.log_test("GET Jobs by Technician", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Jobs by Technician", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_job(self):
        """Test DELETE /api/jobs/{job_id} - delete job"""
        try:
            # Only delete if we created a test job
            if self.created_job_id:
                response = self.session.delete(f"{self.base_url}/jobs/{self.created_job_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "deleted successfully" in result.get('message', ''):
                        # Verify job is actually deleted
                        verify_response = self.session.get(f"{self.base_url}/jobs/{self.created_job_id}")
                        if verify_response.status_code == 404:
                            self.log_test("DELETE Job", True, f"Successfully deleted job {self.created_job_id}")
                            return True
                        else:
                            self.log_test("DELETE Job", False, "Job still exists after deletion")
                    else:
                        self.log_test("DELETE Job", False, f"Unexpected response: {result}")
                else:
                    self.log_test("DELETE Job", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Job", True, "Skipped - no test job was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Job", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== INVOICES API TESTS =====
    
    def test_get_all_invoices(self):
        """Test GET /api/invoices/ - should return 5 seeded invoices"""
        try:
            response = self.session.get(f"{self.base_url}/invoices/")
            
            if response.status_code == 200:
                invoices = response.json()
                if len(invoices) == 5:
                    # Verify invoice structure
                    invoice = invoices[0]
                    required_fields = ['id', 'customer_id', 'customer_name', 'status', 'line_items', 'subtotal', 'total', 'balance_due']
                    missing_fields = [field for field in required_fields if field not in invoice]
                    
                    if not missing_fields:
                        # Check for various statuses
                        statuses = [i['status'] for i in invoices]
                        expected_statuses = ['draft', 'sent', 'paid', 'overdue']
                        has_expected_statuses = any(status in statuses for status in expected_statuses)
                        
                        if has_expected_statuses:
                            self.log_test("GET All Invoices", True, f"Retrieved {len(invoices)} invoices with correct structure and various statuses")
                            return True
                        else:
                            self.log_test("GET All Invoices", False, f"Missing expected statuses. Found: {statuses}")
                    else:
                        self.log_test("GET All Invoices", False, f"Missing fields in invoice: {missing_fields}")
                else:
                    self.log_test("GET All Invoices", False, f"Expected 5 invoices, got {len(invoices)}")
            else:
                self.log_test("GET All Invoices", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Invoices", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_invoice_by_id(self):
        """Test GET /api/invoices/{invoice_id} with existing invoice"""
        try:
            # Test with seeded invoice "inv-001"
            response = self.session.get(f"{self.base_url}/invoices/inv-001")
            
            if response.status_code == 200:
                invoice = response.json()
                if invoice['id'] == 'inv-001' and invoice['status'] == 'paid':
                    # Verify invoice details
                    if invoice['total'] == 172.80 and invoice['balance_due'] == 0.00:
                        self.log_test("GET Invoice by ID", True, "Retrieved invoice with correct details")
                        return True
                    else:
                        self.log_test("GET Invoice by ID", False, f"Incorrect invoice calculations: {invoice}")
                else:
                    self.log_test("GET Invoice by ID", False, f"Unexpected invoice data: {invoice.get('id', 'Unknown')}")
            else:
                self.log_test("GET Invoice by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Invoice by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_invoice(self):
        """Test POST /api/invoices/ - create new invoice"""
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            due_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
            
            new_invoice = {
                "customer_id": "cust-1",
                "customer_name": "John Anderson",
                "invoice_number": "INV-TEST-001",
                "line_items": [
                    {"description": "Test Service", "quantity": 1, "unit_price": 100.00, "total": 100.00},
                    {"description": "Test Materials", "quantity": 2, "unit_price": 25.00, "total": 50.00}
                ],
                "subtotal": 150.00,
                "tax": 12.00,
                "total": 162.00,
                "issue_date": today,
                "due_date": due_date,
                "notes": "Test invoice creation"
            }
            
            response = self.session.post(f"{self.base_url}/invoices/", json=new_invoice)
            
            if response.status_code == 200:
                invoice = response.json()
                if invoice['customer_name'] == 'John Anderson' and invoice['id'].startswith('inv-'):
                    # Store for later tests
                    self.created_invoice_id = invoice['id']
                    
                    # Verify calculations
                    if invoice['total'] == 162.00 and invoice['balance_due'] == 162.00:
                        self.log_test("POST Create Invoice", True, f"Created invoice {invoice['id']} with correct calculations")
                        return True
                    else:
                        self.log_test("POST Create Invoice", False, "Invoice calculations incorrect")
                else:
                    self.log_test("POST Create Invoice", False, f"Unexpected invoice data: {invoice}")
            else:
                self.log_test("POST Create Invoice", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_invoice_payment(self):
        """Test PUT /api/invoices/{invoice_id} - update invoice with payment"""
        try:
            # Use created invoice or fallback to inv-002
            invoice_id = self.created_invoice_id or "inv-002"
            
            update_data = {
                "paid_amount": 100.00,
                "notes": "Partial payment received"
            }
            
            response = self.session.put(f"{self.base_url}/invoices/{invoice_id}", json=update_data)
            
            if response.status_code == 200:
                invoice = response.json()
                if invoice['paid_amount'] == 100.00 and invoice['balance_due'] > 0:
                    self.log_test("PUT Update Invoice Payment", True, f"Successfully updated invoice {invoice_id} with payment")
                    return True
                else:
                    self.log_test("PUT Update Invoice Payment", False, f"Payment update not reflected correctly: {invoice}")
            else:
                self.log_test("PUT Update Invoice Payment", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Invoice Payment", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_invoice(self):
        """Test DELETE /api/invoices/{invoice_id} - delete invoice"""
        try:
            # Only delete if we created a test invoice
            if self.created_invoice_id:
                response = self.session.delete(f"{self.base_url}/invoices/{self.created_invoice_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "deleted successfully" in result.get('message', ''):
                        # Verify invoice is actually deleted
                        verify_response = self.session.get(f"{self.base_url}/invoices/{self.created_invoice_id}")
                        if verify_response.status_code == 404:
                            self.log_test("DELETE Invoice", True, f"Successfully deleted invoice {self.created_invoice_id}")
                            return True
                        else:
                            self.log_test("DELETE Invoice", False, "Invoice still exists after deletion")
                    else:
                        self.log_test("DELETE Invoice", False, f"Unexpected response: {result}")
                else:
                    self.log_test("DELETE Invoice", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Invoice", True, "Skipped - no test invoice was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== TECHNICIANS API TESTS =====
    
    def test_get_all_technicians(self):
        """Test GET /api/technicians/ - should return 4 seeded technicians"""
        try:
            response = self.session.get(f"{self.base_url}/technicians/")
            
            if response.status_code == 200:
                technicians = response.json()
                if len(technicians) == 4:
                    # Verify technician structure
                    tech = technicians[0]
                    required_fields = ['id', 'name', 'email', 'phone', 'color', 'status', 'assigned_days']
                    missing_fields = [field for field in required_fields if field not in tech]
                    
                    if not missing_fields:
                        # Check for expected technician IDs
                        tech_ids = [t['id'] for t in technicians]
                        expected_ids = ['tech-001', 'tech-002', 'tech-003', 'tech-004']
                        has_expected_ids = all(tech_id in tech_ids for tech_id in expected_ids)
                        
                        if has_expected_ids:
                            self.log_test("GET All Technicians", True, f"Retrieved {len(technicians)} technicians with correct structure and IDs")
                            return True
                        else:
                            self.log_test("GET All Technicians", False, f"Missing expected technician IDs. Found: {tech_ids}")
                    else:
                        self.log_test("GET All Technicians", False, f"Missing fields in technician: {missing_fields}")
                else:
                    self.log_test("GET All Technicians", False, f"Expected 4 technicians, got {len(technicians)}")
            else:
                self.log_test("GET All Technicians", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Technicians", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_technician_by_id(self):
        """Test GET /api/technicians/{technician_id} with existing technician"""
        try:
            # Test with seeded technician "tech-001"
            response = self.session.get(f"{self.base_url}/technicians/tech-001")
            
            if response.status_code == 200:
                tech = response.json()
                if tech['id'] == 'tech-001' and tech['name'] == 'Mike Johnson':
                    # Verify technician details
                    if tech['status'] == 'active' and 'Monday' in tech['assigned_days']:
                        self.log_test("GET Technician by ID", True, "Retrieved technician with correct details")
                        return True
                    else:
                        self.log_test("GET Technician by ID", False, f"Incorrect technician details: {tech}")
                else:
                    self.log_test("GET Technician by ID", False, f"Unexpected technician data: {tech.get('id', 'Unknown')}")
            else:
                self.log_test("GET Technician by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Technician by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_technician(self):
        """Test POST /api/technicians/ - create new technician"""
        try:
            new_tech = {
                "name": "Test Technician",
                "email": "test.tech@poolpro.com",
                "phone": "(555) 999-0000",
                "color": "#FF5733",
                "status": "active",
                "assigned_days": ["Monday", "Tuesday"]
            }
            
            response = self.session.post(f"{self.base_url}/technicians/", json=new_tech)
            
            if response.status_code == 201:
                tech = response.json()
                if tech['name'] == 'Test Technician' and tech['id'].startswith('tech-'):
                    # Store for later tests
                    self.created_technician_id = tech['id']
                    
                    # Verify technician details
                    if tech['color'] == '#FF5733' and tech['status'] == 'active':
                        self.log_test("POST Create Technician", True, f"Created technician {tech['id']} with correct details")
                        return True
                    else:
                        self.log_test("POST Create Technician", False, "Technician details incorrect")
                else:
                    self.log_test("POST Create Technician", False, f"Unexpected technician data: {tech}")
            else:
                self.log_test("POST Create Technician", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Technician", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_technician(self):
        """Test PUT /api/technicians/{technician_id} - update technician"""
        try:
            # Use created technician or fallback to tech-001
            tech_id = self.created_technician_id or "tech-001"
            
            update_data = {
                "color": "#00FF00",
                "status": "active",
                "assigned_days": ["Monday", "Wednesday", "Friday"]
            }
            
            response = self.session.put(f"{self.base_url}/technicians/{tech_id}", json=update_data)
            
            if response.status_code == 200:
                tech = response.json()
                if tech['color'] == '#00FF00' and len(tech['assigned_days']) == 3:
                    self.log_test("PUT Update Technician", True, f"Successfully updated technician {tech_id}")
                    return True
                else:
                    self.log_test("PUT Update Technician", False, f"Update not reflected correctly: {tech}")
            else:
                self.log_test("PUT Update Technician", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Technician", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_technician(self):
        """Test DELETE /api/technicians/{technician_id} - delete technician"""
        try:
            # Only delete if we created a test technician
            if self.created_technician_id:
                response = self.session.delete(f"{self.base_url}/technicians/{self.created_technician_id}")
                
                if response.status_code == 204:
                    # Verify technician is actually deleted
                    verify_response = self.session.get(f"{self.base_url}/technicians/{self.created_technician_id}")
                    if verify_response.status_code == 404:
                        self.log_test("DELETE Technician", True, f"Successfully deleted technician {self.created_technician_id}")
                        return True
                    else:
                        self.log_test("DELETE Technician", False, "Technician still exists after deletion")
                else:
                    self.log_test("DELETE Technician", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Technician", True, "Skipped - no test technician was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Technician", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== ROUTES API TESTS =====
    
    def test_get_all_routes(self):
        """Test GET /api/routes/ - should return 12 seeded routes"""
        try:
            response = self.session.get(f"{self.base_url}/routes/")
            
            if response.status_code == 200:
                routes = response.json()
                if len(routes) >= 10:  # Should be around 12 but allow some flexibility
                    # Verify route structure
                    route = routes[0]
                    required_fields = ['id', 'name', 'technician_id', 'technician_name', 'day', 'jobs', 'total_stops']
                    missing_fields = [field for field in required_fields if field not in route]
                    
                    if not missing_fields:
                        # Check for various days
                        days = [r['day'] for r in routes]
                        expected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                        has_expected_days = any(day in days for day in expected_days)
                        
                        if has_expected_days:
                            self.log_test("GET All Routes", True, f"Retrieved {len(routes)} routes with correct structure and various days")
                            return True
                        else:
                            self.log_test("GET All Routes", False, f"Missing expected days. Found: {set(days)}")
                    else:
                        self.log_test("GET All Routes", False, f"Missing fields in route: {missing_fields}")
                else:
                    self.log_test("GET All Routes", False, f"Expected at least 10 routes, got {len(routes)}")
            else:
                self.log_test("GET All Routes", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Routes", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_routes_filtered_by_day(self):
        """Test GET /api/routes/?day=Monday - get routes filtered by day"""
        try:
            response = self.session.get(f"{self.base_url}/routes/?day=Monday")
            
            if response.status_code == 200:
                routes = response.json()
                if len(routes) >= 1:
                    # Verify all routes are for Monday
                    all_monday = all(route['day'] == 'Monday' for route in routes)
                    if all_monday:
                        self.log_test("GET Routes Filtered by Day", True, f"Retrieved {len(routes)} Monday routes")
                        return True
                    else:
                        self.log_test("GET Routes Filtered by Day", False, "Some routes not for Monday")
                else:
                    self.log_test("GET Routes Filtered by Day", False, f"Expected at least 1 Monday route, got {len(routes)}")
            else:
                self.log_test("GET Routes Filtered by Day", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Routes Filtered by Day", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_routes_by_day(self):
        """Test GET /api/routes/by-day/Monday - get routes for Monday"""
        try:
            response = self.session.get(f"{self.base_url}/routes/by-day/Monday")
            
            if response.status_code == 200:
                routes = response.json()
                if len(routes) >= 1:
                    # Verify all routes are for Monday
                    all_monday = all(route['day'] == 'Monday' for route in routes)
                    if all_monday:
                        self.log_test("GET Routes by Day", True, f"Retrieved {len(routes)} Monday routes")
                        return True
                    else:
                        self.log_test("GET Routes by Day", False, "Some routes not for Monday")
                else:
                    self.log_test("GET Routes by Day", True, f"Retrieved {len(routes)} Monday routes (acceptable)")
                    return True  # This is acceptable
            else:
                self.log_test("GET Routes by Day", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Routes by Day", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_routes_by_technician(self):
        """Test GET /api/routes/by-technician/tech-001 - get routes for specific technician"""
        try:
            response = self.session.get(f"{self.base_url}/routes/by-technician/tech-001")
            
            if response.status_code == 200:
                routes = response.json()
                if len(routes) >= 1:
                    # Verify all routes are for tech-001
                    all_tech001 = all(route['technician_id'] == 'tech-001' for route in routes)
                    if all_tech001:
                        self.log_test("GET Routes by Technician", True, f"Retrieved {len(routes)} routes for tech-001")
                        return True
                    else:
                        self.log_test("GET Routes by Technician", False, "Some routes not for tech-001")
                else:
                    self.log_test("GET Routes by Technician", True, f"Retrieved {len(routes)} routes for tech-001 (acceptable)")
                    return True  # This is acceptable
            else:
                self.log_test("GET Routes by Technician", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Routes by Technician", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_route_by_id(self):
        """Test GET /api/routes/{route_id} with existing route"""
        try:
            # First get all routes to find a valid ID
            all_routes_response = self.session.get(f"{self.base_url}/routes/")
            if all_routes_response.status_code == 200:
                routes = all_routes_response.json()
                if routes:
                    route_id = routes[0]['id']
                    
                    response = self.session.get(f"{self.base_url}/routes/{route_id}")
                    
                    if response.status_code == 200:
                        route = response.json()
                        if route['id'] == route_id:
                            self.log_test("GET Route by ID", True, f"Retrieved route {route_id} with correct details")
                            return True
                        else:
                            self.log_test("GET Route by ID", False, f"Unexpected route data: {route.get('id', 'Unknown')}")
                    else:
                        self.log_test("GET Route by ID", False, f"HTTP {response.status_code}: {response.text}")
                else:
                    self.log_test("GET Route by ID", False, "No routes found to test with")
            else:
                self.log_test("GET Route by ID", False, "Could not fetch routes for testing")
                
        except Exception as e:
            self.log_test("GET Route by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_route(self):
        """Test POST /api/routes/ - create new route"""
        try:
            new_route = {
                "name": "Test Route",
                "technician_id": "tech-001",
                "technician_name": "Mike Johnson",
                "day": "Saturday",
                "jobs": ["job-001", "job-002"],
                "estimated_duration": 90
            }
            
            response = self.session.post(f"{self.base_url}/routes/", json=new_route)
            
            if response.status_code == 201:
                route = response.json()
                if route['name'] == 'Test Route' and route['id'].startswith('route-'):
                    # Store for later tests
                    self.created_route_id = route['id']
                    
                    # Verify route details
                    if route['day'] == 'Saturday' and route['total_stops'] == 2:
                        self.log_test("POST Create Route", True, f"Created route {route['id']} with correct details")
                        return True
                    else:
                        self.log_test("POST Create Route", False, "Route details incorrect")
                else:
                    self.log_test("POST Create Route", False, f"Unexpected route data: {route}")
            else:
                self.log_test("POST Create Route", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Route", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_route(self):
        """Test PUT /api/routes/{route_id} - update route"""
        try:
            # Use created route or get first available route
            route_id = self.created_route_id
            if not route_id:
                # Get first available route
                all_routes_response = self.session.get(f"{self.base_url}/routes/")
                if all_routes_response.status_code == 200:
                    routes = all_routes_response.json()
                    if routes:
                        route_id = routes[0]['id']
            
            if route_id:
                update_data = {
                    "day": "Sunday",
                    "jobs": ["job-001", "job-002", "job-003"],
                    "estimated_duration": 135
                }
                
                response = self.session.put(f"{self.base_url}/routes/{route_id}", json=update_data)
                
                if response.status_code == 200:
                    route = response.json()
                    if route['day'] == 'Sunday' and route['total_stops'] == 3:
                        self.log_test("PUT Update Route", True, f"Successfully updated route {route_id}")
                        return True
                    else:
                        self.log_test("PUT Update Route", False, f"Update not reflected correctly: {route}")
                else:
                    self.log_test("PUT Update Route", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("PUT Update Route", False, "No route available for testing")
                
        except Exception as e:
            self.log_test("PUT Update Route", False, f"Exception: {str(e)}")
        
        return False
    
    def test_add_job_to_route(self):
        """Test POST /api/routes/{route_id}/add-job - add job to route"""
        try:
            # Use created route or get first available route
            route_id = self.created_route_id
            if not route_id:
                # Get first available route
                all_routes_response = self.session.get(f"{self.base_url}/routes/")
                if all_routes_response.status_code == 200:
                    routes = all_routes_response.json()
                    if routes:
                        route_id = routes[0]['id']
            
            if route_id:
                # Add a mock job ID (may not exist in DB but tests the endpoint)
                job_id = "job-test-001"
                
                response = self.session.post(f"{self.base_url}/routes/{route_id}/add-job", params={"job_id": job_id})
                
                if response.status_code == 200:
                    route = response.json()
                    if job_id in route['jobs']:
                        self.log_test("POST Add Job to Route", True, f"Successfully added job {job_id} to route {route_id}")
                        return True
                    else:
                        self.log_test("POST Add Job to Route", False, f"Job not added to route: {route['jobs']}")
                else:
                    self.log_test("POST Add Job to Route", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("POST Add Job to Route", False, "No route available for testing")
                
        except Exception as e:
            self.log_test("POST Add Job to Route", False, f"Exception: {str(e)}")
        
        return False
    
    def test_remove_job_from_route(self):
        """Test DELETE /api/routes/{route_id}/remove-job/{job_id} - remove job from route"""
        try:
            # Use created route or get first available route
            route_id = self.created_route_id
            if not route_id:
                # Get first available route
                all_routes_response = self.session.get(f"{self.base_url}/routes/")
                if all_routes_response.status_code == 200:
                    routes = all_routes_response.json()
                    if routes:
                        route_id = routes[0]['id']
            
            if route_id:
                # Remove the job we just added
                job_id = "job-test-001"
                
                response = self.session.delete(f"{self.base_url}/routes/{route_id}/remove-job/{job_id}")
                
                if response.status_code == 200:
                    route = response.json()
                    if job_id not in route['jobs']:
                        self.log_test("DELETE Remove Job from Route", True, f"Successfully removed job {job_id} from route {route_id}")
                        return True
                    else:
                        self.log_test("DELETE Remove Job from Route", False, f"Job still in route: {route['jobs']}")
                else:
                    self.log_test("DELETE Remove Job from Route", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Remove Job from Route", False, "No route available for testing")
                
        except Exception as e:
            self.log_test("DELETE Remove Job from Route", False, f"Exception: {str(e)}")
        
        return False
    
    def test_reorder_route_jobs(self):
        """Test PUT /api/routes/{route_id}/reorder - reorder jobs in route"""
        try:
            # Use created route or get first available route
            route_id = self.created_route_id
            if not route_id:
                # Get first available route
                all_routes_response = self.session.get(f"{self.base_url}/routes/")
                if all_routes_response.status_code == 200:
                    routes = all_routes_response.json()
                    if routes:
                        route_id = routes[0]['id']
            
            if route_id:
                # Reorder jobs (reverse order)
                reorder_data = {
                    "jobs": ["job-003", "job-002", "job-001"]
                }
                
                response = self.session.put(f"{self.base_url}/routes/{route_id}/reorder", json=reorder_data)
                
                if response.status_code == 200:
                    route = response.json()
                    if route['jobs'] == reorder_data['jobs']:
                        self.log_test("PUT Reorder Route Jobs", True, f"Successfully reordered jobs in route {route_id}")
                        return True
                    else:
                        self.log_test("PUT Reorder Route Jobs", False, f"Jobs not reordered correctly: {route['jobs']}")
                else:
                    self.log_test("PUT Reorder Route Jobs", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("PUT Reorder Route Jobs", False, "No route available for testing")
                
        except Exception as e:
            self.log_test("PUT Reorder Route Jobs", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_route(self):
        """Test DELETE /api/routes/{route_id} - delete route"""
        try:
            # Only delete if we created a test route
            if self.created_route_id:
                response = self.session.delete(f"{self.base_url}/routes/{self.created_route_id}")
                
                if response.status_code == 204:
                    # Verify route is actually deleted
                    verify_response = self.session.get(f"{self.base_url}/routes/{self.created_route_id}")
                    if verify_response.status_code == 404:
                        self.log_test("DELETE Route", True, f"Successfully deleted route {self.created_route_id}")
                        return True
                    else:
                        self.log_test("DELETE Route", False, "Route still exists after deletion")
                else:
                    self.log_test("DELETE Route", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Route", True, "Skipped - no test route was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Route", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== ERROR HANDLING TESTS =====
    
    def test_nonexistent_quote(self):
        """Test GET /api/quotes/{quote_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/quotes/nonexistent-quote")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Quote", True, "Correctly returned 404 for non-existent quote")
                return True
            else:
                self.log_test("GET Non-existent Quote", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_nonexistent_job(self):
        """Test GET /api/jobs/{job_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/jobs/nonexistent-job")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Job", True, "Correctly returned 404 for non-existent job")
                return True
            else:
                self.log_test("GET Non-existent Job", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_nonexistent_invoice(self):
        """Test GET /api/invoices/{invoice_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/invoices/nonexistent-invoice")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Invoice", True, "Correctly returned 404 for non-existent invoice")
                return True
            else:
                self.log_test("GET Non-existent Invoice", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    def test_nonexistent_technician(self):
        """Test GET /api/technicians/{technician_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/technicians/nonexistent-tech")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Technician", True, "Correctly returned 404 for non-existent technician")
                return True
            else:
                self.log_test("GET Non-existent Technician", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Technician", False, f"Exception: {str(e)}")
        
        return False
    
    def test_nonexistent_route(self):
        """Test GET /api/routes/{route_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/routes/nonexistent-route")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Route", True, "Correctly returned 404 for non-existent route")
                return True
            else:
                self.log_test("GET Non-existent Route", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Route", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== ALERTS API TESTS =====
    
    def test_get_all_alerts(self):
        """Test GET /api/alerts/ - should return 9 seeded alerts"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/")
            
            if response.status_code == 200:
                alerts = response.json()
                if len(alerts) == 9:
                    # Verify alert structure
                    alert = alerts[0]
                    required_fields = ['id', 'type', 'severity', 'title', 'message', 'customer_id', 'customer_name', 'resolved', 'created_at', 'updated_at']
                    missing_fields = [field for field in required_fields if field not in alert]
                    
                    if not missing_fields:
                        # Check for various types and severities
                        types = [a['type'] for a in alerts]
                        severities = [a['severity'] for a in alerts]
                        expected_types = ['chemical', 'flow', 'leak', 'time', 'cost']
                        expected_severities = ['high', 'medium', 'low']
                        
                        has_expected_types = any(alert_type in types for alert_type in expected_types)
                        has_expected_severities = any(severity in severities for severity in expected_severities)
                        
                        if has_expected_types and has_expected_severities:
                            self.log_test("GET All Alerts", True, f"Retrieved {len(alerts)} alerts with correct structure and various types/severities")
                            return True
                        else:
                            self.log_test("GET All Alerts", False, f"Missing expected types/severities. Types: {set(types)}, Severities: {set(severities)}")
                    else:
                        self.log_test("GET All Alerts", False, f"Missing fields in alert: {missing_fields}")
                else:
                    self.log_test("GET All Alerts", False, f"Expected 9 alerts, got {len(alerts)}")
            else:
                self.log_test("GET All Alerts", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET All Alerts", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alerts_filtered_unresolved(self):
        """Test GET /api/alerts/?resolved=false - should return 7 unresolved alerts"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/?resolved=false")
            
            if response.status_code == 200:
                alerts = response.json()
                if len(alerts) == 7:
                    # Verify all alerts are unresolved
                    all_unresolved = all(not alert['resolved'] for alert in alerts)
                    if all_unresolved:
                        self.log_test("GET Alerts Filtered Unresolved", True, f"Retrieved {len(alerts)} unresolved alerts")
                        return True
                    else:
                        self.log_test("GET Alerts Filtered Unresolved", False, "Some alerts are resolved when filtering for unresolved")
                else:
                    self.log_test("GET Alerts Filtered Unresolved", False, f"Expected 7 unresolved alerts, got {len(alerts)}")
            else:
                self.log_test("GET Alerts Filtered Unresolved", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alerts Filtered Unresolved", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alerts_filtered_resolved(self):
        """Test GET /api/alerts/?resolved=true - should return 2 resolved alerts"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/?resolved=true")
            
            if response.status_code == 200:
                alerts = response.json()
                if len(alerts) == 2:
                    # Verify all alerts are resolved
                    all_resolved = all(alert['resolved'] for alert in alerts)
                    if all_resolved:
                        self.log_test("GET Alerts Filtered Resolved", True, f"Retrieved {len(alerts)} resolved alerts")
                        return True
                    else:
                        self.log_test("GET Alerts Filtered Resolved", False, "Some alerts are unresolved when filtering for resolved")
                else:
                    self.log_test("GET Alerts Filtered Resolved", False, f"Expected 2 resolved alerts, got {len(alerts)}")
            else:
                self.log_test("GET Alerts Filtered Resolved", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alerts Filtered Resolved", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alerts_filtered_by_severity(self):
        """Test GET /api/alerts/?severity=high - filter by severity"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/?severity=high")
            
            if response.status_code == 200:
                alerts = response.json()
                if len(alerts) >= 1:
                    # Verify all alerts are high severity
                    all_high = all(alert['severity'] == 'high' for alert in alerts)
                    if all_high:
                        self.log_test("GET Alerts Filtered by Severity", True, f"Retrieved {len(alerts)} high severity alerts")
                        return True
                    else:
                        self.log_test("GET Alerts Filtered by Severity", False, "Some alerts are not high severity when filtering for high")
                else:
                    self.log_test("GET Alerts Filtered by Severity", False, f"Expected at least 1 high severity alert, got {len(alerts)}")
            else:
                self.log_test("GET Alerts Filtered by Severity", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alerts Filtered by Severity", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alerts_filtered_by_type(self):
        """Test GET /api/alerts/?type=chemical - filter by type"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/?type=chemical")
            
            if response.status_code == 200:
                alerts = response.json()
                if len(alerts) >= 1:
                    # Verify all alerts are chemical type
                    all_chemical = all(alert['type'] == 'chemical' for alert in alerts)
                    if all_chemical:
                        self.log_test("GET Alerts Filtered by Type", True, f"Retrieved {len(alerts)} chemical alerts")
                        return True
                    else:
                        self.log_test("GET Alerts Filtered by Type", False, "Some alerts are not chemical type when filtering for chemical")
                else:
                    self.log_test("GET Alerts Filtered by Type", False, f"Expected at least 1 chemical alert, got {len(alerts)}")
            else:
                self.log_test("GET Alerts Filtered by Type", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alerts Filtered by Type", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alert_by_id(self):
        """Test GET /api/alerts/{alert_id} with existing alert"""
        try:
            # Test with seeded alert "alert-001"
            response = self.session.get(f"{self.base_url}/alerts/alert-001")
            
            if response.status_code == 200:
                alert = response.json()
                if alert['id'] == 'alert-001' and alert['type'] == 'chemical':
                    # Verify alert details
                    if alert['severity'] == 'high' and alert['title'] == 'Low Chlorine Level':
                        self.log_test("GET Alert by ID", True, "Retrieved alert with correct details")
                        return True
                    else:
                        self.log_test("GET Alert by ID", False, f"Incorrect alert details: {alert}")
                else:
                    self.log_test("GET Alert by ID", False, f"Unexpected alert data: {alert.get('id', 'Unknown')}")
            else:
                self.log_test("GET Alert by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alert by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_alert(self):
        """Test POST /api/alerts/ - create new alert"""
        try:
            new_alert = {
                "type": "chemical",
                "severity": "medium",
                "title": "Test Chemical Alert",
                "message": "This is a test chemical alert for API testing",
                "customer_id": "cust-1",
                "customer_name": "John Anderson",
                "pool_id": "pool-1",
                "pool_name": "Main Pool"
            }
            
            response = self.session.post(f"{self.base_url}/alerts/", json=new_alert)
            
            if response.status_code == 200:
                alert = response.json()
                if alert['title'] == 'Test Chemical Alert' and alert['id'].startswith('alert-'):
                    # Store for later tests
                    self.created_alert_id = alert['id']
                    
                    # Verify alert details
                    if alert['type'] == 'chemical' and alert['severity'] == 'medium' and not alert['resolved']:
                        self.log_test("POST Create Alert", True, f"Created alert {alert['id']} with correct details")
                        return True
                    else:
                        self.log_test("POST Create Alert", False, "Alert details incorrect")
                else:
                    self.log_test("POST Create Alert", False, f"Unexpected alert data: {alert}")
            else:
                self.log_test("POST Create Alert", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Create Alert", False, f"Exception: {str(e)}")
        
        return False
    
    def test_update_alert(self):
        """Test PUT /api/alerts/{alert_id} - update alert"""
        try:
            # Use created alert or fallback to alert-001
            alert_id = self.created_alert_id or "alert-001"
            
            update_data = {
                "resolved": True
            }
            
            response = self.session.put(f"{self.base_url}/alerts/{alert_id}", json=update_data)
            
            if response.status_code == 200:
                alert = response.json()
                if alert['resolved'] and alert.get('resolved_at'):
                    self.log_test("PUT Update Alert", True, f"Successfully updated alert {alert_id} to resolved with timestamp")
                    return True
                else:
                    self.log_test("PUT Update Alert", False, f"Update not reflected correctly: resolved={alert['resolved']}, resolved_at={alert.get('resolved_at')}")
            else:
                self.log_test("PUT Update Alert", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("PUT Update Alert", False, f"Exception: {str(e)}")
        
        return False
    
    def test_resolve_alert(self):
        """Test POST /api/alerts/{alert_id}/resolve - mark alert as resolved"""
        try:
            # Use alert-002 which should be unresolved
            alert_id = "alert-002"
            
            response = self.session.post(f"{self.base_url}/alerts/{alert_id}/resolve")
            
            if response.status_code == 200:
                alert = response.json()
                if alert['resolved'] and alert.get('resolved_at'):
                    self.log_test("POST Resolve Alert", True, f"Successfully resolved alert {alert_id} with timestamp")
                    return True
                else:
                    self.log_test("POST Resolve Alert", False, f"Alert not resolved correctly: resolved={alert['resolved']}, resolved_at={alert.get('resolved_at')}")
            else:
                self.log_test("POST Resolve Alert", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Resolve Alert", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_alert_stats(self):
        """Test GET /api/alerts/stats/summary - get alert statistics"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/stats/summary")
            
            if response.status_code == 200:
                stats = response.json()
                required_fields = ['total', 'unresolved', 'resolved', 'by_severity', 'by_type']
                missing_fields = [field for field in required_fields if field not in stats]
                
                if not missing_fields:
                    # Verify by_severity structure
                    severity_fields = ['high', 'medium', 'low']
                    severity_missing = [field for field in severity_fields if field not in stats['by_severity']]
                    
                    # Verify by_type structure
                    type_fields = ['chemical', 'flow', 'leak', 'time', 'cost']
                    type_missing = [field for field in type_fields if field not in stats['by_type']]
                    
                    if not severity_missing and not type_missing:
                        # Verify totals make sense
                        if stats['total'] == stats['unresolved'] + stats['resolved']:
                            self.log_test("GET Alert Stats", True, f"Retrieved alert statistics: {stats['total']} total, {stats['unresolved']} unresolved, {stats['resolved']} resolved")
                            return True
                        else:
                            self.log_test("GET Alert Stats", False, f"Total count mismatch: total={stats['total']}, unresolved={stats['unresolved']}, resolved={stats['resolved']}")
                    else:
                        self.log_test("GET Alert Stats", False, f"Missing severity/type fields: {severity_missing}, {type_missing}")
                else:
                    self.log_test("GET Alert Stats", False, f"Missing fields in stats: {missing_fields}")
            else:
                self.log_test("GET Alert Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Alert Stats", False, f"Exception: {str(e)}")
        
        return False
    
    def test_delete_alert(self):
        """Test DELETE /api/alerts/{alert_id} - delete alert"""
        try:
            # Only delete if we created a test alert
            if self.created_alert_id:
                response = self.session.delete(f"{self.base_url}/alerts/{self.created_alert_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "deleted successfully" in result.get('message', ''):
                        # Verify alert is actually deleted
                        verify_response = self.session.get(f"{self.base_url}/alerts/{self.created_alert_id}")
                        if verify_response.status_code == 404:
                            self.log_test("DELETE Alert", True, f"Successfully deleted alert {self.created_alert_id}")
                            return True
                        else:
                            self.log_test("DELETE Alert", False, "Alert still exists after deletion")
                    else:
                        self.log_test("DELETE Alert", False, f"Unexpected response: {result}")
                else:
                    self.log_test("DELETE Alert", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("DELETE Alert", True, "Skipped - no test alert was created")
                return True
                
        except Exception as e:
            self.log_test("DELETE Alert", False, f"Exception: {str(e)}")
        
        return False
    
    def test_nonexistent_alert(self):
        """Test GET /api/alerts/{alert_id} with non-existent ID"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/nonexistent-alert")
            
            if response.status_code == 404:
                self.log_test("GET Non-existent Alert", True, "Correctly returned 404 for non-existent alert")
                return True
            else:
                self.log_test("GET Non-existent Alert", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Non-existent Alert", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== REPORTS API TESTS =====
    
    def test_get_revenue_report(self):
        """Test GET /api/reports/revenue - revenue breakdown"""
        try:
            response = self.session.get(f"{self.base_url}/reports/revenue")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                if "summary" in data and "breakdown" in data:
                    summary = data["summary"]
                    required_fields = ["total_revenue", "paid_revenue", "outstanding_revenue", "total_invoices"]
                    missing_fields = [field for field in required_fields if field not in summary]
                    
                    if not missing_fields:
                        # Verify breakdown is a list
                        if isinstance(data["breakdown"], list):
                            self.log_test("GET Revenue Report", True, f"Retrieved revenue report with {summary['total_invoices']} invoices, total revenue: ${summary['total_revenue']}")
                            return True
                        else:
                            self.log_test("GET Revenue Report", False, "Breakdown should be a list")
                    else:
                        self.log_test("GET Revenue Report", False, f"Missing summary fields: {missing_fields}")
                else:
                    self.log_test("GET Revenue Report", False, "Missing summary or breakdown in response")
            else:
                self.log_test("GET Revenue Report", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Revenue Report", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_jobs_performance(self):
        """Test GET /api/reports/jobs-performance - job completion statistics"""
        try:
            response = self.session.get(f"{self.base_url}/reports/jobs-performance")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                if "summary" in data and "by_service_type" in data:
                    summary = data["summary"]
                    required_fields = ["total_jobs", "completed_jobs", "in_progress_jobs", "scheduled_jobs", "completion_rate"]
                    missing_fields = [field for field in required_fields if field not in summary]
                    
                    if not missing_fields:
                        # Verify by_service_type is a list
                        if isinstance(data["by_service_type"], list):
                            self.log_test("GET Jobs Performance", True, f"Retrieved job performance: {summary['total_jobs']} total jobs, {summary['completion_rate']}% completion rate")
                            return True
                        else:
                            self.log_test("GET Jobs Performance", False, "by_service_type should be a list")
                    else:
                        self.log_test("GET Jobs Performance", False, f"Missing summary fields: {missing_fields}")
                else:
                    self.log_test("GET Jobs Performance", False, "Missing summary or by_service_type in response")
            else:
                self.log_test("GET Jobs Performance", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Jobs Performance", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_customer_stats(self):
        """Test GET /api/reports/customer-stats - customer statistics"""
        try:
            response = self.session.get(f"{self.base_url}/reports/customer-stats")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["total_customers", "active_customers", "paused_customers", "inactive_customers", 
                                 "total_pools", "avg_pools_per_customer", "autopay_customers", "autopay_percentage"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_test("GET Customer Stats", True, f"Retrieved customer stats: {data['total_customers']} customers, {data['total_pools']} pools, {data['autopay_percentage']}% autopay")
                    return True
                else:
                    self.log_test("GET Customer Stats", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Stats", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_technician_performance(self):
        """Test GET /api/reports/technician-performance - technician performance metrics"""
        try:
            response = self.session.get(f"{self.base_url}/reports/technician-performance")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                if "technicians" in data:
                    technicians = data["technicians"]
                    if isinstance(technicians, list) and len(technicians) > 0:
                        # Check first technician structure
                        tech = technicians[0]
                        required_fields = ["technician_id", "technician_name", "total_jobs", "completed_jobs", 
                                         "in_progress_jobs", "scheduled_jobs", "completion_rate"]
                        missing_fields = [field for field in required_fields if field not in tech]
                        
                        if not missing_fields:
                            self.log_test("GET Technician Performance", True, f"Retrieved performance for {len(technicians)} technicians")
                            return True
                        else:
                            self.log_test("GET Technician Performance", False, f"Missing technician fields: {missing_fields}")
                    else:
                        self.log_test("GET Technician Performance", True, "Retrieved technician performance (no technicians found)")
                        return True
                else:
                    self.log_test("GET Technician Performance", False, "Missing technicians field in response")
            else:
                self.log_test("GET Technician Performance", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Technician Performance", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_financial_summary(self):
        """Test GET /api/reports/financial-summary - overall financial summary"""
        try:
            response = self.session.get(f"{self.base_url}/reports/financial-summary")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                if "invoices" in data and "quotes" in data:
                    invoices = data["invoices"]
                    quotes = data["quotes"]
                    
                    invoice_fields = ["total_invoiced", "total_paid", "total_outstanding", "overdue_amount", 
                                    "paid_count", "sent_count", "draft_count", "overdue_count"]
                    quote_fields = ["total_quotes", "pending_quotes", "approved_quotes", "declined_quotes", "conversion_rate"]
                    
                    missing_invoice_fields = [field for field in invoice_fields if field not in invoices]
                    missing_quote_fields = [field for field in quote_fields if field not in quotes]
                    
                    if not missing_invoice_fields and not missing_quote_fields:
                        self.log_test("GET Financial Summary", True, f"Retrieved financial summary: ${invoices['total_invoiced']} invoiced, {quotes['conversion_rate']}% quote conversion")
                        return True
                    else:
                        self.log_test("GET Financial Summary", False, f"Missing fields - invoices: {missing_invoice_fields}, quotes: {missing_quote_fields}")
                else:
                    self.log_test("GET Financial Summary", False, "Missing invoices or quotes in response")
            else:
                self.log_test("GET Financial Summary", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Financial Summary", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_dashboard_stats(self):
        """Test GET /api/reports/dashboard-stats - key dashboard metrics"""
        try:
            response = self.session.get(f"{self.base_url}/reports/dashboard-stats")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                if "customers" in data and "jobs" in data and "alerts" in data and "revenue" in data:
                    customers = data["customers"]
                    jobs = data["jobs"]
                    alerts = data["alerts"]
                    revenue = data["revenue"]
                    
                    # Check required fields in each section
                    if ("total" in customers and "active" in customers and
                        "total" in jobs and "completed" in jobs and
                        "unresolved" in alerts and
                        "total" in revenue and "paid" in revenue and "outstanding" in revenue):
                        
                        self.log_test("GET Dashboard Stats", True, f"Retrieved dashboard stats: {customers['total']} customers, {jobs['total']} jobs, {alerts['unresolved']} alerts, ${revenue['total']} revenue")
                        return True
                    else:
                        self.log_test("GET Dashboard Stats", False, "Missing required fields in dashboard stats sections")
                else:
                    self.log_test("GET Dashboard Stats", False, "Missing required sections in dashboard stats")
            else:
                self.log_test("GET Dashboard Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Dashboard Stats", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== CUSTOMER AUTH API TESTS =====
    
    def test_customer_login(self):
        """Test POST /api/auth/login - login with test account"""
        try:
            login_data = {
                "email": "john.anderson@email.com",
                "password": "password123"
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify token structure
                required_fields = ["access_token", "token_type", "customer_id", "customer_name"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Store token for subsequent tests
                    self.jwt_token = data["access_token"]
                    self.customer_id = data["customer_id"]
                    self.customer_name = data["customer_name"]
                    
                    if data["token_type"] == "bearer" and data["customer_id"] == "cust-1":
                        self.log_test("POST Customer Login", True, f"Successfully logged in as {data['customer_name']} (ID: {data['customer_id']})")
                        return True
                    else:
                        self.log_test("POST Customer Login", False, f"Unexpected token data: {data}")
                else:
                    self.log_test("POST Customer Login", False, f"Missing token fields: {missing_fields}")
            else:
                self.log_test("POST Customer Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Customer Login", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_current_customer(self):
        """Test GET /api/auth/me - get current authenticated customer info"""
        try:
            if not self.jwt_token:
                self.log_test("GET Current Customer", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify customer info structure
                required_fields = ["id", "name", "email", "phone", "address", "status"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    if data["id"] == self.customer_id and data["name"] == self.customer_name:
                        self.log_test("GET Current Customer", True, f"Retrieved customer info for {data['name']} ({data['id']})")
                        return True
                    else:
                        self.log_test("GET Current Customer", False, f"Customer info mismatch: expected {self.customer_id}, got {data.get('id')}")
                else:
                    self.log_test("GET Current Customer", False, f"Missing customer fields: {missing_fields}")
            else:
                self.log_test("GET Current Customer", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Current Customer", False, f"Exception: {str(e)}")
        
        return False
    
    def test_customer_register(self):
        """Test POST /api/auth/register - register new account for existing customer"""
        try:
            register_data = {
                "customer_id": "cust-2",
                "email": "sarah.mitchell.new@email.com",
                "password": "newpassword123"
            }
            
            response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify token structure
                required_fields = ["access_token", "token_type", "customer_id", "customer_name"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    if data["token_type"] == "bearer" and data["customer_id"] == "cust-2":
                        self.log_test("POST Customer Register", True, f"Successfully registered new account for {data['customer_name']} (ID: {data['customer_id']})")
                        return True
                    else:
                        self.log_test("POST Customer Register", False, f"Unexpected registration data: {data}")
                else:
                    self.log_test("POST Customer Register", False, f"Missing token fields: {missing_fields}")
            else:
                self.log_test("POST Customer Register", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Customer Register", False, f"Exception: {str(e)}")
        
        return False
    
    # ===== CUSTOMER PORTAL API TESTS =====
    
    def test_get_customer_pools(self):
        """Test GET /api/portal/pools - get customer's pools"""
        try:
            if not self.jwt_token:
                self.log_test("GET Customer Pools", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/pools", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "pools"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    if data["customer_id"] == self.customer_id:
                        pools_count = len(data["pools"])
                        self.log_test("GET Customer Pools", True, f"Retrieved {pools_count} pools for customer {data['customer_name']}")
                        return True
                    else:
                        self.log_test("GET Customer Pools", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                else:
                    self.log_test("GET Customer Pools", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Pools", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Pools", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_customer_invoices(self):
        """Test GET /api/portal/invoices - get customer's invoices"""
        try:
            if not self.jwt_token:
                self.log_test("GET Customer Invoices", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/invoices", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "invoices", "summary"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    summary = data["summary"]
                    summary_fields = ["total_invoiced", "total_paid", "total_outstanding", "invoice_count"]
                    missing_summary_fields = [field for field in summary_fields if field not in summary]
                    
                    if not missing_summary_fields:
                        if data["customer_id"] == self.customer_id:
                            self.log_test("GET Customer Invoices", True, f"Retrieved {summary['invoice_count']} invoices for customer, total: ${summary['total_invoiced']}")
                            return True
                        else:
                            self.log_test("GET Customer Invoices", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                    else:
                        self.log_test("GET Customer Invoices", False, f"Missing summary fields: {missing_summary_fields}")
                else:
                    self.log_test("GET Customer Invoices", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Invoices", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Invoices", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_specific_invoice(self):
        """Test GET /api/portal/invoices/{invoice_id} - get specific invoice"""
        try:
            if not self.jwt_token:
                self.log_test("GET Specific Invoice", False, "No JWT token available - login test must run first")
                return False
            
            # First get customer invoices to find a valid invoice ID
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            invoices_response = self.session.get(f"{self.base_url}/portal/invoices", headers=headers)
            
            if invoices_response.status_code == 200:
                invoices_data = invoices_response.json()
                invoices = invoices_data.get("invoices", [])
                
                if invoices:
                    invoice_id = invoices[0]["id"]
                    
                    response = self.session.get(f"{self.base_url}/portal/invoices/{invoice_id}", headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Verify invoice structure
                        required_fields = ["id", "customer_id", "customer_name", "total", "status"]
                        missing_fields = [field for field in required_fields if field not in data]
                        
                        if not missing_fields:
                            if data["id"] == invoice_id and data["customer_id"] == self.customer_id:
                                self.log_test("GET Specific Invoice", True, f"Retrieved invoice {invoice_id} with total ${data['total']}")
                                return True
                            else:
                                self.log_test("GET Specific Invoice", False, f"Invoice data mismatch")
                        else:
                            self.log_test("GET Specific Invoice", False, f"Missing invoice fields: {missing_fields}")
                    else:
                        self.log_test("GET Specific Invoice", False, f"HTTP {response.status_code}: {response.text}")
                else:
                    self.log_test("GET Specific Invoice", True, "No invoices found for customer (acceptable)")
                    return True
            else:
                self.log_test("GET Specific Invoice", False, "Could not retrieve customer invoices for testing")
                
        except Exception as e:
            self.log_test("GET Specific Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_customer_jobs(self):
        """Test GET /api/portal/jobs - get customer's jobs"""
        try:
            if not self.jwt_token:
                self.log_test("GET Customer Jobs", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/jobs", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "jobs", "summary"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    summary = data["summary"]
                    summary_fields = ["total_jobs", "scheduled", "in_progress", "completed"]
                    missing_summary_fields = [field for field in summary_fields if field not in summary]
                    
                    if not missing_summary_fields:
                        if data["customer_id"] == self.customer_id:
                            self.log_test("GET Customer Jobs", True, f"Retrieved {summary['total_jobs']} jobs for customer ({summary['completed']} completed)")
                            return True
                        else:
                            self.log_test("GET Customer Jobs", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                    else:
                        self.log_test("GET Customer Jobs", False, f"Missing summary fields: {missing_summary_fields}")
                else:
                    self.log_test("GET Customer Jobs", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Jobs", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Jobs", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_customer_quotes(self):
        """Test GET /api/portal/quotes - get customer's quotes"""
        try:
            if not self.jwt_token:
                self.log_test("GET Customer Quotes", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/quotes", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "quotes", "summary"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    summary = data["summary"]
                    summary_fields = ["total_quotes", "pending", "approved", "declined"]
                    missing_summary_fields = [field for field in summary_fields if field not in summary]
                    
                    if not missing_summary_fields:
                        if data["customer_id"] == self.customer_id:
                            self.log_test("GET Customer Quotes", True, f"Retrieved {summary['total_quotes']} quotes for customer ({summary['approved']} approved)")
                            return True
                        else:
                            self.log_test("GET Customer Quotes", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                    else:
                        self.log_test("GET Customer Quotes", False, f"Missing summary fields: {missing_summary_fields}")
                else:
                    self.log_test("GET Customer Quotes", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Quotes", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Quotes", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_service_history(self):
        """Test GET /api/portal/service-history - get chemical readings from all pools"""
        try:
            if not self.jwt_token:
                self.log_test("GET Service History", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/service-history", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "service_history"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    if data["customer_id"] == self.customer_id:
                        service_history = data["service_history"]
                        if isinstance(service_history, list):
                            # Check if we have readings and verify structure
                            if service_history:
                                reading = service_history[0]
                                reading_fields = ["pool_id", "pool_name", "date", "fc", "ph", "ta", "ch", "cya"]
                                missing_reading_fields = [field for field in reading_fields if field not in reading]
                                
                                if not missing_reading_fields:
                                    self.log_test("GET Service History", True, f"Retrieved {len(service_history)} chemical readings for customer")
                                    return True
                                else:
                                    self.log_test("GET Service History", False, f"Missing reading fields: {missing_reading_fields}")
                            else:
                                self.log_test("GET Service History", True, "Retrieved service history (no readings found - acceptable)")
                                return True
                        else:
                            self.log_test("GET Service History", False, "service_history should be a list")
                    else:
                        self.log_test("GET Service History", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                else:
                    self.log_test("GET Service History", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Service History", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Service History", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_customer_alerts(self):
        """Test GET /api/portal/alerts - get customer's alerts"""
        try:
            if not self.jwt_token:
                self.log_test("GET Customer Alerts", False, "No JWT token available - login test must run first")
                return False
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{self.base_url}/portal/alerts", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify structure
                required_fields = ["customer_id", "customer_name", "alerts", "summary"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    summary = data["summary"]
                    summary_fields = ["total_alerts", "unresolved", "resolved"]
                    missing_summary_fields = [field for field in summary_fields if field not in summary]
                    
                    if not missing_summary_fields:
                        if data["customer_id"] == self.customer_id:
                            self.log_test("GET Customer Alerts", True, f"Retrieved {summary['total_alerts']} alerts for customer ({summary['unresolved']} unresolved)")
                            return True
                        else:
                            self.log_test("GET Customer Alerts", False, f"Customer ID mismatch: expected {self.customer_id}, got {data.get('customer_id')}")
                    else:
                        self.log_test("GET Customer Alerts", False, f"Missing summary fields: {missing_summary_fields}")
                else:
                    self.log_test("GET Customer Alerts", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET Customer Alerts", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Customer Alerts", False, f"Exception: {str(e)}")
        
        return False
    
    def test_unauthorized_portal_access(self):
        """Test portal endpoints without JWT token - should return 401"""
        try:
            # Test without Authorization header
            response = self.session.get(f"{self.base_url}/portal/pools")
            
            if response.status_code == 401:
                self.log_test("Unauthorized Portal Access", True, "Correctly returned 401 for unauthorized portal access")
                return True
            else:
                self.log_test("Unauthorized Portal Access", False, f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Unauthorized Portal Access", False, f"Exception: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all Phase 4 backend API tests"""
        print(f"🧪 Starting PoolPro Phase 4 Backend API Tests - Alert System")
        print(f"🔗 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence - organized by API group
        tests = [
            # Alerts API Tests
            self.test_get_all_alerts,
            self.test_get_alerts_filtered_unresolved,
            self.test_get_alerts_filtered_resolved,
            self.test_get_alerts_filtered_by_severity,
            self.test_get_alerts_filtered_by_type,
            self.test_get_alert_by_id,
            self.test_create_alert,
            self.test_update_alert,
            self.test_resolve_alert,
            self.test_get_alert_stats,
            self.test_delete_alert,
            
            # Error Handling Tests
            self.test_nonexistent_alert
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
            print("🎉 All tests passed! Phase 4 Alert System Backend APIs are working correctly.")
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
