
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from '@/components/ui/use-toast';
import { Eye, EyeOff, Lock, Mail } from 'lucide-react';

function LoginPage({ setIsAuthenticated }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!email || !password) {
      toast({
        title: "Erro de Login",
        description: "Por favor, preencha o email e a senha.",
        variant: "destructive",
      });
      return;
    }
    
    // Simulação de autenticação
    if (email === 'admin@example.com' && password === 'password123') {
      toast({
        title: "Login Bem-sucedido!",
        description: "Redirecionando para o dashboard...",
        variant: "default",
      });
      setIsAuthenticated(true);
      navigate('/dashboard');
    } else {
      toast({
        title: "Credenciais Inválidas",
        description: "Por favor, verifique seu email e senha.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="w-full max-w-md glass-effect shadow-2xl">
          <CardHeader className="text-center">
            <motion.div 
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              <Lock className="h-16 w-16 mx-auto text-green-400 mb-4 p-3 rounded-full bg-green-500/10" />
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                Acesso ao Inventário
              </CardTitle>
            </motion.div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-6">
              <motion.div
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.5 }}
                className="space-y-2"
              >
                <label htmlFor="email" className="text-sm font-medium text-slate-300">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="seuemail@exemplo.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10 bg-slate-800/50 border-slate-600 text-white placeholder:text-slate-500 focus:border-green-500"
                  />
                </div>
              </motion.div>
              <motion.div
                initial={{ x: 20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.4, duration: 0.5 }}
                className="space-y-2"
              >
                <label htmlFor="password" className="text-sm font-medium text-slate-300">Senha</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="********"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10 pr-10 bg-slate-800/50 border-slate-600 text-white placeholder:text-slate-500 focus:border-green-500"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </motion.div>
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.5 }}
              >
                <Button type="submit" className="w-full bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-semibold py-3 text-base">
                  Entrar
                </Button>
              </motion.div>
            </form>
            <motion.p 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="mt-6 text-center text-sm text-slate-400"
            >
              Não tem uma conta?{' '}
              <a href="#" onClick={(e) => {e.preventDefault(); toast({title: "🚧 Funcionalidade não implementada"});}} className="font-medium text-green-400 hover:text-green-300">
                Registre-se
              </a>
            </motion.p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

export default LoginPage;
