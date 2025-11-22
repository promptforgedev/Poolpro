#!/usr/bin/env python3
"""
Backend API Testing for Pool Management Software (PoolPro)
Phase 2: Job Management Workflow (Quotes, Jobs, Invoices)
"""

import requests
import json
import sys
from datetime import datetime, timezone

# Backend URL from environment
BACKEND_URL = "https://swimsmart.preview.emergentagent.com/api"

class PoolProPhase2Tester:
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
    
    # ==================== QUOTES API TESTS ====================
    
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
                            self.log_test("GET All Quotes", True, f"Retrieved {len(quotes)} quotes with correct structure and various statuses: {set(statuses)}")
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
        """Test POST /api/quotes - create new quote"""
        try:
            new_quote = {
                "customer_id": "cust-1",
                "customer_name": "John Anderson",
                "items": [
                    {"description": "Pool Filter Replacement", "quantity": 1, "unit_price": 150.00, "total": 150.00},
                    {"description": "Labor", "quantity": 1, "unit_price": 75.00, "total": 75.00}
                ],
                "subtotal": 225.00,
                "tax": 18.00,
                "total": 243.00,
                "notes": "Test quote creation",
                "valid_until": "2025-02-15"
            }
            
            response = self.session.post(f"{self.base_url}/quotes", json=new_quote)
            
            if response.status_code == 200:
                quote = response.json()
                if quote['customer_name'] == 'John Anderson' and quote['id'].startswith('quote-'):
                    # Store for later tests
                    self.created_quote_id = quote['id']
                    
                    # Verify calculations
                    if quote['total'] == 243.00 and quote['subtotal'] == 225.00:
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
    
    def test_approve_quote(self):
        """Test POST /api/quotes/{quote_id}/approve"""
        try:
            # Use quote-001 which is pending
            response = self.session.post(f"{self.base_url}/quotes/quote-001/approve")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Quote approved' and result['quote']['status'] == 'approved':
                    self.log_test("POST Approve Quote", True, "Successfully approved quote-001")
                    return True
                else:
                    self.log_test("POST Approve Quote", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Approve Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Approve Quote", False, f"Exception: {str(e)}")
        
        return False
    
    def test_decline_quote(self):
        """Test POST /api/quotes/{quote_id}/decline"""
        try:
            # Use quote-004 which is pending
            response = self.session.post(f"{self.base_url}/quotes/quote-004/decline")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Quote declined' and result['quote']['status'] == 'declined':
                    self.log_test("POST Decline Quote", True, "Successfully declined quote-004")
                    return True
                else:
                    self.log_test("POST Decline Quote", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Decline Quote", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Decline Quote", False, f"Exception: {str(e)}")
        
        return False
    
    # ==================== JOBS API TESTS ====================
    
    def test_get_all_jobs(self):
        """Test GET /api/jobs - should return 6 seeded jobs"""
        try:
            response = self.session.get(f"{self.base_url}/jobs")
            
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
                            self.log_test("GET All Jobs", True, f"Retrieved {len(jobs)} jobs with correct structure and various statuses: {set(statuses)}")
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
    
    def test_get_jobs_by_status(self):
        """Test GET /api/jobs?status=scheduled - filter by status"""
        try:
            response = self.session.get(f"{self.base_url}/jobs?status=scheduled")
            
            if response.status_code == 200:
                jobs = response.json()
                if len(jobs) > 0:
                    # Verify all jobs have scheduled status
                    all_scheduled = all(job['status'] == 'scheduled' for job in jobs)
                    if all_scheduled:
                        self.log_test("GET Jobs by Status", True, f"Retrieved {len(jobs)} scheduled jobs")
                        return True
                    else:
                        statuses = [job['status'] for job in jobs]
                        self.log_test("GET Jobs by Status", False, f"Not all jobs are scheduled: {statuses}")
                else:
                    self.log_test("GET Jobs by Status", False, "No scheduled jobs found")
            else:
                self.log_test("GET Jobs by Status", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Jobs by Status", False, f"Exception: {str(e)}")
        
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
                        self.log_test("GET Job by ID", False, f"Incorrect job details: service_type={job['service_type']}, technician={job['technician']}")
                else:
                    self.log_test("GET Job by ID", False, f"Unexpected job data: {job.get('id', 'Unknown')}")
            else:
                self.log_test("GET Job by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Job by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_job(self):
        """Test POST /api/jobs - create new job"""
        try:
            new_job = {
                "customer_id": "cust-2",
                "customer_name": "Sarah Wilson",
                "customer_address": "456 Oak Avenue, Austin, TX 78702",
                "service_type": "One-time Service",
                "scheduled_date": "2025-01-20",
                "scheduled_time": "02:00 PM",
                "technician": "David Chen",
                "pools": ["pool-2"],
                "notes": "Test job creation"
            }
            
            response = self.session.post(f"{self.base_url}/jobs", json=new_job)
            
            if response.status_code == 200:
                job = response.json()
                if job['customer_name'] == 'Sarah Wilson' and job['id'].startswith('job-'):
                    # Store for later tests
                    self.created_job_id = job['id']
                    
                    # Verify job details
                    if job['service_type'] == 'One-time Service' and job['status'] == 'scheduled':
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
    
    def test_start_job(self):
        """Test POST /api/jobs/{job_id}/start"""
        try:
            # Use job-001 which is scheduled
            response = self.session.post(f"{self.base_url}/jobs/job-001/start")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Job started' and result['job']['status'] == 'in-progress':
                    self.log_test("POST Start Job", True, "Successfully started job-001")
                    return True
                else:
                    self.log_test("POST Start Job", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Start Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Start Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_complete_job(self):
        """Test POST /api/jobs/{job_id}/complete"""
        try:
            # Use job-004 which is scheduled
            response = self.session.post(f"{self.base_url}/jobs/job-004/complete", 
                                       params={"completion_notes": "Pool cleaner repaired successfully"})
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Job completed' and result['job']['status'] == 'completed':
                    # Verify completion notes and completed_at timestamp
                    if result['job'].get('completion_notes') == 'Pool cleaner repaired successfully':
                        self.log_test("POST Complete Job", True, "Successfully completed job-004 with notes")
                        return True
                    else:
                        self.log_test("POST Complete Job", False, "Completion notes not set correctly")
                else:
                    self.log_test("POST Complete Job", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Complete Job", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Complete Job", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_jobs_by_technician(self):
        """Test GET /api/jobs/by-technician/{technician}"""
        try:
            response = self.session.get(f"{self.base_url}/jobs/by-technician/Mike Johnson")
            
            if response.status_code == 200:
                jobs = response.json()
                if len(jobs) > 0:
                    # Verify all jobs are assigned to Mike Johnson
                    all_mike = all(job['technician'] == 'Mike Johnson' for job in jobs)
                    if all_mike:
                        self.log_test("GET Jobs by Technician", True, f"Retrieved {len(jobs)} jobs for Mike Johnson")
                        return True
                    else:
                        technicians = [job['technician'] for job in jobs]
                        self.log_test("GET Jobs by Technician", False, f"Not all jobs assigned to Mike Johnson: {technicians}")
                else:
                    self.log_test("GET Jobs by Technician", False, "No jobs found for Mike Johnson")
            else:
                self.log_test("GET Jobs by Technician", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Jobs by Technician", False, f"Exception: {str(e)}")
        
        return False
    
    # ==================== INVOICES API TESTS ====================
    
    def test_get_all_invoices(self):
        """Test GET /api/invoices - should return 5 seeded invoices"""
        try:
            response = self.session.get(f"{self.base_url}/invoices")
            
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
                        expected_statuses = ['paid', 'sent', 'overdue', 'draft']
                        has_expected_statuses = any(status in statuses for status in expected_statuses)
                        
                        if has_expected_statuses:
                            self.log_test("GET All Invoices", True, f"Retrieved {len(invoices)} invoices with correct structure and various statuses: {set(statuses)}")
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
    
    def test_get_invoices_by_status(self):
        """Test GET /api/invoices?status=paid - filter by status"""
        try:
            response = self.session.get(f"{self.base_url}/invoices?status=paid")
            
            if response.status_code == 200:
                invoices = response.json()
                if len(invoices) > 0:
                    # Verify all invoices have paid status
                    all_paid = all(invoice['status'] == 'paid' for invoice in invoices)
                    if all_paid:
                        self.log_test("GET Invoices by Status", True, f"Retrieved {len(invoices)} paid invoices")
                        return True
                    else:
                        statuses = [invoice['status'] for invoice in invoices]
                        self.log_test("GET Invoices by Status", False, f"Not all invoices are paid: {statuses}")
                else:
                    self.log_test("GET Invoices by Status", False, "No paid invoices found")
            else:
                self.log_test("GET Invoices by Status", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Invoices by Status", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_invoice_by_id(self):
        """Test GET /api/invoices/{invoice_id} with existing invoice"""
        try:
            # Test with seeded invoice "inv-001"
            response = self.session.get(f"{self.base_url}/invoices/inv-001")
            
            if response.status_code == 200:
                invoice = response.json()
                if invoice['id'] == 'inv-001' and invoice['status'] == 'paid':
                    # Verify invoice calculations
                    if invoice['total'] == 172.80 and invoice['balance_due'] == 0.00:
                        self.log_test("GET Invoice by ID", True, "Retrieved invoice with correct calculations")
                        return True
                    else:
                        self.log_test("GET Invoice by ID", False, f"Incorrect calculations: total={invoice['total']}, balance_due={invoice['balance_due']}")
                else:
                    self.log_test("GET Invoice by ID", False, f"Unexpected invoice data: {invoice.get('id', 'Unknown')}")
            else:
                self.log_test("GET Invoice by ID", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Invoice by ID", False, f"Exception: {str(e)}")
        
        return False
    
    def test_create_invoice(self):
        """Test POST /api/invoices - create new invoice"""
        try:
            new_invoice = {
                "customer_id": "cust-3",
                "customer_name": "Michael Brown",
                "job_id": "job-003",
                "invoice_number": "INV-TEST-001",
                "line_items": [
                    {"description": "Test Service", "quantity": 1, "unit_price": 100.00, "total": 100.00}
                ],
                "subtotal": 100.00,
                "tax": 8.00,
                "total": 108.00,
                "issue_date": "2025-01-16",
                "due_date": "2025-02-15",
                "notes": "Test invoice creation"
            }
            
            response = self.session.post(f"{self.base_url}/invoices", json=new_invoice)
            
            if response.status_code == 200:
                invoice = response.json()
                if invoice['customer_name'] == 'Michael Brown' and invoice['id'].startswith('inv-'):
                    # Store for later tests
                    self.created_invoice_id = invoice['id']
                    
                    # Verify calculations
                    if invoice['total'] == 108.00 and invoice['balance_due'] == 108.00:
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
    
    def test_send_invoice(self):
        """Test POST /api/invoices/{invoice_id}/send"""
        try:
            # Use inv-005 which is draft
            response = self.session.post(f"{self.base_url}/invoices/inv-005/send")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Invoice sent' and result['invoice']['status'] == 'sent':
                    self.log_test("POST Send Invoice", True, "Successfully sent inv-005")
                    return True
                else:
                    self.log_test("POST Send Invoice", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Send Invoice", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Send Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    def test_pay_invoice(self):
        """Test POST /api/invoices/{invoice_id}/pay"""
        try:
            # Use inv-003 which has balance due of 156.60
            response = self.session.post(f"{self.base_url}/invoices/inv-003/pay", 
                                       params={"amount": 156.60})
            
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Payment of $156.6 recorded' and result['invoice']['status'] == 'paid':
                    # Verify balance is now zero
                    if result['invoice']['balance_due'] == 0.00:
                        self.log_test("POST Pay Invoice", True, "Successfully paid inv-003 in full")
                        return True
                    else:
                        self.log_test("POST Pay Invoice", False, f"Balance not updated correctly: {result['invoice']['balance_due']}")
                else:
                    self.log_test("POST Pay Invoice", False, f"Unexpected response: {result}")
            else:
                self.log_test("POST Pay Invoice", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("POST Pay Invoice", False, f"Exception: {str(e)}")
        
        return False
    
    def test_get_invoices_by_customer(self):
        """Test GET /api/invoices/by-customer/{customer_id}"""
        try:
            # Get invoices for cust-1 (John Anderson)
            response = self.session.get(f"{self.base_url}/invoices/by-customer/cust-1")
            
            if response.status_code == 200:
                invoices = response.json()
                if len(invoices) > 0:
                    # Verify all invoices belong to cust-1
                    all_cust1 = all(invoice['customer_id'] == 'cust-1' for invoice in invoices)
                    if all_cust1:
                        self.log_test("GET Invoices by Customer", True, f"Retrieved {len(invoices)} invoices for cust-1")
                        return True
                    else:
                        customer_ids = [invoice['customer_id'] for invoice in invoices]
                        self.log_test("GET Invoices by Customer", False, f"Not all invoices belong to cust-1: {customer_ids}")
                else:
                    self.log_test("GET Invoices by Customer", False, "No invoices found for cust-1")
            else:
                self.log_test("GET Invoices by Customer", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Invoices by Customer", False, f"Exception: {str(e)}")
        
        return False
    
    # ==================== DATA VALIDATION TESTS ====================
    
    def test_data_relationships(self):
        """Test relationships between quotes, jobs, and invoices"""
        try:
            # Get all data
            quotes_response = self.session.get(f"{self.base_url}/quotes")
            jobs_response = self.session.get(f"{self.base_url}/jobs")
            invoices_response = self.session.get(f"{self.base_url}/invoices")
            
            if all(r.status_code == 200 for r in [quotes_response, jobs_response, invoices_response]):
                quotes = quotes_response.json()
                jobs = jobs_response.json()
                invoices = invoices_response.json()
                
                # Check quote-job relationships
                quote_ids = {q['id'] for q in quotes}
                job_quote_refs = {j['quote_id'] for j in jobs if j.get('quote_id')}
                
                # Check job-invoice relationships
                job_ids = {j['id'] for j in jobs}
                invoice_job_refs = {i['job_id'] for i in invoices if i.get('job_id')}
                
                # Verify relationships exist
                valid_quote_refs = job_quote_refs.issubset(quote_ids) if job_quote_refs else True
                valid_job_refs = invoice_job_refs.issubset(job_ids) if invoice_job_refs else True
                
                if valid_quote_refs and valid_job_refs:
                    self.log_test("Data Relationships", True, f"All relationships valid. Quote refs: {len(job_quote_refs)}, Job refs: {len(invoice_job_refs)}")
                    return True
                else:
                    self.log_test("Data Relationships", False, f"Invalid relationships found. Quote refs valid: {valid_quote_refs}, Job refs valid: {valid_job_refs}")
            else:
                self.log_test("Data Relationships", False, "Failed to retrieve data for relationship testing")
                
        except Exception as e:
            self.log_test("Data Relationships", False, f"Exception: {str(e)}")
        
        return False
    
    def test_cleanup_created_data(self):
        """Clean up test data created during testing"""
        try:
            cleanup_count = 0
            
            # Delete created quote
            if self.created_quote_id:
                response = self.session.delete(f"{self.base_url}/quotes/{self.created_quote_id}")
                if response.status_code == 200:
                    cleanup_count += 1
            
            # Delete created job
            if self.created_job_id:
                response = self.session.delete(f"{self.base_url}/jobs/{self.created_job_id}")
                if response.status_code == 200:
                    cleanup_count += 1
            
            # Delete created invoice
            if self.created_invoice_id:
                response = self.session.delete(f"{self.base_url}/invoices/{self.created_invoice_id}")
                if response.status_code == 200:
                    cleanup_count += 1
            
            self.log_test("Cleanup Test Data", True, f"Cleaned up {cleanup_count} test records")
            return True
                
        except Exception as e:
            self.log_test("Cleanup Test Data", False, f"Exception: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all Phase 2 backend API tests"""
        print(f"🧪 Starting PoolPro Phase 2 Backend API Tests")
        print(f"🔗 Backend URL: {self.base_url}")
        print("=" * 80)
        
        # Test sequence
        tests = [
            # Quotes API Tests
            self.test_get_all_quotes,
            self.test_get_quote_by_id,
            self.test_create_quote,
            self.test_approve_quote,
            self.test_decline_quote,
            
            # Jobs API Tests
            self.test_get_all_jobs,
            self.test_get_jobs_by_status,
            self.test_get_job_by_id,
            self.test_create_job,
            self.test_start_job,
            self.test_complete_job,
            self.test_get_jobs_by_technician,
            
            # Invoices API Tests
            self.test_get_all_invoices,
            self.test_get_invoices_by_status,
            self.test_get_invoice_by_id,
            self.test_create_invoice,
            self.test_send_invoice,
            self.test_pay_invoice,
            self.test_get_invoices_by_customer,
            
            # Data Validation Tests
            self.test_data_relationships,
            self.test_cleanup_created_data
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()  # Add spacing between tests
        
        print("=" * 80)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All Phase 2 tests passed! Job Management Workflow APIs are working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Check the issues above.")
            return False

def main():
    """Main test execution"""
    tester = PoolProPhase2Tester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()