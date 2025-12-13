import { useState, useEffect } from 'react';
import api from '../api/client';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
    const [stats, setStats] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // In a real app, we'd fetch aggregate stats. 
        // For now, we'll fetch campaigns and getting individual stats (mocking the aggregate)
        // Or we can create an aggregate endpoint later.

        // For this prototype, we'll mock the data if the API call fails or implement a basic fetch
        const fetchStats = async () => {
            try {
                const res = await api.get('/campaigns/');
                const campaigns = res.data;

                // Fetch stats for each active campaign
                const statsPromises = campaigns.map(c => api.get(`/campaigns/${c.id}/stats`));
                const statsRes = await Promise.all(statsPromises);

                const data = statsRes.map(r => r.data);
                setStats(data);
            } catch (err) {
                console.error("Failed to fetch dashboard data", err);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) return <div>Loading metrics...</div>;
    if (stats.length === 0) return <div>No active campaigns found. Start one to see metrics!</div>;

    return (
        <div className="space-y-6">
            {/* Key Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <MetricCard label="Total Sent" value={stats.reduce((acc, curr) => acc + curr.total_sent, 0)} color="bg-blue-500" />
                <MetricCard label="Opened" value={stats.reduce((acc, curr) => acc + curr.opened, 0)} color="bg-yellow-500" />
                <MetricCard label="Clicked" value={stats.reduce((acc, curr) => acc + curr.clicked, 0)} color="bg-orange-500" />
                <MetricCard label="Compromised" value={stats.reduce((acc, curr) => acc + curr.submitted, 0)} color="bg-red-500" />
            </div>

            {/* Chart */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-96">
                <h3 className="text-lg font-medium mb-6">Campaign Performance</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={stats}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="campaign" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="opened" fill="#eab308" name="Opened" />
                        <Bar dataKey="clicked" fill="#f97316" name="Clicked" />
                        <Bar dataKey="submitted" fill="#ef4444" name="Submitted Data" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

function MetricCard({ label, value, color }) {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-gray-500 text-sm font-medium">{label}</p>
            <div className="mt-2 flex items-baseline">
                <span className="text-3xl font-bold text-gray-900">{value}</span>
            </div>
            <div className={`mt-2 h-1 w-full rounded-full ${color.replace('bg-', 'bg-opacity-20 ')}`}>
                <div className={`h-1 rounded-full ${color}`} style={{ width: '100%' }}></div>
            </div>
        </div>
    );
}
