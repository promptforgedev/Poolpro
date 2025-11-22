import React, { useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { mockQuotes } from '../mock';
import { Plus, Search, FileText, Send, CheckCircle, XCircle, Clock } from 'lucide-react';

const Quotes = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-700';
      case 'declined':
        return 'bg-red-100 text-red-700';
      case 'pending':
        return 'bg-yellow-100 text-yellow-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="h-4 w-4" />;
      case 'declined':
        return <XCircle className="h-4 w-4" />;
      case 'pending':
        return <Clock className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const filteredQuotes = mockQuotes.filter(quote =>
    quote.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    quote.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const quoteCounts = {
    total: mockQuotes.length,
    pending: mockQuotes.filter(q => q.status === 'pending').length,
    approved: mockQuotes.filter(q => q.status === 'approved').length,
    declined: mockQuotes.filter(q => q.status === 'declined').length
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Quotes</h1>
            <p className="text-gray-600 mt-1">Create and manage customer quotes</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Create New Quote
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-gray-900">{quoteCounts.total}</p>
                <p className="text-sm text-gray-600 mt-1">Total Quotes</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-yellow-600">{quoteCounts.pending}</p>
                <p className="text-sm text-gray-600 mt-1">Pending</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-green-600">{quoteCounts.approved}</p>
                <p className="text-sm text-gray-600 mt-1">Approved</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-red-600">{quoteCounts.declined}</p>
                <p className="text-sm text-gray-600 mt-1">Declined</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search */}
        <Card>
          <CardContent className="pt-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search quotes by customer or title..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Quotes List */}
        <div className="space-y-4">
          {filteredQuotes.map((quote) => (
            <Card key={quote.id} className="hover:shadow-md transition-shadow">
              <CardContent className="pt-6">
                <div className="flex flex-col lg:flex-row lg:items-start gap-4">
                  {/* Quote Icon */}
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                      <FileText className="h-6 w-6 text-purple-600" />
                    </div>
                  </div>

                  {/* Quote Details */}
                  <div className="flex-1 space-y-3">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <div>
                        <h3 className="font-semibold text-lg text-gray-900">{quote.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">{quote.customerName}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getStatusColor(quote.status)}>
                          {getStatusIcon(quote.status)}
                          <span className="ml-2 capitalize">{quote.status}</span>
                        </Badge>
                        <div className="text-right">
                          <p className="text-xl font-bold text-gray-900">${quote.total.toFixed(2)}</p>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Created Date</p>
                        <p className="text-sm text-gray-900">{quote.createdDate}</p>
                      </div>
                      {quote.status === 'pending' && (
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Expiry Date</p>
                          <p className="text-sm text-gray-900">{quote.expiryDate}</p>
                        </div>
                      )}
                      {quote.approvedDate && (
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Approved Date</p>
                          <p className="text-sm text-green-600">{quote.approvedDate}</p>
                        </div>
                      )}
                      {quote.declinedDate && (
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Declined Date</p>
                          <p className="text-sm text-red-600">{quote.declinedDate}</p>
                        </div>
                      )}
                    </div>

                    {/* Line Items */}
                    <div className="border-t pt-3">
                      <p className="text-sm font-medium text-gray-700 mb-2">Quote Items:</p>
                      <div className="space-y-2">
                        {quote.items.map((item, index) => (
                          <div key={index} className="flex justify-between items-start p-2 bg-gray-50 rounded">
                            <div className="flex-1">
                              <p className="text-sm font-medium text-gray-900">{item.name}</p>
                              <p className="text-xs text-gray-600">Quantity: {item.quantity}</p>
                            </div>
                            <p className="text-sm font-semibold text-gray-900">${item.price.toFixed(2)}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {quote.notes && (
                      <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <p className="text-sm text-gray-700">
                          <span className="font-medium">Notes:</span> {quote.notes}
                        </p>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <Button size="sm" variant="outline">View Details</Button>
                      {quote.status === 'pending' && (
                        <>
                          <Button size="sm" variant="outline">
                            <Send className="h-3 w-3 mr-2" />
                            Resend Quote
                          </Button>
                          <Button size="sm" variant="outline">Edit</Button>
                        </>
                      )}
                      {quote.status === 'approved' && (
                        <Button size="sm" className="bg-green-600 hover:bg-green-700 text-white">
                          Create Job
                        </Button>
                      )}
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

export default Quotes;
