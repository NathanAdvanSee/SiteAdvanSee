
import React from 'react';
import { Card } from '@/components/ui/card';

const StatsCard = ({ label, value, icon: Icon, color, borderColor }) => {
  return (
    <Card className={`glass-effect p-6 ${borderColor}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">{label}</p>
          <p className={`text-3xl font-bold ${color}`}>{value}</p>
        </div>
        <Icon className={`h-12 w-12 ${color}`} />
      </div>
    </Card>
  );
};

export default StatsCard;
