"use client";

import React, { useState, useEffect } from 'react';
import { ShieldAlert, AlertTriangle, Activity, Clock, LayoutDashboard, Terminal, Shield, Settings } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function Dashboard() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/alerts?limit=100');
        const data = await response.json();
        setAlerts(data.data || []);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch alerts", error);
        setLoading(false);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const criticalCount = alerts.filter(a => a.severity === 'critical').length;
  const highCount = alerts.filter(a => a.severity === 'high').length;
  const mediumCount = alerts.filter(a => a.severity === 'medium').length;

  const severityData = [
    { name: 'Critical', value: criticalCount, color: '#EF4444' },
    { name: 'High', value: highCount, color: '#F97316' },
    { name: 'Medium', value: mediumCount, color: '#EAB308' },
    { name: 'Info', value: alerts.length - (criticalCount + highCount + mediumCount), color: '#3B82F6' },
  ];

  const getSeverityStyle = (severity: string) => {
    switch(severity) {
      case 'critical': return 'bg-red-500/20 text-red-500 border border-red-500/30';
      case 'high': return 'bg-orange-500/20 text-orange-500 border border-orange-500/30';
      case 'medium': return 'bg-yellow-500/20 text-yellow-500 border border-yellow-500/30';
      default: return 'bg-blue-500/20 text-blue-500 border border-blue-500/30';
    }
  };

  return (
    <div className="flex h-screen bg-[#0B0E14] text-white overflow-hidden">
      
      <div className="w-64 bg-[#151923] border-r border-[#2A2F3D] flex flex-col">
        <div className="p-6 flex items-center gap-3 border-b border-[#2A2F3D]">
          <Shield className="text-blue-500" size={28} />
          <div>
            <h1 className="font-bold text-lg tracking-wide">AI SOC Analyst</h1>
            <p className="text-xs text-gray-400">Intelligent Operations</p>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a href="#" className="flex items-center gap-3 px-4 py-3 bg-blue-500/10 text-blue-500 rounded-lg"><LayoutDashboard size={20} /> Overview</a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-[#2A2F3D] rounded-lg transition-colors"><AlertTriangle size={20} /> Alerts</a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-[#2A2F3D] rounded-lg transition-colors"><Terminal size={20} /> Threat Hunting</a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-[#2A2F3D] rounded-lg transition-colors"><Settings size={20} /> Settings</a>
        </nav>
      </div>

      <div className="flex-1 overflow-auto">
        <header className="p-8 pb-4 flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold mb-1">Security Operations Overview</h2>
            <p className="text-gray-400">AI-powered threat detection, correlation and response</p>
          </div>
        </header>

        <main className="p-8 space-y-6">
          <div className="grid grid-cols-4 gap-6">
            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <p className="text-gray-400 font-medium">Total Alerts</p>
                <Activity className="text-blue-500" size={20} />
              </div>
              <h3 className="text-3xl font-bold">{alerts.length}</h3>
            </div>
            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <p className="text-gray-400 font-medium">Critical Alerts</p>
                <ShieldAlert className="text-red-500" size={20} />
              </div>
              <h3 className="text-3xl font-bold text-red-500">{criticalCount}</h3>
            </div>
            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <p className="text-gray-400 font-medium">High Severity</p>
                <AlertTriangle className="text-orange-500" size={20} />
              </div>
              <h3 className="text-3xl font-bold text-orange-500">{highCount}</h3>
            </div>
            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <p className="text-gray-400 font-medium">System Status</p>
                <Clock className="text-green-500" size={20} />
              </div>
              <h3 className="text-3xl font-bold text-green-500">Live</h3>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-6">
            
            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6 col-span-2">
              <h3 className="font-semibold mb-6">Latest Security Alerts</h3>
              {loading ? (
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-4 py-1">
                    <div className="h-4 bg-[#2A2F3D] rounded w-3/4"></div>
                    <div className="h-4 bg-[#2A2F3D] rounded"></div>
                    <div className="h-4 bg-[#2A2F3D] rounded w-5/6"></div>
                  </div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="text-xs text-gray-500 uppercase border-b border-[#2A2F3D]">
                        <th className="pb-3 font-medium">Time</th>
                        <th className="pb-3 font-medium">Event Action</th>
                        <th className="pb-3 font-medium">Source IP</th>
                        <th className="pb-3 font-medium">Log Source</th>
                        <th className="pb-3 font-medium">Severity</th>
                      </tr>
                    </thead>
                    <tbody className="text-sm">
                      {alerts.slice(0, 8).map((alert, idx) => (
                        <tr key={idx} className="border-b border-[#2A2F3D]/50 hover:bg-[#2A2F3D]/20 transition-colors">
                          <td className="py-4 text-gray-400">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                          <td className="py-4 font-medium">{alert.event?.action?.replace(/_/g, ' ') || 'Unknown'}</td>
                          <td className="py-4 text-gray-400">{alert.source?.ip || 'N/A'}</td>
                          <td className="py-4 text-gray-400 uppercase">{alert.log_source}</td>
                          <td className="py-4">
                            <span className={`px-2.5 py-1 rounded-md text-xs font-medium uppercase ${getSeverityStyle(alert.severity)}`}>
                              {alert.severity}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            <div className="bg-[#151923] border border-[#2A2F3D] rounded-xl p-6">
              <h3 className="font-semibold mb-6">Alerts by Severity</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={severityData}
                      innerRadius={60}
                      outerRadius={90}
                      paddingAngle={5}
                      dataKey="value"
                      stroke="none"
                    >
                      {severityData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#151923', borderColor: '#2A2F3D', color: '#fff' }}
                      itemStyle={{ color: '#fff' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 space-y-2">
                {severityData.map((item) => (
                  <div key={item.name} className="flex justify-between items-center text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                      <span className="text-gray-400">{item.name}</span>
                    </div>
                    <span className="font-medium">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}