// Mock data for PoolBrain clone

export const mockCustomers = [
  {
    id: 'cust-1',
    name: 'John Anderson',
    email: 'john.anderson@email.com',
    phone: '(555) 123-4567',
    address: '1234 Oak Street, Austin, TX 78701',
    status: 'active',
    accountBalance: 0,
    serviceDay: 'Monday',
    routePosition: 1,
    autopay: true,
    pools: [
      {
        id: 'pool-1',
        name: 'Main Pool',
        type: 'In-Ground',
        color: '#3B82F6',
        gallons: 25000,
        equipment: ['Pump', 'Filter', 'Heater', 'Salt Cell'],
        lastService: '2025-01-15',
        chemReadings: [
          { date: '2025-01-15', fc: 3.2, ph: 7.4, ta: 120, ch: 250, cya: 50 },
          { date: '2025-01-08', fc: 2.8, ph: 7.6, ta: 115, ch: 240, cya: 50 },
          { date: '2025-01-01', fc: 3.5, ph: 7.2, ta: 125, ch: 260, cya: 50 }
        ]
      }
    ]
  },
  {
    id: 'cust-2',
    name: 'Sarah Mitchell',
    email: 'sarah.mitchell@email.com',
    phone: '(555) 234-5678',
    address: '5678 Pine Avenue, Austin, TX 78702',
    status: 'active',
    accountBalance: -125.50,
    serviceDay: 'Monday',
    routePosition: 2,
    autopay: false,
    pools: [
      {
        id: 'pool-2',
        name: 'Main Pool',
        type: 'In-Ground',
        color: '#3B82F6',
        gallons: 18000,
        equipment: ['Pump', 'Filter', 'Salt Cell'],
        lastService: '2025-01-15',
        chemReadings: [
          { date: '2025-01-15', fc: 2.5, ph: 7.8, ta: 140, ch: 280, cya: 60 },
          { date: '2025-01-08', fc: 2.2, ph: 7.9, ta: 145, ch: 290, cya: 60 }
        ]
      },
      {
        id: 'pool-3',
        name: 'Spa',
        type: 'Spa/Hot Tub',
        color: '#F59E0B',
        gallons: 400,
        equipment: ['Heater', 'Jets'],
        lastService: '2025-01-15',
        chemReadings: [
          { date: '2025-01-15', fc: 4.0, ph: 7.5, ta: 100, ch: 180, cya: 30 }
        ]
      }
    ]
  },
  {
    id: 'cust-3',
    name: 'Michael Torres',
    email: 'michael.torres@email.com',
    phone: '(555) 345-6789',
    address: '9012 Elm Drive, Austin, TX 78703',
    status: 'active',
    accountBalance: 75.00,
    serviceDay: 'Tuesday',
    routePosition: 1,
    autopay: true,
    pools: [
      {
        id: 'pool-4',
        name: 'Pool',
        type: 'Above-Ground',
        color: '#10B981',
        gallons: 15000,
        equipment: ['Pump', 'Filter'],
        lastService: '2025-01-14',
        chemReadings: [
          { date: '2025-01-14', fc: 3.0, ph: 7.3, ta: 110, ch: 230, cya: 45 }
        ]
      }
    ]
  },
  {
    id: 'cust-4',
    name: 'Emily Roberts',
    email: 'emily.roberts@email.com',
    phone: '(555) 456-7890',
    address: '3456 Maple Court, Austin, TX 78704',
    status: 'active',
    accountBalance: 0,
    serviceDay: 'Wednesday',
    routePosition: 1,
    autopay: true,
    pools: [
      {
        id: 'pool-5',
        name: 'Main Pool',
        type: 'In-Ground',
        color: '#3B82F6',
        gallons: 30000,
        equipment: ['Pump', 'Filter', 'Heater', 'Salt Cell', 'Automation'],
        lastService: '2025-01-13',
        chemReadings: [
          { date: '2025-01-13', fc: 3.8, ph: 7.2, ta: 105, ch: 220, cya: 40 }
        ]
      }
    ]
  },
  {
    id: 'cust-5',
    name: 'David Chen',
    email: 'david.chen@email.com',
    phone: '(555) 567-8901',
    address: '7890 Cedar Lane, Austin, TX 78705',
    status: 'paused',
    accountBalance: 0,
    serviceDay: 'Thursday',
    routePosition: 1,
    autopay: false,
    pools: [
      {
        id: 'pool-6',
        name: 'Pool',
        type: 'In-Ground',
        color: '#3B82F6',
        gallons: 22000,
        equipment: ['Pump', 'Filter'],
        lastService: '2024-12-28',
        chemReadings: [
          { date: '2024-12-28', fc: 2.9, ph: 7.5, ta: 115, ch: 245, cya: 55 }
        ]
      }
    ]
  }
];

