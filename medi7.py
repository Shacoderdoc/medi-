// pages/charts.js
import { useEffect, useState } from 'react';
import Nav from '../components/Nav';
import { supabase } from '../lib/supabaseClient';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function ChartsPage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      const { data: items, error } = await supabase.from('items').select('id, title, created_at').order('created_at', { ascending: true });
      if (error) return console.error(error);
      // build daily counts
      const counts = {};
      items.forEach(it => {
        const date = new Date(it.created_at).toLocaleDateString();
        counts[date] = (counts[date] || 0) + 1;
      });
      const chartData = Object.keys(counts).map(k => ({ date: k, count: counts[k] }));
      setData(chartData);
    }
    load();
  }, []);

  return (
    <>
      <Nav />
      <main className="max-w-4xl mx-auto py-12 px-4">
        <h1 className="text-2xl font-semibold mb-6">Analytics / Charts</h1>
        <div className="bg-white p-4 rounded shadow-sm" style={{ height: 350 }}>
          {data.length === 0 ? (
            <div className="text-center text-gray-500">No data yet. Add items from Dashboard to populate the chart.</div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </main>
    </>
  );
}
