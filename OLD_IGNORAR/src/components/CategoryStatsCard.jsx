
import React from 'react';
import { motion } from 'framer-motion';

const CategoryStatsCard = ({ category, count, icon: Icon, label, color }) => {
  return (
    <motion.div
      key={category}
      whileHover={{ scale: 1.05 }}
      className={`${color} rounded-xl p-4 text-white text-center`}
    >
      <Icon className="h-8 w-8 mx-auto mb-2" />
      <p className="font-semibold">{label}</p>
      <p className="text-2xl font-bold">{count}</p>
    </motion.div>
  );
};

export default CategoryStatsCard;