export const mockAlerts = [
  {
    id: 'alert-1',
    customerId: 'cust-2',
    customerName: 'Sarah Mitchell',
    poolId: 'pool-2',
    poolName: 'Main Pool',
    type: 'chemical',
    severity: 'high',
    title: 'High pH Reading',
    description: 'pH reading of 7.8 is above recommended range (7.2-7.6)',
    date: '2025-01-15',
    status: 'open'
  },
  {
    id: 'alert-2',
    customerId: 'cust-2',
    customerName: 'Sarah Mitchell',
    poolId: 'pool-2',
    poolName: 'Main Pool',
    type: 'chemical',
    severity: 'medium',
    title: 'Low Free Chlorine',
    description: 'FC reading of 2.5 is below optimal range (3.0-5.0)',
    date: '2025-01-15',
    status: 'open'
  },
  {
    id: 'alert-3',
    customerId: 'cust-1',
    customerName: 'John Anderson',
    poolId: 'pool-1',
    poolName: 'Main Pool',
    type: 'time',
    severity: 'low',
    title: 'Service Time Extended',
    description: 'Service took 45 minutes (avg: 30 minutes)',
    date: '2025-01-15',
    status: 'open'
  },
  {
    id: 'alert-4',
    customerId: 'cust-1',
    customerName: 'John Anderson',
    poolId: 'pool-1',
    poolName: 'Main Pool',
    type: 'equipment',
    severity: 'high',
    title: 'Filter Clean Due',
    description: 'Filter clean is 2 weeks overdue',
    date: '2025-01-14',
    status: 'open'
  }
];

export const mockJobs = [
  {
    id: 'job-1',
    customerId: 'cust-1',
    customerName: 'John Anderson',
    type: 'filter-clean',
    title: 'Filter Clean + Salt Cell',
    status: 'scheduled',
    scheduledDate: '2025-01-18',
    assignedTo: 'tech-1',
    technicianName: 'Mike Johnson',
    estimatedTime: 60,
    price: 125.00,
    notes: 'Customer mentioned filter pressure has been high'
  },
  {
    id: 'job-2',
    customerId: 'cust-2',
    customerName: 'Sarah Mitchell',
    type: 'repair',
    title: 'Pool Pump Repair',
    status: 'in-progress',
    scheduledDate: '2025-01-16',
    assignedTo: 'tech-2',
    technicianName: 'Carlos Rodriguez',
    estimatedTime: 120,
    price: 350.00,
    notes: 'Pump making loud noise, possible bearing issue'
  },
  {
    id: 'job-3',
    customerId: 'cust-4',
    customerName: 'Emily Roberts',
    type: 'equipment-install',
    title: 'Install New Pool Light',
    status: 'completed',
    scheduledDate: '2025-01-15',
    completedDate: '2025-01-15',
    assignedTo: 'tech-1',
    technicianName: 'Mike Johnson',
    estimatedTime: 90,
    actualTime: 85,
    price: 425.00,
    notes: 'LED color-changing light installation'
  },
  {
    id: 'job-4',
    customerId: 'cust-3',
    customerName: 'Michael Torres',
    type: 'green-pool',
    title: 'Green Pool Treatment',
    status: 'scheduled',
    scheduledDate: '2025-01-17',
    assignedTo: 'tech-2',
    technicianName: 'Carlos Rodriguez',
    estimatedTime: 45,
    price: 150.00,
    notes: 'Pool turned green after owner was away'
  }
];

export const mockQuotes = [
  {
    id: 'quote-1',
    customerId: 'cust-1',
    customerName: 'John Anderson',
    title: 'Heater Replacement',
    status: 'pending',
    createdDate: '2025-01-14',
    expiryDate: '2025-01-28',
    items: [
      { name: 'Hayward H400 Heater', quantity: 1, price: 2500.00 },
      { name: 'Installation & Labor', quantity: 1, price: 500.00 },
      { name: 'Gas Line Connection', quantity: 1, price: 300.00 }
    ],
    total: 3300.00,
    notes: 'Current heater is 15 years old and inefficient'
  },
  {
    id: 'quote-2',
    customerId: 'cust-2',
    customerName: 'Sarah Mitchell',
    title: 'Weekly Pool Service',
    status: 'approved',
    createdDate: '2025-01-10',
    approvedDate: '2025-01-12',
    items: [
      { name: 'Weekly Service (Monthly)', quantity: 1, price: 150.00 }
    ],
    total: 150.00,
    notes: 'Started service on 01/15/2025'
  },
  {
    id: 'quote-3',
    customerId: 'cust-4',
    customerName: 'Emily Roberts',
    title: 'Salt Cell Replacement',
    status: 'declined',
    createdDate: '2025-01-08',
    declinedDate: '2025-01-10',
    items: [
      { name: 'Pentair IC40 Salt Cell', quantity: 1, price: 750.00 },
      { name: 'Installation', quantity: 1, price: 100.00 }
    ],
    total: 850.00,
    notes: 'Customer decided to wait until spring'
  }
];

