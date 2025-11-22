import React from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { mockReports, mockCustomers, mockJobs, mockInvoices, mockAlerts } from '../mock';
import { TrendingUp, TrendingDown, DollarSign, Users, Briefcase, AlertCircle, Download, Calendar } from 'lucide-react';

const Reports = () => {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
            <p className="text-gray-600 mt-1">Track your business performance and metrics</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <Calendar className="h-4 w-4 mr-2" />
              Date Range
            </Button>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    ${mockReports.revenue.thisMonth.toLocaleString()}
                  </p>
                  <div className="flex items-center gap-1 mt-2">
                    <TrendingUp className="h-4 w-4 text-green-600" />
                    <span className="text-sm text-green-600 font-medium">
                      +{mockReports.revenue.percentChange}%
                    </span>
                  </div>
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
                  <p className="text-sm font-medium text-gray-600">Chemical Costs</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    ${mockReports.chemicalCosts.thisMonth.toLocaleString()}
                  </p>
                  <div className="flex items-center gap-1 mt-2">
                    <TrendingDown className="h-4 w-4 text-green-600" />
                    <span className="text-sm text-green-600 font-medium">
                      {Math.abs(mockReports.chemicalCosts.percentChange)}% saved
                    </span>
                  </div>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Customers</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">{mockReports.activeCustomers}</p>
                  <p className="text-sm text-gray-500 mt-2">Total accounts</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completed Jobs</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">{mockReports.completedJobs}</p>
                  <p className="text-sm text-gray-500 mt-2">This month</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Briefcase className="h-6 w-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Performance Charts */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Revenue Breakdown</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Weekly Service</span>
                    <span className="text-sm font-semibold text-gray-900">$8,500</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full" style={{ width: '68%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Repairs & Jobs</span>
                    <span className="text-sm font-semibold text-gray-900">$2,950</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-green-600 h-2 rounded-full" style={{ width: '24%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Chemical Sales</span>
                    <span className="text-sm font-semibold text-gray-900">$1,000</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-purple-600 h-2 rounded-full" style={{ width: '8%' }}></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Customer Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Customers</p>
                    <p className="text-2xl font-bold text-green-700 mt-1">
                      {mockCustomers.filter(c => c.status === 'active').length}
                    </p>
                  </div>
                  <div className="text-4xl">✓</div>
                </div>
                <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Paused Customers</p>
                    <p className="text-2xl font-bold text-yellow-700 mt-1">
                      {mockCustomers.filter(c => c.status === 'paused').length}
                    </p>
                  </div>
                  <div className="text-4xl">⏸</div>
                </div>
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Pools Managed</p>
                    <p className="text-2xl font-bold text-blue-700 mt-1">
                      {mockCustomers.reduce((sum, c) => sum + c.pools.length, 0)}
                    </p>
                  </div>
                  <div className="text-4xl">🏊</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Job Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Job Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center p-6 bg-purple-50 rounded-lg">
                <Briefcase className="h-8 w-8 text-purple-600 mx-auto mb-3" />
                <p className="text-3xl font-bold text-purple-700">{mockJobs.length}</p>
                <p className="text-sm text-gray-600 mt-2">Total Jobs</p>
              </div>
              <div className="text-center p-6 bg-green-50 rounded-lg">
                <Briefcase className="h-8 w-8 text-green-600 mx-auto mb-3" />
                <p className="text-3xl font-bold text-green-700">
                  {mockJobs.filter(j => j.status === 'completed').length}
                </p>
                <p className="text-sm text-gray-600 mt-2">Completed Jobs</p>
              </div>
              <div className="text-center p-6 bg-blue-50 rounded-lg">
                <Briefcase className="h-8 w-8 text-blue-600 mx-auto mb-3" />
                <p className="text-3xl font-bold text-blue-700">
                  {mockJobs.filter(j => j.status === 'in-progress').length}
                </p>
                <p className="text-sm text-gray-600 mt-2">In Progress</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Alert Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Alert Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
                <AlertCircle className="h-6 w-6 text-red-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-red-700">
                  {mockAlerts.filter(a => a.severity === 'high').length}
                </p>
                <p className="text-xs text-gray-600 mt-1">High Priority</p>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <AlertCircle className="h-6 w-6 text-yellow-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-yellow-700">
                  {mockAlerts.filter(a => a.severity === 'medium').length}
                </p>
                <p className="text-xs text-gray-600 mt-1">Medium Priority</p>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg border border-blue-200">
                <AlertCircle className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-blue-700">
                  {mockAlerts.filter(a => a.severity === 'low').length}
                </p>
                <p className="text-xs text-gray-600 mt-1">Low Priority</p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg border border-gray-200">
                <AlertCircle className="h-6 w-6 text-gray-600 mx-auto mb-2" />
                <p className="text-2xl font-bold text-gray-700">{mockAlerts.length}</p>
                <p className="text-xs text-gray-600 mt-1">Total Alerts</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Financial Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Financial Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
                <DollarSign className="h-8 w-8 text-green-600 mb-3" />
                <p className="text-sm text-gray-600">Total Invoiced</p>
                <p className="text-3xl font-bold text-green-700 mt-2">
                  ${mockInvoices.reduce((sum, inv) => sum + inv.total, 0).toLocaleString()}
                </p>
              </div>
              <div className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                <DollarSign className="h-8 w-8 text-blue-600 mb-3" />
                <p className="text-sm text-gray-600">Collected</p>
                <p className="text-3xl font-bold text-blue-700 mt-2">
                  ${mockInvoices.filter(i => i.status === 'paid').reduce((sum, inv) => sum + inv.total, 0).toLocaleString()}
                </p>
              </div>
              <div className="p-6 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg">
                <DollarSign className="h-8 w-8 text-orange-600 mb-3" />
                <p className="text-sm text-gray-600">Outstanding</p>
                <p className="text-3xl font-bold text-orange-700 mt-2">
                  ${mockInvoices.filter(i => i.status !== 'paid' && i.status !== 'draft').reduce((sum, inv) => sum + inv.total, 0).toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Reports;
