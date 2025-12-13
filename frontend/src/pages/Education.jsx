import { BookOpen, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

export default function Education() {
    const trainingModules = [
        {
            id: 1,
            title: "Identifying Suspicious Senders",
            description: "Learn how to spot mismatched email addresses and display names.",
            completed: true,
            score: 100
        },
        {
            id: 2,
            title: "Urgency and Threats",
            description: "Understanding how social engineering uses panic to trick you.",
            completed: false,
            score: null
        },
        {
            id: 3,
            title: "Safe Browsing Habits",
            description: "Best practices for checking links before clicking.",
            completed: false,
            score: null
        }
    ];

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <BookOpen className="w-6 h-6 mr-2 text-blue-600" />
                    Security Awareness Training
                </h2>
                <p className="text-gray-500 mt-1">
                    Complete these modules to improve your phishing recognition skills.
                </p>
            </div>

            {/* Status Card */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl p-6 text-white shadow-lg">
                <h3 className="text-lg font-bold">Your Security Score</h3>
                <div className="mt-4 flex items-end">
                    <span className="text-5xl font-extrabold">85</span>
                    <span className="text-blue-200 ml-2 mb-1">/ 100</span>
                </div>
                <div className="mt-4 w-full bg-blue-900 bg-opacity-30 rounded-full h-2">
                    <div className="bg-white h-2 rounded-full" style={{ width: '85%' }}></div>
                </div>
                <p className="mt-2 text-sm text-blue-100">You are doing great! Complete 2 more modules to reach 100.</p>
            </div>

            {/* Modules List */}
            <div className="grid grid-cols-1 gap-6">
                {trainingModules.map((module) => (
                    <div key={module.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex justify-between items-center hover:shadow-md transition-shadow">
                        <div className="flex items-start space-x-4">
                            <div className={`p-3 rounded-lg ${module.completed ? 'bg-green-100 text-green-600' : 'bg-orange-100 text-orange-600'}`}>
                                {module.completed ? <CheckCircle className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
                            </div>
                            <div>
                                <h4 className="text-lg font-semibold text-gray-900">{module.title}</h4>
                                <p className="text-gray-500">{module.description}</p>
                            </div>
                        </div>

                        <div className="flex items-center">
                            {module.completed ? (
                                <span className="px-4 py-2 bg-green-50 text-green-700 rounded-full text-sm font-medium border border-green-200">
                                    Completed
                                </span>
                            ) : (
                                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors">
                                    Start Module
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Educational Content Example - "The Teachable Moment" */}
            <div className="border-t border-gray-200 pt-8">
                <h3 className="text-xl font-bold text-gray-800 mb-4">Recent Simulation Analysis</h3>
                <div className="bg-red-50 border border-red-200 rounded-xl p-6">
                    <div className="flex items-start mb-4">
                        <XCircle className="w-6 h-6 text-red-500 mr-2 mt-1" />
                        <div>
                            <h4 className="text-lg font-bold text-red-800">You clicked a simulated phishing link!</h4>
                            <p className="text-red-700 mt-1">
                                On Dec 12, ran "CEO Fraud" simulation. You clicked the link "Update Account Now".
                            </p>
                        </div>
                    </div>

                    <div className="bg-white p-4 rounded-lg border border-red-100">
                        <h5 className="font-semibold text-gray-900 mb-2">Red Flags You Missed:</h5>
                        <ul className="list-disc list-inside text-gray-600 space-y-1">
                            <li><strong>Sender Address:</strong> The email came from `ceo-office@gmaill.com` instead of the company domain.</li>
                            <li><strong>Urgency:</strong> The subject line demanded "Immediate Action" to bypass critical thinking.</li>
                            <li><strong>Generic Greeting:</strong> It used "Dear Employee" instead of your name.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
