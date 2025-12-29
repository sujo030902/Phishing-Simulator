import { useState, useEffect } from 'react';
import api from '../api/client';
import { Wand2, Save, Info, X } from 'lucide-react';

export default function TemplateGenerator() {
    const [formData, setFormData] = useState({
        type: 'CEO Fraud',
        sender_name: 'John CEO',
        context: 'Urgent wire transfer request for a confidential project.',
    });
    const [generated, setGenerated] = useState(null);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [templates, setTemplates] = useState([]);
    const [toast, setToast] = useState(null);
    const [customName, setCustomName] = useState(''); // For new template
    const [editingId, setEditingId] = useState(null); // For renaming existing
    const [editName, setEditName] = useState('');

    useEffect(() => {
        fetchTemplates();
    }, []);

    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 3000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    const showToast = (message, type = 'success') => setToast({ message, type });

    const fetchTemplates = async () => {
        try {
            const res = await api.get('/templates/');
            setTemplates(res.data);
        } catch (err) {
            console.error("Failed to load templates");
        }
    };

    const handleGenerate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post('/templates/generate', formData);
            setGenerated({ ...res.data, is_ai_generated: true });
            setCustomName(`${formData.type} - ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`);
            showToast("Template generated successfully!");
        } catch (err) {
            const errorMsg = err.response?.data?.error || err.message || "Failed to generate template";
            console.error("Template generation error:", err);
            showToast(errorMsg, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!generated) return;
        setSaving(true);
        try {
            await api.post('/templates/', {
                name: customName || `${formData.type} - ${new Date().toLocaleDateString()}`,
                ...generated
            });
            showToast("Template saved!");
            setGenerated(null);
            setCustomName('');
            fetchTemplates();
        } catch (err) {
            const errorMsg = err.response?.data?.error || err.message || "Failed to save template";
            console.error("Template save error:", err);
            showToast(errorMsg, 'error');
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to delete this template?")) return;
        try {
            await api.delete(`/templates/${id}`);
            setTemplates(templates.filter(t => t.id !== id));
            showToast("Template deleted");
        } catch (err) {
            showToast("Failed to delete template", 'error');
        }
    };

    const startEditing = (template) => {
        setEditingId(template.id);
        setEditName(template.name);
    };

    const saveEdit = async (id) => {
        try {
            await api.put(`/templates/${id}`, { name: editName });
            setTemplates(templates.map(t => t.id === id ? { ...t, name: editName } : t));
            setEditingId(null);
            showToast("Template renamed");
        } catch (err) {
            showToast("Failed to rename", 'error');
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div>
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <Wand2 className="w-6 h-6 mr-2 text-purple-600" />
                    AI Template Generator
                </h2>
                <p className="text-gray-500 mt-1">Generate realistic phishing templates using Groq AI (Llama 3).</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Input Form */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <form onSubmit={handleGenerate} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Attack Type</label>
                            <select
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                value={formData.type}
                                onChange={e => setFormData({ ...formData, type: e.target.value })}
                            >
                                <option>CEO Fraud</option>
                                <option>IT Password Reset</option>
                                <option>Package Delivery</option>
                                <option>HR Policy Update</option>
                                <option>Invoice Payment</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Sender Name</label>
                            <input
                                type="text"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                value={formData.sender_name}
                                onChange={e => setFormData({ ...formData, sender_name: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Context/Scenario</label>
                            <textarea
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                rows={4}
                                value={formData.context}
                                onChange={e => setFormData({ ...formData, context: e.target.value })}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
                        >
                            {loading ? 'Generating...' : 'Generate Content'}
                        </button>
                    </form>
                </div>

                {/* Preview */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Preview</h3>

                    {generated ? (
                        <div className="flex-1 space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 uppercase mb-1">Template Name</label>
                                <input
                                    type="text"
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                    value={customName}
                                    onChange={e => setCustomName(e.target.value)}
                                    placeholder="Enter a name for this template"
                                />
                            </div>

                            <div className="border-b pb-4">
                                <p className="text-sm text-gray-500">Subject</p>
                                <p className="font-medium text-gray-900">{generated.subject}</p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-500 mb-2">Body</p>
                                <div
                                    className="prose prose-sm bg-gray-50 p-4 rounded-md border border-gray-200"
                                    dangerouslySetInnerHTML={{ __html: generated.body }}
                                />
                            </div>
                            <div className="mt-4 bg-blue-50 border-l-4 border-blue-400 p-4">
                                <div className="flex">
                                    <div className="flex-shrink-0">
                                        <Info className="h-5 w-5 text-blue-400" aria-hidden="true" />
                                    </div>
                                    <div className="ml-3">
                                        <p className="text-sm text-blue-700">
                                            Note: Verify this content is safe and educational before saving.
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={handleSave}
                                disabled={saving}
                                className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
                            >
                                <Save className="w-4 h-4 mr-2" />
                                Save Template
                            </button>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center text-gray-400 border-2 border-dashed rounded-lg">
                            No content generated yet
                        </div>
                    )}
                </div>
            </div>

            {/* Saved Templates Section */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-100">
                    <h3 className="text-lg font-bold text-gray-900">Saved Templates</h3>
                </div>
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subject</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {templates.map((t) => (
                            <tr key={t.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 text-sm font-medium text-gray-900">
                                    {editingId === t.id ? (
                                        <div className="flex items-center space-x-2">
                                            <input
                                                type="text"
                                                value={editName}
                                                onChange={e => setEditName(e.target.value)}
                                                className="border rounded px-2 py-1 text-sm w-full"
                                            />
                                            <button onClick={() => saveEdit(t.id)} className="text-green-600 text-xs">Save</button>
                                            <button onClick={() => setEditingId(null)} className="text-gray-500 text-xs">Cancel</button>
                                        </div>
                                    ) : (
                                        <span onClick={() => startEditing(t)} className="cursor-pointer hover:underline decoration-dashed" title="Click to rename">
                                            {t.name}
                                        </span>
                                    )}
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-500 truncate max-w-xs">{t.subject}</td>
                                <td className="px-6 py-4 text-right space-x-3 text-sm">
                                    <button
                                        onClick={() => setGenerated({ subject: t.subject, body: t.body_content })}
                                        className="text-blue-600 hover:text-blue-900 font-medium"
                                    >
                                        Load
                                    </button>
                                    <button
                                        onClick={() => handleDelete(t.id)}
                                        className="text-red-400 hover:text-red-600"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {templates.length === 0 && (
                            <tr>
                                <td colSpan="3" className="px-6 py-8 text-center text-gray-500">
                                    No saved templates found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

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
        </div>
    );
}