export const mockInvoices = [
  {
    id: 'inv-1001',
    customerId: 'cust-1',
    customerName: 'John Anderson',
    date: '2025-01-15',
    dueDate: '2025-02-01',
    status: 'paid',
    paidDate: '2025-01-16',
    items: [
      { description: 'Weekly Pool Service', quantity: 4, rate: 37.50, amount: 150.00 },
      { description: 'Chemicals (Chlorine)', quantity: 1, rate: 25.00, amount: 25.00 }
    ],
    subtotal: 175.00,
    tax: 0,
    total: 175.00,
    paymentMethod: 'credit-card'
  },
  {
    id: 'inv-1002',
    customerId: 'cust-2',
    customerName: 'Sarah Mitchell',
    date: '2025-01-15',
    dueDate: '2025-02-01',
    status: 'overdue',
    items: [
      { description: 'Weekly Pool Service', quantity: 4, rate: 37.50, amount: 150.00 },
      { description: 'Chemicals (Acid)', quantity: 1, rate: 15.50, amount: 15.50 },
      { description: 'Filter Clean', quantity: 1, rate: 75.00, amount: 75.00 }
    ],
    subtotal: 240.50,
    tax: 0,
    total: 240.50,
    paymentMethod: 'unpaid'
  },
  {
    id: 'inv-1003',
    customerId: 'cust-3',
    customerName: 'Michael Torres',
    date: '2025-01-14',
    dueDate: '2025-02-01',
    status: 'sent',
    items: [
      { description: 'Weekly Pool Service', quantity: 4, rate: 35.00, amount: 140.00 }
    ],
    subtotal: 140.00,
    tax: 0,
    total: 140.00,
    paymentMethod: 'unpaid'
  },
  {
    id: 'inv-1004',
    customerId: 'cust-4',
    customerName: 'Emily Roberts',
    date: '2025-01-13',
    dueDate: '2025-02-01',
    status: 'draft',
    items: [
      { description: 'Weekly Pool Service', quantity: 4, rate: 40.00, amount: 160.00 },
      { description: 'Pool Light Installation', quantity: 1, rate: 425.00, amount: 425.00 }
    ],
    subtotal: 585.00,
    tax: 0,
    total: 585.00,
    paymentMethod: 'unpaid'
  }
];

export const mockTechnicians = [
  {
    id: 'tech-1',
    name: 'Mike Johnson',
    email: 'mike.j@poolpro.com',
    phone: '(555) 111-2222',
    avatar: 'MJ',
    status: 'active',
    assignedRoutes: ['Monday', 'Tuesday'],
    completedJobs: 245,
    avgServiceTime: 32
  },
  {
    id: 'tech-2',
    name: 'Carlos Rodriguez',
    email: 'carlos.r@poolpro.com',
    phone: '(555) 222-3333',
    avatar: 'CR',
    status: 'active',
    assignedRoutes: ['Wednesday', 'Thursday'],
    completedJobs: 198,
    avgServiceTime: 28
  },
  {
    id: 'tech-3',
    name: 'Sarah Kim',
    email: 'sarah.k@poolpro.com',
    phone: '(555) 333-4444',
    avatar: 'SK',
    status: 'active',
    assignedRoutes: ['Friday'],
    completedJobs: 167,
    avgServiceTime: 30
  }
];

export const mockRoutes = [
  {
    day: 'Monday',
    technicianId: 'tech-1',
    technicianName: 'Mike Johnson',
    stops: [
      {
        id: 'stop-1',
        customerId: 'cust-1',
        customerName: 'John Anderson',
        address: '1234 Oak Street',
        position: 1,
        estimatedTime: 30,
        status: 'completed',
        timeWindow: '8:00 AM - 9:00 AM',
        notes: 'Code 1234 for gate'
      },
      {
        id: 'stop-2',
        customerId: 'cust-2',
        customerName: 'Sarah Mitchell',
        address: '5678 Pine Avenue',
        position: 2,
        estimatedTime: 35,
        status: 'completed',
        timeWindow: '9:30 AM - 10:30 AM',
        notes: 'Two pools - Main + Spa'
      }
    ]
  },
  {
    day: 'Tuesday',
    technicianId: 'tech-1',
    technicianName: 'Mike Johnson',
    stops: [
      {
        id: 'stop-3',
        customerId: 'cust-3',
        customerName: 'Michael Torres',
        address: '9012 Elm Drive',
        position: 1,
        estimatedTime: 25,
        status: 'in-progress',
        timeWindow: '8:00 AM - 9:00 AM',
        notes: 'Above ground pool'
      }
    ]
  },
  {
    day: 'Wednesday',
    technicianId: 'tech-2',
    technicianName: 'Carlos Rodriguez',
    stops: [
      {
        id: 'stop-4',
        customerId: 'cust-4',
        customerName: 'Emily Roberts',
        address: '3456 Maple Court',
        position: 1,
        estimatedTime: 35,
        status: 'scheduled',
        timeWindow: '8:00 AM - 9:00 AM',
        notes: 'Large pool with automation'
      }
    ]
  }
];

export const mockReports = {
  revenue: {
    thisMonth: 12450.00,
    lastMonth: 11200.00,
    percentChange: 11.2
  },
  chemicalCosts: {
    thisMonth: 1850.00,
    lastMonth: 1920.00,
    percentChange: -3.6
  },
  activeCustomers: 42,
  pendingInvoices: 8,
  completedJobs: 178,
  openAlerts: 12
};
