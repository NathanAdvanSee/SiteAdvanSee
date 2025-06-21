
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';
import DashboardPage from '@/pages/DashboardPage';
import LoginPage from '@/pages/LoginPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false); // Example state

  return (
    <>
      <Routes>
        <Route 
          path="/login" 
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} 
        />
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/" 
          element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} 
        />
      </Routes>
      <Toaster />
    </>
  );
}

export default App;
