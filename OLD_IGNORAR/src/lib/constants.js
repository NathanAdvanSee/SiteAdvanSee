
import { Monitor, Laptop, Server, Wifi, Smartphone, Printer, CheckCircle, Clock, AlertTriangle } from 'lucide-react';

export const CATEGORIES = {
  desktop: { icon: Monitor, label: 'Desktop', color: 'category-desktop' },
  laptop: { icon: Laptop, label: 'Laptop', color: 'category-laptop' },
  server: { icon: Server, label: 'Servidor', color: 'category-server' },
  network: { icon: Wifi, label: 'Rede', color: 'category-network' },
  mobile: { icon: Smartphone, label: 'Mobile', color: 'category-mobile' },
  printer: { icon: Printer, label: 'Impressora', color: 'category-printer' }
};

export const STATUS_OPTIONS = {
  online: { label: 'Online', color: 'status-online', icon: CheckCircle },
  maintenance: { label: 'Manutenção', color: 'status-maintenance', icon: Clock },
  offline: { label: 'Offline', color: 'status-offline', icon: AlertTriangle }
};

export const INITIAL_EQUIPMENT_DATA = [
  {
    id: 1,
    name: 'Desktop Desenvolvimento 01',
    category: 'desktop',
    status: 'online',
    location: 'Sala 101',
    user: 'João Silva',
    serialNumber: 'DT001-2024',
    purchaseDate: '2024-01-15',
    warranty: '2027-01-15',
    specifications: 'Intel i7, 16GB RAM, 512GB SSD'
  },
  {
    id: 2,
    name: 'Laptop Marketing 02',
    category: 'laptop',
    status: 'maintenance',
    location: 'Sala 205',
    user: 'Maria Santos',
    serialNumber: 'LT002-2024',
    purchaseDate: '2024-02-10',
    warranty: '2027-02-10',
    specifications: 'Intel i5, 8GB RAM, 256GB SSD'
  },
  {
    id: 3,
    name: 'Servidor Principal',
    category: 'server',
    status: 'online',
    location: 'Data Center',
    user: 'Admin',
    serialNumber: 'SV001-2023',
    purchaseDate: '2023-12-01',
    warranty: '2028-12-01',
    specifications: 'Xeon E5, 64GB RAM, 2TB SSD RAID'
  }
];

