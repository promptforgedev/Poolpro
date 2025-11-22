import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Plus, Search, User, Phone, Mail, MapPin, Droplets, CheckCircle, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

const Customers = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BACKEND_URL}/api/customers`);
      if (!response.ok) throw new Error('Failed to fetch customers');
      const data = await response.json();
      setCustomers(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching customers:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.address.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-700';
      case 'paused':
        return 'bg-yellow-100 text-yellow-700';
      case 'inactive':
        return 'bg-gray-100 text-gray-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Customers</h1>
            <p className="text-gray-600 mt-1">Manage your customer accounts and pools</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Add Customer
          </Button>
        </div>

        {/* Search */}
        <Card>
          <CardContent className="pt-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search customers by name, email, or address..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-gray-900">{mockCustomers.length}</p>
                <p className="text-sm text-gray-600 mt-1">Total Customers</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-green-600">
                  {mockCustomers.filter(c => c.status === 'active').length}
                </p>
                <p className="text-sm text-gray-600 mt-1">Active</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-blue-600">
                  {mockCustomers.filter(c => c.autopay).length}
                </p>
                <p className="text-sm text-gray-600 mt-1">Autopay Enabled</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-gray-900">
                  {mockCustomers.reduce((sum, c) => sum + c.pools.length, 0)}
                </p>
                <p className="text-sm text-gray-600 mt-1">Total Pools</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Customer List */}
        <div className="space-y-4">
          {filteredCustomers.map((customer) => (
            <Card key={customer.id} className="hover:shadow-md transition-shadow">
              <CardContent className="pt-6">
                <div className="flex flex-col lg:flex-row gap-6">
                  {/* Customer Avatar */}
                  <div className="flex-shrink-0">
                    <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                      {customer.name.split(' ').map(n => n[0]).join('')}
                    </div>
                  </div>

                  {/* Customer Details */}
                  <div className="flex-1 space-y-4">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900">{customer.name}</h3>
                        <div className="flex flex-wrap gap-4 mt-2 text-sm text-gray-600">
                          <div className="flex items-center gap-2">
                            <Mail className="h-4 w-4" />
                            <span>{customer.email}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Phone className="h-4 w-4" />
                            <span>{customer.phone}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Badge className={getStatusColor(customer.status)}>
                          {customer.status}
                        </Badge>
                        {customer.autopay && (
                          <Badge className="bg-blue-100 text-blue-700">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Autopay
                          </Badge>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <MapPin className="h-4 w-4" />
                      <span>{customer.address}</span>
                    </div>

                    {/* Pools */}
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-2">Pools & Bodies of Water:</p>
                      <div className="flex flex-wrap gap-2">
                        {customer.pools.map((pool) => (
                          <div
                            key={pool.id}
                            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg border"
                            style={{ borderColor: pool.color + '40', backgroundColor: pool.color + '10' }}
                          >
                            <Droplets className="h-4 w-4" style={{ color: pool.color }} />
                            <span className="text-sm font-medium" style={{ color: pool.color }}>
                              {pool.name}
                            </span>
                            <span className="text-xs text-gray-600">
                              ({pool.type})
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Service Info */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Service Day</p>
                        <p className="text-sm font-medium text-gray-900">{customer.serviceDay}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Account Balance</p>
                        <p className={`text-sm font-medium ${
                          customer.accountBalance < 0 ? 'text-red-600' :
                          customer.accountBalance > 0 ? 'text-green-600' : 'text-gray-900'
                        }`}>
                          ${Math.abs(customer.accountBalance).toFixed(2)}
                          {customer.accountBalance < 0 && ' (owed)'}
                          {customer.accountBalance > 0 && ' (credit)'}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Route Position</p>
                        <p className="text-sm font-medium text-gray-900">#{customer.routePosition}</p>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">View Details</Button>
                      <Button size="sm" variant="outline">Edit</Button>
                      <Button size="sm" variant="outline">Service History</Button>
                      <Button size="sm" variant="outline">Create Job</Button>
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

export default Customers;
