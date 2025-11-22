import React, { useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockJobs } from '../mock';
import { Plus, Search, Briefcase, Clock, DollarSign, User } from 'lucide-react';

const Jobs = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-700';
      case 'in-progress':
        return 'bg-blue-100 text-blue-700';
      case 'scheduled':
        return 'bg-purple-100 text-purple-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getJobTypeColor = (type) => {
    switch (type) {
      case 'filter-clean':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'repair':
        return 'bg-orange-50 text-orange-700 border-orange-200';
      case 'equipment-install':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'green-pool':
        return 'bg-green-50 text-green-700 border-green-200';
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200';
    }
  };

  const filteredJobs = mockJobs.filter(job => {
    const matchesSearch = job.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || job.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const jobCounts = {
    all: mockJobs.length,
    scheduled: mockJobs.filter(j => j.status === 'scheduled').length,
    'in-progress': mockJobs.filter(j => j.status === 'in-progress').length,
    completed: mockJobs.filter(j => j.status === 'completed').length
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Jobs</h1>
            <p className="text-gray-600 mt-1">Manage all your service jobs and tasks</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Create New Job
          </Button>
        </div>

        {/* Search and Filter */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search jobs or customers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Tabs value={statusFilter} onValueChange={setStatusFilter} className="w-full md:w-auto">
                <TabsList>
                  <TabsTrigger value="all">All ({jobCounts.all})</TabsTrigger>
                  <TabsTrigger value="scheduled">Scheduled ({jobCounts.scheduled})</TabsTrigger>
                  <TabsTrigger value="in-progress">In Progress ({jobCounts['in-progress']})</TabsTrigger>
                  <TabsTrigger value="completed">Completed ({jobCounts.completed})</TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </CardContent>
        </Card>

        {/* Jobs List */}
        <div className="space-y-4">
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job) => (
              <Card key={job.id} className="hover:shadow-md transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    {/* Job Icon */}
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Briefcase className="h-6 w-6 text-blue-600" />
                      </div>
                    </div>

                    {/* Job Details */}
                    <div className="flex-1 space-y-3">
                      <div className="flex flex-wrap items-start justify-between gap-2">
                        <div>
                          <h3 className="font-semibold text-lg text-gray-900">{job.title}</h3>
                          <p className="text-sm text-gray-600 mt-1">{job.customerName}</p>
                        </div>
                        <div className="flex gap-2">
                          <Badge className={getJobTypeColor(job.type)} variant="outline">
                            {job.type.replace('-', ' ')}
                          </Badge>
                          <Badge className={getStatusColor(job.status)}>
                            {job.status}
                          </Badge>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="flex items-center gap-2 text-sm">
                          <User className="h-4 w-4 text-gray-400" />
                          <span className="text-gray-600">{job.technicianName}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <Clock className="h-4 w-4 text-gray-400" />
                          <span className="text-gray-600">{job.scheduledDate}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <Clock className="h-4 w-4 text-gray-400" />
                          <span className="text-gray-600">{job.estimatedTime} min</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <DollarSign className="h-4 w-4 text-gray-400" />
                          <span className="text-gray-600 font-semibold">${job.price.toFixed(2)}</span>
                        </div>
                      </div>

                      {job.notes && (
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <p className="text-sm text-gray-700">
                            <span className="font-medium">Notes:</span> {job.notes}
                          </p>
                        </div>
                      )}

                      {/* Actions */}
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">View Details</Button>
                        {job.status === 'scheduled' && (
                          <Button size="sm" variant="outline">Start Job</Button>
                        )}
                        {job.status === 'in-progress' && (
                          <Button size="sm" className="bg-green-600 hover:bg-green-700 text-white">
                            Complete Job
                          </Button>
                        )}
                        <Button size="sm" variant="outline">Edit</Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <Card>
              <CardContent className="pt-6 text-center py-12">
                <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No jobs found matching your criteria</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Jobs;
