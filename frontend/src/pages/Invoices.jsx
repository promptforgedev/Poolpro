import React, { useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockInvoices } from '../mock';
import { Plus, Search, FileText, Download, Send, DollarSign, Calendar } from 'lucide-react';

const Invoices = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid':
        return 'bg-green-100 text-green-700';
      case 'sent':
        return 'bg-blue-100 text-blue-700';
      case 'overdue':
        return 'bg-red-100 text-red-700';
      case 'draft':
        return 'bg-gray-100 text-gray-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const filteredInvoices = mockInvoices.filter(invoice => {
    const matchesSearch = invoice.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         invoice.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || invoice.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const invoiceCounts = {
    all: mockInvoices.length,
    draft: mockInvoices.filter(i => i.status === 'draft').length,
    sent: mockInvoices.filter(i => i.status === 'sent').length,
    paid: mockInvoices.filter(i => i.status === 'paid').length,
    overdue: mockInvoices.filter(i => i.status === 'overdue').length
  };

  const totalRevenue = mockInvoices.reduce((sum, inv) => sum + inv.total, 0);
  const paidRevenue = mockInvoices.filter(i => i.status === 'paid').reduce((sum, inv) => sum + inv.total, 0);
  const outstandingRevenue = mockInvoices.filter(i => i.status !== 'paid' && i.status !== 'draft').reduce((sum, inv) => sum + inv.total, 0);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Invoices</h1>
            <p className="text-gray-600 mt-1">Manage billing and payments</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Create Invoice
          </Button>
        </div>

        {/* Revenue Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">${totalRevenue.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Paid</p>
                  <p className="text-2xl font-bold text-green-600 mt-2">${paidRevenue.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Outstanding</p>
                  <p className="text-2xl font-bold text-orange-600 mt-2">${outstandingRevenue.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search and Filter */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search invoices by customer or invoice number..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Tabs value={statusFilter} onValueChange={setStatusFilter} className="w-full md:w-auto">
                <TabsList>
                  <TabsTrigger value="all">All ({invoiceCounts.all})</TabsTrigger>
                  <TabsTrigger value="draft">Draft ({invoiceCounts.draft})</TabsTrigger>
                  <TabsTrigger value="sent">Sent ({invoiceCounts.sent})</TabsTrigger>
                  <TabsTrigger value="paid">Paid ({invoiceCounts.paid})</TabsTrigger>
                  <TabsTrigger value="overdue">Overdue ({invoiceCounts.overdue})</TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </CardContent>
        </Card>

        {/* Invoices List */}
        <div className="space-y-4">
          {filteredInvoices.map((invoice) => (
            <Card key={invoice.id} className="hover:shadow-md transition-shadow">
              <CardContent className="pt-6">
                <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                  {/* Invoice Icon */}
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <FileText className="h-6 w-6 text-blue-600" />
                    </div>
                  </div>

                  {/* Invoice Details */}
                  <div className="flex-1 space-y-3">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-3">
                          <h3 className="font-semibold text-lg text-gray-900">Invoice #{invoice.id}</h3>
                          <Badge className={getStatusColor(invoice.status)}>
                            {invoice.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{invoice.customerName}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-gray-900">${invoice.total.toFixed(2)}</p>
                        <p className="text-sm text-gray-600 mt-1">{invoice.status === 'paid' ? 'Paid' : 'Outstanding'}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Invoice Date</p>
                        <div className="flex items-center gap-1 text-sm text-gray-900">
                          <Calendar className="h-3 w-3" />
                          <span>{invoice.date}</span>
                        </div>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Due Date</p>
                        <div className="flex items-center gap-1 text-sm text-gray-900">
                          <Calendar className="h-3 w-3" />
                          <span>{invoice.dueDate}</span>
                        </div>
                      </div>
                      {invoice.paidDate && (
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Paid Date</p>
                          <div className="flex items-center gap-1 text-sm text-green-600">
                            <Calendar className="h-3 w-3" />
                            <span>{invoice.paidDate}</span>
                          </div>
                        </div>
                      )}
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Payment Method</p>
                        <p className="text-sm text-gray-900 capitalize">
                          {invoice.paymentMethod.replace('-', ' ')}
                        </p>
                      </div>
                    </div>

                    {/* Line Items */}
                    <div className="border-t pt-3">
                      <p className="text-sm font-medium text-gray-700 mb-2">Line Items:</p>
                      <div className="space-y-1">
                        {invoice.items.map((item, index) => (
                          <div key={index} className="flex justify-between text-sm text-gray-600">
                            <span>
                              {item.description}
                              {item.quantity > 1 && ` (x${item.quantity})`}
                            </span>
                            <span className="font-medium">${item.amount.toFixed(2)}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <Button size="sm" variant="outline">
                        <Download className="h-3 w-3 mr-2" />
                        Download PDF
                      </Button>
                      {invoice.status !== 'paid' && (
                        <>
                          <Button size="sm" variant="outline">
                            <Send className="h-3 w-3 mr-2" />
                            Send Invoice
                          </Button>
                          <Button size="sm" className="bg-green-600 hover:bg-green-700 text-white">
                            Record Payment
                          </Button>
                        </>
                      )}
                      <Button size="sm" variant="outline">View Details</Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Invoices;
