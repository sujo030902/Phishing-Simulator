import { useState, useEffect } from 'react';
import api from '../api/client';
import { User, Plus, Trash2, X, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function UserResults() {
    const [targets, setTargets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [newTarget, setNewTarget] = useState({
        first_name: '', last_name: '', email: '', department: ''
    });
    const [toast, setToast] = useState(null);
    const [selectedHistory, setSelectedHistory] = useState(null); // Modal state

    useEffect(() => {
        fetchTargets();
    }, []);

    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 3000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    const showToast = (message, type = 'success') => setToast({ message, type });

    const fetchTargets = async () => {
        try {
            const res = await api.get('/targets/');
            setTargets(res.data);
        } catch (err) {
            console.error("Failed to fetch targets");
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/targets/', newTarget);
            setShowModal(false);
            setNewTarget({ first_name: '', last_name: '', email: '', department: '' });
            fetchTargets();
            showToast("Target added successfully!");
        } catch (err) {
            const msg = err.response?.data?.error || "Failed to add target";
            showToast(msg, 'error');
        }
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure? This will remove the target from future campaigns.")) return;
        try {
            await api.delete(`/targets/${id}`);
            setTargets(targets.filter(t => t.id !== id));
            showToast("Target deleted");
        } catch (err) {
            showToast("Failed to delete target", 'error');
        }
    };

    const handleEmailClick = async (e) => {
        // Intercept clicks on links within the email preview
        const link = e.target.closest('a');
        if (link) {
            e.preventDefault();

            // Show analysis modal immediatey
            setSelectedHistory((prev) => ({
                ...prev,
                showAnalysis: true,
                analysisLoading: true,
                analysisPoints: []
            }));

            try {
                // Fetch AI analysis
                const res = await api.post('/templates/analyze', {
                    subject: selectedHistory.email_subject,
                    body: selectedHistory.email_body
                });

                setSelectedHistory((prev) => ({
                    ...prev,
                    analysisLoading: false,
                    analysisPoints: res.data.analysis
                }));
            } catch (err) {
                console.error("Analysis failed", err);
                setSelectedHistory((prev) => ({
                    ...prev,
                    analysisLoading: false,
                    analysisPoints: ["Could not load specific analysis. Remember to check the sender and urgency."]
                }));
            }
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="space-y-6 relative">
            {/* Toast */}
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
                    <h2 className="text-2xl font-bold text-gray-900">Target Management</h2>
                    <p className="text-gray-500">Manage employees/targets for phishing simulations.</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Target
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Employee</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {targets.map((target) => (
                            <tr key={target.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className="flex-shrink-0 h-10 w-10 bg-slate-100 rounded-full flex items-center justify-center">
                                            <User className="h-5 w-5 text-slate-500" />
                                        </div>
                                        <div className="ml-4">
                                            <div className="text-sm font-medium text-gray-900">{target.first_name} {target.last_name}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {target.department || 'N/A'}
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-500">
                                    {target.email}
                                    {/* History Preview */}
                                    {target.history && target.history.length > 0 && (
                                        <div className="mt-2 space-y-1">
                                            {target.history.slice(0, 2).map((h, idx) => (
                                                <button
                                                    key={idx}
                                                    onClick={async () => {
                                                        setSelectedHistory(h);
                                                        // Track open
                                                        try {
                                                            await api.post(`/campaigns/${h.result_id}/track/open`);
                                                        } catch (err) { console.error("Track open failed", err); }
                                                    }}
                                                    className="w-full text-left text-xs bg-gray-50 hover:bg-blue-50 p-1.5 rounded border border-gray-100 hover:border-blue-200 flex justify-between items-center transition-colors"
                                                >
                                                    <span className="font-medium text-gray-700 truncate max-w-[150px]" title={h.email_subject}>
                                                        {h.email_subject}
                                                    </span>
                                                    <span className={`ml-2 px-1.5 py-0.5 rounded-full ${h.status === 'Clicked' ? 'bg-red-100 text-red-800' :
                                                        h.status === 'Opened' ? 'bg-yellow-100 text-yellow-800' :
                                                            'bg-blue-100 text-blue-800'
                                                        }`}>
                                                        {h.status}
                                                    </span>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => handleDelete(target.id)}
                                        className="text-red-400 hover:text-red-600"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {targets.length === 0 && (
                            <tr>
                                <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                                    No targets found. Add employees to start simulations.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Email Preview Modal */}
            {selectedHistory && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
                        <div className="flex justify-between items-start mb-4 border-b border-gray-100 pb-4">
                            <div>
                                <h3 className="text-xl font-bold text-gray-900">{selectedHistory.email_subject}</h3>
                                <p className="text-sm text-gray-500 mt-1">Campaign: {selectedHistory.campaign_name}</p>
                                <p className="text-xs text-gray-400 mt-1">Sent: {new Date(selectedHistory.sent_at).toLocaleString()}</p>
                            </div>
                            <button onClick={() => setSelectedHistory(null)} className="text-gray-400 hover:text-gray-600">
                                <X className="w-6 h-6" />
                            </button>
                        </div>

                        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
                            <div
                                className="prose prose-sm max-w-none"
                                onClick={handleEmailClick} // Intercept clicks here
                                dangerouslySetInnerHTML={{ __html: selectedHistory.email_body }}
                            />
                        </div>

                        <div className="mt-6 flex justify-end">
                            <button
                                onClick={() => setSelectedHistory(null)}
                                className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800"
                            >
                                Close Preview
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Add Target Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-40">
                    <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
                        <h3 className="text-lg font-bold mb-4">Add New Target</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">First Name</label>
                                    <input
                                        type="text"
                                        className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                        value={newTarget.first_name}
                                        onChange={e => setNewTarget({ ...newTarget, first_name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Last Name</label>
                                    <input
                                        type="text"
                                        className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                        value={newTarget.last_name}
                                        onChange={e => setNewTarget({ ...newTarget, last_name: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Email Address</label>
                                <input
                                    required
                                    type="email"
                                    className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                    value={newTarget.email}
                                    onChange={e => setNewTarget({ ...newTarget, email: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Department</label>
                                <input
                                    type="text"
                                    className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm p-2"
                                    value={newTarget.department}
                                    onChange={e => setNewTarget({ ...newTarget, department: e.target.value })}
                                />
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
                                    Add Target
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Phishing Education Modal (The "Caught" Popup) */}
            {selectedHistory && selectedHistory.showAnalysis && (
                <div className="fixed inset-0 bg-red-900/80 flex items-center justify-center p-4 z-[60]">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden animate-in fade-in zoom-in duration-300">
                        <div className="bg-red-600 p-6 text-center text-white">
                            <div className="mx-auto bg-white/20 w-16 h-16 rounded-full flex items-center justify-center mb-4">
                                <AlertTriangle className="w-10 h-10 text-white" />
                            </div>
                            <h2 className="text-2xl font-bold">Oops! You clicked a phishing link.</h2>
                            <p className="text-red-100 mt-2">In a real attack, this could have compromised your system.</p>
                        </div>

                        <div className="p-6">
                            <h3 className="font-bold text-gray-900 mb-3 flex items-center">
                                <ShieldAlert className="w-5 h-5 mr-2 text-orange-500" />
                                Why this is suspicious (AI Analysis):
                            </h3>

                            {selectedHistory.analysisLoading ? (
                                <div className="space-y-3 animate-pulse">
                                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                                </div>
                            ) : (
                                <ul className="space-y-3">
                                    {selectedHistory.analysisPoints?.map((point, idx) => (
                                        <li key={idx} className="flex items-start text-sm text-gray-700">
                                            <span className="flex-shrink-0 w-1.5 h-1.5 bg-red-500 rounded-full mt-1.5 mr-2"></span>
                                            {point}
                                        </li>
                                    ))}
                                </ul>
                            )}

                            <div className="mt-8 pt-6 border-t border-gray-100">
                                <button
                                    onClick={() => setSelectedHistory(prev => ({ ...prev, showAnalysis: false }))}
                                    className="w-full py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 transition-colors"
                                >
                                    I understand, close this.
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
