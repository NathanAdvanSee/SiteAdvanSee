
import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { DropdownMenu } from '@/components/ui/dropdown-menu';
import { MoreVertical, Eye, Edit, Trash2 } from 'lucide-react';
import { CATEGORIES, STATUS_OPTIONS } from '@/lib/constants';

const EquipmentCard = ({ item, onViewDetails, onEdit, onDelete }) => {
  const CategoryIcon = CATEGORIES[item.category]?.icon;
  const StatusIcon = STATUS_OPTIONS[item.status]?.icon;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      whileHover={{ y: -5 }}
      className="group"
    >
      <Card className="glass-effect p-6 h-full hover:border-green-500/40 transition-all duration-300">
        <div className="flex items-start justify-between mb-4">
          {CategoryIcon && (
            <div className={`p-3 rounded-lg ${CATEGORIES[item.category]?.color || ''}`}>
              <CategoryIcon className="h-6 w-6 text-white" />
            </div>
          )}
          <DropdownMenu>
            <Button variant="ghost" size="icon" className="opacity-0 group-hover:opacity-100 transition-opacity">
              <MoreVertical className="h-4 w-4" />
            </Button>
            <div className="bg-slate-800 border border-slate-600 rounded-md p-1 space-y-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onViewDetails(item)}
                className="w-full justify-start"
              >
                <Eye className="h-4 w-4 mr-2" />
                Ver Detalhes
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onEdit(item)}
                className="w-full justify-start"
              >
                <Edit className="h-4 w-4 mr-2" />
                Editar
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDelete(item)}
                className="w-full justify-start text-red-400 hover:text-red-300"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Excluir
              </Button>
            </div>
          </DropdownMenu>
        </div>

        <div className="space-y-3">
          <div>
            <h3 className="font-bold text-lg text-white">{item.name}</h3>
            <p className="text-slate-400">{item.serialNumber}</p>
          </div>

          <div className="flex items-center space-x-2">
            <Badge className={`${STATUS_OPTIONS[item.status]?.color || ''} text-white border-0`}>
              {StatusIcon && <StatusIcon className="h-3 w-3 mr-1" />}
              {STATUS_OPTIONS[item.status]?.label || item.status}
            </Badge>
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Usuário:</span>
              <span className="text-white">{item.user}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Local:</span>
              <span className="text-white">{item.location}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Categoria:</span>
              <span className="text-white">{CATEGORIES[item.category]?.label || item.category}</span>
            </div>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => onViewDetails(item)}
            className="w-full mt-4 border-green-500/30 hover:border-green-500/60 hover:bg-green-500/10"
          >
            Ver Detalhes
          </Button>
        </div>
      </Card>
    </motion.div>
  );
};

export default EquipmentCard;
