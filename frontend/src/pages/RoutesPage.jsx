import React, { useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockRoutes, mockTechnicians } from '../mock';
import { MapPin, Clock, Navigation, CheckCircle, Loader, Calendar } from 'lucide-react';

const RoutesPage = () => {
  const [selectedDay, setSelectedDay] = useState('Monday');

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'in-progress':
        return <Loader className="h-4 w-4 text-blue-600 animate-spin" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-700';
      case 'in-progress':
        return 'bg-blue-100 text-blue-700';
      case 'scheduled':
        return 'bg-gray-100 text-gray-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const currentRoute = mockRoutes.find(r => r.day === selectedDay);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Route Scheduling</h1>
            <p className="text-gray-600 mt-1">Manage and optimize your service routes</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline">
              <Navigation className="h-4 w-4 mr-2" />
              Optimize Routes
            </Button>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Calendar className="h-4 w-4 mr-2" />
              Bulk Schedule
            </Button>
          </div>
        </div>

        {/* Day Tabs */}
        <Card>
          <CardContent className="pt-6">
            <Tabs value={selectedDay} onValueChange={setSelectedDay}>
              <TabsList className="grid w-full grid-cols-5">
                {days.map(day => (
                  <TabsTrigger key={day} value={day}>{day}</TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
          </CardContent>
        </Card>

        {/* Technician Info */}
        {currentRoute && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-lg font-semibold">
                    {currentRoute.technicianName.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <CardTitle className="text-lg">{currentRoute.technicianName}</CardTitle>
                    <p className="text-sm text-gray-600">{currentRoute.stops.length} stops scheduled</p>
                  </div>
                </div>
                <Badge className="bg-green-100 text-green-700">Active</Badge>
              </div>
            </CardHeader>
          </Card>
        )}

        {/* Route Stops */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Route Stops</h2>
          {currentRoute ? (
            currentRoute.stops.map((stop) => (
              <Card key={stop.id} className="hover:shadow-md transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex items-start gap-4">
                    {/* Position Badge */}
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-bold">
                        {stop.position}
                      </div>
                    </div>

                    {/* Stop Details */}
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-gray-900 text-lg">{stop.customerName}</h3>
                          <div className="flex items-center gap-2 text-sm text-gray-600 mt-1">
                            <MapPin className="h-4 w-4" />
                            <span>{stop.address}</span>
                          </div>
                        </div>
                        <Badge className={getStatusColor(stop.status)}>
                          {getStatusIcon(stop.status)}
                          <span className="ml-2 capitalize">{stop.status}</span>
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Time Window</p>
                          <p className="text-sm font-medium text-gray-900">{stop.timeWindow}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Est. Time</p>
                          <p className="text-sm font-medium text-gray-900">{stop.estimatedTime} min</p>
                        </div>
                        <div className="col-span-2">
                          <p className="text-xs text-gray-600 mb-1">Notes</p>
                          <p className="text-sm font-medium text-gray-900">{stop.notes}</p>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-2 mt-4">
                        <Button size="sm" variant="outline">View Details</Button>
                        <Button size="sm" variant="outline">Reschedule</Button>
                        <Button size="sm" variant="outline">Remove</Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <Card>
              <CardContent className="pt-6 text-center py-12">
                <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No routes scheduled for {selectedDay}</p>
                <Button className="mt-4" variant="outline">Add Route Stop</Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default RoutesPage;
