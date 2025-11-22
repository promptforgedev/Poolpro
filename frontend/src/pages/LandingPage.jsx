import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Droplets, CheckCircle, Zap, TrendingUp, Users, Shield, ArrowRight, Star } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Quotes',
      description: 'Add labels and pictures to line items in the field or on the web. Send to customer with a tap. Job is auto-created when approved.',
      icon: CheckCircle
    },
    {
      title: 'Jobs',
      description: 'Use one time job templates to add common or complex workflows in seconds. Invoice is auto-created when job is closed.',
      icon: Zap
    },
    {
      title: 'Invoices & Payments',
      description: 'Create and manage all your invoices/payments directly in Pool Pro. Automatic or manual billing. Per visit or flat rate. Advance or arrears.',
      icon: TrendingUp
    },
    {
      title: 'Routing',
      description: 'Optimize with one click. Drag & drop anything anywhere. One time moves easily cover the unexpected. Real time progress indicators.',
      icon: Users
    },
    {
      title: 'Guided Workflows',
      description: "Tasks can't be skipped, forgotten or cheated. Correct actions are performed at the correct times. Less training, mistakes and turnover.",
      icon: Shield
    },
    {
      title: 'Custom Alerts',
      description: 'Never do random follow ups in the heat again or search through reports for potential issues. Chemicals, Flow, Leaks, Time, Cost and more.',
      icon: Star
    }
  ];

  const companies = [
    'ASP Pool Service',
    'Keith Zars Pools',
    'Riverbend Pools',
    'Shasta Pools',
    'Tortorella Pools',
    'Poolie'
  ];

  const stats = [
    { value: '36%', label: 'Reduced Chem Spend' },
    { value: '60%', label: 'Less Training Time' },
    { value: '78%', label: 'Fewer Green Pools' },
    { value: '84%', label: 'Fewer Complaint Calls' }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-2 rounded-lg">
                <Droplets className="h-6 w-6" />
              </div>
              <span className="text-xl font-bold text-gray-900">PoolPro</span>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => navigate('/portal')}>Customer Portal</Button>
              <Button onClick={() => navigate('/dashboard')}>Dashboard</Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Pool Company Software that{' '}
              <span className="text-blue-600">optimizes everything</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              A modern "all in one" solution built by industry experts to give you more time, more money and less stress
            </p>
            <div className="flex items-center justify-center gap-4">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white" onClick={() => navigate('/dashboard')}>
                View Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline">30 Day Free Trial</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Companies Section */}
      <section className="bg-gray-50 py-12 border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm font-semibold text-gray-500 uppercase tracking-wider mb-8">
            The largest companies in the industry run on PoolPro
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center">
            {companies.map((company) => (
              <div key={company} className="text-center">
                <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                  <p className="text-sm font-semibold text-gray-700">{company}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            {stats.map((stat, index) => (
              <div key={index}>
                <div className="text-4xl lg:text-5xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-blue-100 text-sm font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Quotes become jobs. Jobs become invoices. Automatically.
            </h2>
            <p className="text-xl text-gray-600">Streamline your entire workflow from start to finish</p>
          </div>
          <div className="bg-white rounded-2xl shadow-xl p-8 lg:p-12">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">1</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Create Quote</h3>
                <p className="text-gray-600">Send professional quotes with photos and line items</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">2</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Auto-Create Job</h3>
                <p className="text-gray-600">When approved, job is automatically created and scheduled</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">3</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Auto-Invoice</h3>
                <p className="text-gray-600">Invoice is created when job completes and sent automatically</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Ready to optimize your pool business?</h2>
          <p className="text-xl text-gray-600 mb-8">Join hundreds of pool companies using PoolPro</p>
          <div className="flex items-center justify-center gap-4">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white" onClick={() => navigate('/dashboard')}>
              Get Started Free
            </Button>
            <Button size="lg" variant="outline">Schedule Demo</Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="bg-blue-600 text-white p-2 rounded-lg">
                <Droplets className="h-6 w-6" />
              </div>
              <span className="text-xl font-bold">PoolPro</span>
            </div>
            <p className="text-gray-400">© 2025 PoolPro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
