import { useState, useEffect } from 'react';
import api from '../api/client';
import { Play, Plus, BarChart3, Trash2, X } from 'lucide-react';

export default function CampaignManager() {
    const [campaigns, setCampaigns] = useState([]);
    const [templates, setTemplates] = useState([]);
    const [targets, setTargets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    // Launch Modal State
    const [launchConfig, setLaunchConfig] = useState(null); // { id, name }
    const [selectedTargetIds, setSelectedTargetIds] = useState(new Set());

    const [newCampaign, setNewCampaign] = useState({ name: '', template_id: '' });
    const [toast, setToast] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 3000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    const showToast = (message, type = 'success') => setToast({ message, type });

    const fetchData = async () => {
        try {
            const [campRes, tempRes, targRes] = await Promise.all([
                api.get('/campaigns/'),
                api.get('/templates/'),
                api.get('/targets/')
            ]);
            setCampaigns(campRes.data);
            setTemplates(tempRes.data);
            setTargets(targRes.data);
        } catch (err) {
            console.error("Failed to load data", err);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/campaigns/', newCampaign);
            setShowModal(false);
            setNewCampaign({ name: '', template_id: '' });
            fetchData();
            showToast("Campaign created successfully!");
        } catch (err) {
            showToast("Failed to create campaign", 'error');
        }
    };

    const openLaunchModal = (campaign) => {
        setLaunchConfig(campaign);
        // Default select all targets
        setSelectedTargetIds(new Set(targets.map(t => t.id)));
    };

    const toggleTarget = (id) => {
        const newSet = new Set(selectedTargetIds);
        if (newSet.has(id)) {
            newSet.delete(id);
        } else {
            newSet.add(id);
        }
        setSelectedTargetIds(newSet);
    };

    const handleLaunchConfirm = async () => {
        if (!launchConfig) return;

        try {
            await api.post(`/campaigns/${launchConfig.id}/launch`, {
                target_ids: Array.from(selectedTargetIds)
            });
            fetchData();
            showToast(`Campaign launched to ${selectedTargetIds.size} targets!`);
            setLaunchConfig(null);
        } catch (err) {
            showToast("Failed to launch campaign", 'error');
        }
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to delete this campaign?")) return;
        try {
            await api.delete(`/campaigns/${id}`);
            setCampaigns(campaigns.filter(c => c.id !== id));
            showToast("Campaign deleted");
        } catch (err) {
            showToast("Failed to delete campaign", 'error');
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="space-y-6 relative">
            {/* Toast Notification */}
            {toast && (
                <div className={`fixed top-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg text-white ${toast.type === 'error' ? 'bg-red-600' : 'bg-green-600'
                    } transition-all duration-300 flex items-center`}>
                    <span>{toast.message}</span>
                    <button onClick={() => setToast(null)} className="ml-2 hover:text-gray-200">
                        <X className="w-4 h-4" />
                    </button>
                </div>
            )}

            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">Campaign Management</h2>
                    <p className="text-gray-500">Create, schedule, and monitor phishing simulations.</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    New Campaign
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campaign Name</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created At</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {campaigns.map((c) => (
                            <tr key={c.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 font-medium text-gray-900">{c.name}</td>
                                <td className="px-6 py-4">
                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${c.status === 'active' ? 'bg-green-100 text-green-800' :
                                        c.status === 'completed' ? 'bg-gray-100 text-gray-800' :
                                            'bg-yellow-100 text-yellow-800'
                                        }`}>
                                        {c.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-gray-500 text-sm">
                                    {new Date(c.created_at).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4 text-right space-x-3">
                                    {c.status === 'draft' && (
                                        <button
                                            onClick={() => openLaunchModal(c)}
                                            className="text-blue-600 hover:text-blue-900 font-medium inline-flex items-center"
                                            title="Launch Campaign"
                                        >
                                            <Play className="w-4 h-4 mr-1" /> Launch
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleDelete(c.id)}
                                        className="text-red-400 hover:text-red-600 inline-flex items-center"
                                        title="Delete Campaign"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {campaigns.length === 0 && (
                            <tr>
                                <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                                    No campaigns found. Create one to get started.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Launch Confirmation Modal */}
            {launchConfig && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
                        <h3 className="text-xl font-bold mb-2">Launch Campaign</h3>
                        <p className="text-gray-500 mb-4">Select targets to receive "{launchConfig.name}".</p>

                        <div className="max-h-60 overflow-y-auto mb-4 border border-gray-200 rounded-lg divide-y divide-gray-100">
                            {targets.length > 0 ? targets.map(t => (
                                <div key={t.id} className="flex items-center p-3 hover:bg-gray-50">
                                    <input
                                        type="checkbox"
                                        checked={selectedTargetIds.has(t.id)}
                                        onChange={() => toggleTarget(t.id)}
                                        className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                                    />
                                    <div className="ml-3">
                                        <p className="text-sm font-medium text-gray-900">{t.first_name} {t.last_name}</p>
                                        <p className="text-xs text-gray-500">{t.email}</p>
                                    </div>
                                </div>
                            )) : (
                                <p className="p-4 text-center text-gray-500">No targets available.</p>
                            )}
                        </div>

                        <div className="flex justify-between items-center border-t pt-4">
                            <span className="text-sm text-gray-600">
                                {selectedTargetIds.size} target(s) selected
                            </span>
                            <div className="flex space-x-3">
                                <button
                                    onClick={() => setLaunchConfig(null)}
                                    className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={handleLaunchConfirm}
                                    disabled={selectedTargetIds.size === 0}
                                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                                >
                                    Launch Now
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Create Campaign Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-40">
                    <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
                        <h3 className="text-lg font-bold mb-4">Create New Campaign</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Campaign Name</label>
                                <input
                                    required
                                    type="text"
                                    className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                    value={newCampaign.name}
                                    onChange={e => setNewCampaign({ ...newCampaign, name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Select Template</label>
                                <select
                                    required
                                    className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                    value={newCampaign.template_id}
                                    onChange={e => setNewCampaign({ ...newCampaign, template_id: e.target.value })}
                                >
                                    <option value="">-- Choose a Template --</option>
                                    {templates.map(t => (
                                        <option key={t.id} value={t.id}>{t.name}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex justify-end space-x-3 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setShowModal(false)}
                                    className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                >
                                    Create
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
