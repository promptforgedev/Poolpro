import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockCustomers, mockInvoices } from '../mock';
import { Droplets, Download, CreditCard, Calendar, Droplet, CheckCircle } from 'lucide-react';

const CustomerPortal = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  
  // Using first customer as logged-in customer for demo
  const customer = mockCustomers[0];
  const customerInvoices = mockInvoices.filter(inv => inv.customerId === customer.id);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-2 rounded-lg">
                <Droplets className="h-6 w-6" />
              </div>
              <span className="text-xl font-bold text-gray-900">PoolPro</span>
              <span className="text-sm text-gray-500 ml-2">Customer Portal</span>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => navigate('/')}>Back to Home</Button>
              <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                {customer.name.split(' ').map(n => n[0]).join('')}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome, {customer.name.split(' ')[0]}!</h1>
          <p className="text-gray-600 mt-1">Manage your pool service account</p>
        </div>

        {/* Account Status */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Account Status</p>
                  <Badge className="bg-green-100 text-green-700 mt-2">
                    <CheckCircle className="h-3 w-3 mr-1" />
                    {customer.status}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div>
                <p className="text-sm text-gray-600">Account Balance</p>
                <p className={`text-2xl font-bold mt-2 ${
                  customer.accountBalance < 0 ? 'text-red-600' :
                  customer.accountBalance > 0 ? 'text-green-600' : 'text-gray-900'
                }`}>
                  ${Math.abs(customer.accountBalance).toFixed(2)}
                </p>
                {customer.accountBalance < 0 && (
                  <p className="text-xs text-red-600 mt-1">Amount Due</p>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div>
                <p className="text-sm text-gray-600">Next Service</p>
                <p className="text-lg font-semibold text-gray-900 mt-2">{customer.serviceDay}</p>
                <p className="text-xs text-gray-600 mt-1">Weekly service schedule</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="pools">My Pools</TabsTrigger>
            <TabsTrigger value="invoices">Invoices</TabsTrigger>
            <TabsTrigger value="payments">Payment Methods</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Contact Information</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Email</p>
                    <p className="text-base text-gray-900">{customer.email}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Phone</p>
                    <p className="text-base text-gray-900">{customer.phone}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-sm text-gray-600 mb-1">Service Address</p>
                    <p className="text-base text-gray-900">{customer.address}</p>
                  </div>
                </div>
                <Button className="mt-6" variant="outline">Update Information</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recent Service Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {customer.pools[0].chemReadings.slice(0, 3).map((reading, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900">Pool Service Completed</p>
                        <p className="text-sm text-gray-600">{reading.date}</p>
                      </div>
                      <Badge className="bg-green-100 text-green-700">Completed</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Pools Tab */}
          <TabsContent value="pools" className="space-y-6">
            {customer.pools.map((pool) => (
              <Card key={pool.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Droplet style={{ color: pool.color }} />
                      {pool.name}
                    </CardTitle>
                    <Badge variant="outline">{pool.type}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid md:grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Capacity</p>
                        <p className="text-base font-medium text-gray-900">{pool.gallons.toLocaleString()} gallons</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Last Service</p>
                        <p className="text-base font-medium text-gray-900">{pool.lastService}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Equipment</p>
                        <p className="text-base font-medium text-gray-900">{pool.equipment.length} items</p>
                      </div>
                    </div>

                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-3">Latest Chemical Readings</p>
                      {pool.chemReadings[0] && (
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 p-4 bg-blue-50 rounded-lg">
                          <div className="text-center">
                            <p className="text-xs text-gray-600">Free Chlorine</p>
                            <p className="text-lg font-bold text-gray-900 mt-1">{pool.chemReadings[0].fc}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-xs text-gray-600">pH</p>
                            <p className="text-lg font-bold text-gray-900 mt-1">{pool.chemReadings[0].ph}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-xs text-gray-600">Total Alkalinity</p>
                            <p className="text-lg font-bold text-gray-900 mt-1">{pool.chemReadings[0].ta}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-xs text-gray-600">Calcium Hardness</p>
                            <p className="text-lg font-bold text-gray-900 mt-1">{pool.chemReadings[0].ch}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-xs text-gray-600">Cyanuric Acid</p>
                            <p className="text-lg font-bold text-gray-900 mt-1">{pool.chemReadings[0].cya}</p>
                          </div>
                        </div>
                      )}
                    </div>

                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-2">Equipment</p>
                      <div className="flex flex-wrap gap-2">
                        {pool.equipment.map((eq, idx) => (
                          <Badge key={idx} variant="outline">{eq}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Invoices Tab */}
          <TabsContent value="invoices" className="space-y-4">
            {customerInvoices.map((invoice) => (
              <Card key={invoice.id}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-lg text-gray-900">Invoice #{invoice.id}</h3>
                      <p className="text-sm text-gray-600">{invoice.date}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-gray-900">${invoice.total.toFixed(2)}</p>
                      <Badge className={invoice.status === 'paid' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}>
                        {invoice.status}
                      </Badge>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    {invoice.items.map((item, idx) => (
                      <div key={idx} className="flex justify-between text-sm py-2">
                        <span className="text-gray-600">{item.description}</span>
                        <span className="text-gray-900 font-medium">${item.amount.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>

                  <div className="flex gap-2 mt-4">
                    <Button size="sm" variant="outline">
                      <Download className="h-3 w-3 mr-2" />
                      Download
                    </Button>
                    {invoice.status !== 'paid' && (
                      <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white">
                        <CreditCard className="h-3 w-3 mr-2" />
                        Pay Now
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Payment Methods Tab */}
          <TabsContent value="payments">
            <Card>
              <CardHeader>
                <CardTitle>Payment Methods</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {customer.autopay ? (
                    <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <CreditCard className="h-5 w-5 text-green-600" />
                          <div>
                            <p className="font-medium text-gray-900">Autopay Enabled</p>
                            <p className="text-sm text-gray-600">Credit Card ending in ****1234</p>
                          </div>
                        </div>
                        <Badge className="bg-green-100 text-green-700">
                          <CheckCircle className="h-3 w-3 mr-1" />
                          Active
                        </Badge>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-sm text-gray-700">No autopay method configured</p>
                    </div>
                  )}

                  <Button className="w-full md:w-auto">
                    <CreditCard className="h-4 w-4 mr-2" />
                    Add Payment Method
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default CustomerPortal;
