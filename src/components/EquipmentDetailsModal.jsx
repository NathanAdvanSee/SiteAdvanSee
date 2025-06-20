
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CATEGORIES, STATUS_OPTIONS } from '@/lib/constants';
import { Edit, Trash2 } from 'lucide-react';

const EquipmentDetailsModal = ({ equipment, onClose, onEdit, onDelete }) => {
  if (!equipment) return null;

  const CategoryIcon = CATEGORIES[equipment.category]?.icon;
  const StatusIcon = STATUS_OPTIONS[equipment.status]?.icon;

  return (
    <AnimatePresence>
      {equipment && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="glass-effect rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Detalhes do Equipamento</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={onClose}
                className="text-slate-400 hover:text-white"
              >
                ×
              </Button>
            </div>

            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                {CategoryIcon && (
                  <div className={`p-4 rounded-lg ${CATEGORIES[equipment.category]?.color || ''}`}>
                    <CategoryIcon className="h-8 w-8 text-white" />
                  </div>
                )}
                <div>
                  <h3 className="text-xl font-bold text-white">{equipment.name}</h3>
                  <p className="text-slate-400">{equipment.serialNumber}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="text-sm text-slate-400">Status</label>
                    <div className="mt-1">
                      <Badge className={`${STATUS_OPTIONS[equipment.status]?.color || ''} text-white border-0`}>
                        {StatusIcon && <StatusIcon className="h-3 w-3 mr-1" />}
                        {STATUS_OPTIONS[equipment.status]?.label || equipment.status}
                      </Badge>
                    </div>
                  </div>

                  <div>
                    <label className="text-sm text-slate-400">Categoria</label>
                    <p className="text-white font-medium">{CATEGORIES[equipment.category]?.label || equipment.category}</p>
                  </div>

                  <div>
                    <label className="text-sm text-slate-400">Usuário</label>
                    <p className="text-white font-medium">{equipment.user}</p>
                  </div>

                  <div>
                    <label className="text-sm text-slate-400">Localização</label>
                    <p className="text-white font-medium">{equipment.location}</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="text-sm text-slate-400">Data de Compra</label>
                    <p className="text-white font-medium">{equipment.purchaseDate ? new Date(equipment.purchaseDate).toLocaleDateString('pt-BR') : 'N/A'}</p>
                  </div>

                  <div>
                    <label className="text-sm text-slate-400">Garantia até</label>
                    <p className="text-white font-medium">{equipment.warranty ? new Date(equipment.warranty).toLocaleDateString('pt-BR') : 'N/A'}</p>
                  </div>

                  <div>
                    <label className="text-sm text-slate-400">Especificações</label>
                    <p className="text-white font-medium">{equipment.specifications}</p>
                  </div>
                </div>
              </div>

              <div className="flex space-x-4 pt-6 border-t border-slate-600">
                <Button
                  onClick={() => onEdit(equipment)}
                  className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
                >
                  <Edit className="h-4 w-4 mr-2" />
                  Editar
                </Button>
                <Button
                  variant="outline"
                  onClick={() => onDelete(equipment)}
                  className="border-red-500/30 text-red-400 hover:border-red-500/60 hover:bg-red-500/10"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Excluir
                </Button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default EquipmentDetailsModal;
