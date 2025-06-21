
import React from 'react';

const RecentActivityItem = ({ icon: Icon, color, text, time }) => {
  return (
    <div className="flex items-center space-x-4 p-4 bg-slate-800/50 rounded-lg">
      <Icon className={`h-6 w-6 ${color}`} />
      <div>
        <p className="font-semibold">{text}</p>
        <p className="text-sm text-slate-400">{time}</p>
      </div>
    </div>
  );
};

export default RecentActivityItem;
