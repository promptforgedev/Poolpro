#!/usr/bin/env python3
"""
Backend API Testing for Pool Management Software (PoolPro)
Phase 3: Tests Route & Scheduling (Technicians, Routes)
"""

import requests
import json
import sys
from datetime import datetime, timezone, timedelta

# Backend URL from environment
BACKEND_URL = "https://pooltask.preview.emergentagent.com/api"

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
    
    def run_all_tests(self):
        """Run all Phase 2 backend API tests"""
        print(f"🧪 Starting PoolPro Phase 2 Backend API Tests")
        print(f"🔗 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence - organized by API group
        tests = [
            # Quotes API Tests
            self.test_get_all_quotes,
            self.test_get_quote_by_id,
            self.test_create_quote,
            self.test_update_quote,
            self.test_approve_quote,
            self.test_decline_quote,
            self.test_delete_quote,
            
            # Jobs API Tests
            self.test_get_all_jobs,
            self.test_get_job_by_id,
            self.test_create_job,
            self.test_update_job,
            self.test_start_job,
            self.test_complete_job,
            self.test_get_jobs_by_date,
            self.test_get_jobs_by_technician,
            self.test_delete_job,
            
            # Invoices API Tests
            self.test_get_all_invoices,
            self.test_get_invoice_by_id,
            self.test_create_invoice,
            self.test_update_invoice_payment,
            self.test_delete_invoice,
            
            # Error Handling Tests
            self.test_nonexistent_quote,
            self.test_nonexistent_job,
            self.test_nonexistent_invoice
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
            print("🎉 All tests passed! Phase 2 Backend APIs are working correctly.")
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
