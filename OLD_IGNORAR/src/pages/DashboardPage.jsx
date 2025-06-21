
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Monitor, 
  Laptop, 
  Server, 
  Wifi, 
  Smartphone, 
  Printer,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  HardDrive
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from '@/components/ui/use-toast';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DropdownMenu } from '@/components/ui/dropdown-menu';
import { Tabs } from '@/components/ui/tabs';
import EquipmentDetailsModal from '@/components/EquipmentDetailsModal';
import StatsCard from '@/components/StatsCard';
import CategoryStatsCard from '@/components/CategoryStatsCard';
import RecentActivityItem from '@/components/RecentActivityItem';
import EquipmentCard from '@/components/EquipmentCard';
import { CATEGORIES, STATUS_OPTIONS, INITIAL_EQUIPMENT_DATA } from '@/lib/constants';

function DashboardPage() {
  const [equipment, setEquipment] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const savedEquipment = localStorage.getItem('itInventory');
    if (savedEquipment) {
      setEquipment(JSON.parse(savedEquipment));
    } else {
      setEquipment(INITIAL_EQUIPMENT_DATA);
      localStorage.setItem('itInventory', JSON.stringify(INITIAL_EQUIPMENT_DATA));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('itInventory', JSON.stringify(equipment));
  }, [equipment]);

  const filteredEquipment = equipment.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (item.user && item.user.toLowerCase().includes(searchTerm.toLowerCase())) ||
                         (item.location && item.location.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesStatus = selectedStatus === 'all' || item.status === selectedStatus;
    
    return matchesSearch && matchesCategory && matchesStatus;
  });

  const getStats = () => {
    const total = equipment.length;
    const online = equipment.filter(item => item.status === 'online').length;
    const maintenance = equipment.filter(item => item.status === 'maintenance').length;
    const offline = equipment.filter(item => item.status === 'offline').length;
    
    return { total, online, maintenance, offline };
  };

  const getCategoryStats = () => {
    return Object.keys(CATEGORIES).map(categoryKey => ({
      category: categoryKey,
      count: equipment.filter(item => item.category === categoryKey).length,
      ...CATEGORIES[categoryKey]
    }));
  };

  const handleAddEquipment = () => {
    toast({
      title: "🚧 Esta funcionalidade ainda não foi implementada—mas não se preocupe! Você pode solicitá-la no seu próximo prompt! 🚀"
    });
  };

  const handleEditEquipment = (item) => {
    toast({
      title: "🚧 Esta funcionalidade ainda não foi implementada—mas não se preocupe! Você pode solicitá-la no seu próximo prompt! 🚀"
    });
  };

  const handleDeleteEquipment = (item) => {
    toast({
      title: "🚧 Esta funcionalidade ainda não foi implementada—mas não se preocupe! Você pode solicitá-la no seu próximo prompt! 🚀"
    });
  };

  const handleViewDetails = (item) => {
    setSelectedEquipment(item);
  };

  const stats = getStats();
  const categoryStats = getCategoryStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="container mx-auto p-6 space-y-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-4"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
            Dashboard de Inventário de TI
          </h1>
          <p className="text-xl text-slate-300">
            Gerencie todos os seus equipamentos de TI em um só lugar
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          <StatsCard label="Total de Equipamentos" value={stats.total} icon={HardDrive} color="text-green-400" borderColor="border-green-500/20" />
          <StatsCard label="Online" value={stats.online} icon={CheckCircle} color="text-blue-400" borderColor="border-blue-500/20" />
          <StatsCard label="Manutenção" value={stats.maintenance} icon={Clock} color="text-yellow-400" borderColor="border-yellow-500/20" />
          <StatsCard label="Offline" value={stats.offline} icon={AlertTriangle} color="text-red-400" borderColor="border-red-500/20" />
        </motion.div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <div className="flex justify-center mb-8">
            <div className="glass-effect rounded-lg p-1">
              <Button
                variant={activeTab === 'overview' ? 'default' : 'ghost'}
                onClick={() => setActiveTab('overview')}
                className="mr-2"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Visão Geral
              </Button>
              <Button
                variant={activeTab === 'equipment' ? 'default' : 'ghost'}
                onClick={() => setActiveTab('equipment')}
              >
                <Monitor className="h-4 w-4 mr-2" />
                Equipamentos
              </Button>
            </div>
          </div>

          {activeTab === 'overview' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <Card className="glass-effect p-6">
                <h3 className="text-2xl font-bold mb-6 text-center">Equipamentos por Categoria</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  {categoryStats.map((stat) => (
                    <CategoryStatsCard key={stat.category} {...stat} />
                  ))}
                </div>
              </Card>

              <Card className="glass-effect p-6">
                <h3 className="text-2xl font-bold mb-6">Atividade Recente</h3>
                <div className="space-y-4">
                  <RecentActivityItem icon={CheckCircle} color="text-green-400" text="Desktop Desenvolvimento 01 voltou online" time="Há 2 horas" />
                  <RecentActivityItem icon={Clock} color="text-yellow-400" text="Laptop Marketing 02 entrou em manutenção" time="Há 4 horas" />
                  <RecentActivityItem icon={Plus} color="text-blue-400" text="Novo servidor adicionado ao inventário" time="Ontem" />
                </div>
              </Card>
            </motion.div>
          )}

          {activeTab === 'equipment' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <Card className="glass-effect p-6">
                <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
                  <div className="flex flex-col sm:flex-row gap-4 flex-1">
                    <div className="relative flex-1 max-w-md">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                      <Input
                        placeholder="Buscar equipamentos..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10 bg-slate-800/50 border-slate-600"
                      />
                    </div>
                    
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="px-4 py-2 bg-slate-800/50 border border-slate-600 rounded-md text-white"
                    >
                      <option value="all">Todas as Categorias</option>
                      {Object.entries(CATEGORIES).map(([key, { label }]) => (
                        <option key={key} value={key}>{label}</option>
                      ))}
                    </select>

                    <select
                      value={selectedStatus}
                      onChange={(e) => setSelectedStatus(e.target.value)}
                      className="px-4 py-2 bg-slate-800/50 border border-slate-600 rounded-md text-white"
                    >
                      <option value="all">Todos os Status</option>
                      {Object.entries(STATUS_OPTIONS).map(([key, { label }]) => (
                        <option key={key} value={key}>{label}</option>
                      ))}
                    </select>
                  </div>

                  <Button onClick={handleAddEquipment} className="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600">
                    <Plus className="h-4 w-4 mr-2" />
                    Adicionar Equipamento
                  </Button>
                </div>
              </Card>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <AnimatePresence>
                  {filteredEquipment.map((item) => (
                    <EquipmentCard
                      key={item.id}
                      item={item}
                      onViewDetails={handleViewDetails}
                      onEdit={handleEditEquipment}
                      onDelete={handleDeleteEquipment}
                    />
                  ))}
                </AnimatePresence>
              </div>

              {filteredEquipment.length === 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12"
                >
                  <Monitor className="h-16 w-16 text-slate-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-slate-300 mb-2">
                    Nenhum equipamento encontrado
                  </h3>
                  <p className="text-slate-400">
                    Tente ajustar os filtros ou adicionar novos equipamentos
                  </p>
                </motion.div>
              )}
            </motion.div>
          )}
        </Tabs>

        <EquipmentDetailsModal
          equipment={selectedEquipment}
          onClose={() => setSelectedEquipment(null)}
          onEdit={handleEditEquipment}
          onDelete={handleDeleteEquipment}
        />
      </div>
    </div>
  );
}

export default DashboardPage;
