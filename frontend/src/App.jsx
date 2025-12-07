import React, { useState } from 'react';
import { MessageSquare, Settings, LayoutDashboard, Send } from 'lucide-react';
import Upload from './components/Upload';

function App() {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [testMessage, setTestMessage] = useState('');
    const [chatLog, setChatLog] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleTestChat = async (e) => {
        e.preventDefault();
        if (!testMessage.trim()) return;

        const newMessage = { role: 'user', content: testMessage };
        setChatLog(prev => [...prev, newMessage]);
        setTestMessage('');
        setLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: newMessage.content }),
            });
            const data = await response.json();
            setChatLog(prev => [...prev, { role: 'bot', content: data.response }]);
        } catch (error) {
            console.error("Chat error", error);
            setChatLog(prev => [...prev, { role: 'bot', content: "Error al conectar con el servidor." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex font-sans text-slate-900">
            {/* Sidebar */}
            <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
                <div className="p-6 border-b border-slate-100">
                    <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                        WhatsApp AI
                    </h1>
                    <p className="text-xs text-slate-500 mt-1">Soporte Inteligente</p>
                </div>

                <nav className="flex-1 p-4 space-y-1">
                    <button
                        onClick={() => setActiveTab('dashboard')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${activeTab === 'dashboard' ? 'bg-indigo-50 text-indigo-600' : 'text-slate-600 hover:bg-slate-50'}`}
                    >
                        <LayoutDashboard className="w-5 h-5" />
                        Dashboard
                    </button>
                    <button
                        onClick={() => setActiveTab('chats')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${activeTab === 'chats' ? 'bg-indigo-50 text-indigo-600' : 'text-slate-600 hover:bg-slate-50'}`}
                    >
                        <MessageSquare className="w-5 h-5" />
                        Chats Activos
                    </button>
                    <button
                        onClick={() => setActiveTab('settings')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${activeTab === 'settings' ? 'bg-indigo-50 text-indigo-600' : 'text-slate-600 hover:bg-slate-50'}`}
                    >
                        <Settings className="w-5 h-5" />
                        Configuración
                    </button>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8 overflow-y-auto">
                <header className="mb-8 flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">
                            {activeTab === 'dashboard' && 'Panel de Control'}
                            {activeTab === 'chats' && 'Chats en Tiempo Real'}
                            {activeTab === 'settings' && 'Configuración'}
                        </h2>
                        <p className="text-slate-500 text-sm mt-1">Gestión de tu agente de soporte</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
                        <span className="text-sm font-medium text-slate-600">Sistema Operativo</span>
                    </div>
                </header>

                {activeTab === 'dashboard' && (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Left Column: Upload & Stats */}
                        <div className="space-y-8">
                            <Upload />

                            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                                <h3 className="font-semibold text-slate-800 mb-4">Estadísticas Rápidas</h3>
                                <div className="space-y-4">
                                    <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                                        <span className="text-sm text-slate-600">Documentos Indexados</span>
                                        <span className="font-bold text-slate-900">3</span>
                                    </div>
                                    <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                                        <span className="text-sm text-slate-600">Consultas Hoy</span>
                                        <span className="font-bold text-slate-900">12</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Right Column: Test Chat */}
                        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 flex flex-col h-[600px]">
                            <div className="p-4 border-b border-slate-100 flex justify-between items-center">
                                <h3 className="font-semibold text-slate-800">Simulador de Chat</h3>
                                <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">Modo Prueba</span>
                            </div>

                            <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-50/50">
                                {chatLog.length === 0 && (
                                    <div className="text-center text-slate-400 mt-20">
                                        <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-20" />
                                        <p>Inicia una conversación para probar el agente.</p>
                                    </div>
                                )}
                                {chatLog.map((msg, idx) => (
                                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                                            ? 'bg-indigo-600 text-white rounded-tr-none'
                                            : 'bg-white border border-slate-200 text-slate-700 rounded-tl-none shadow-sm'
                                            }`}>
                                            {msg.content}
                                        </div>
                                    </div>
                                ))}
                                {loading && (
                                    <div className="flex justify-start">
                                        <div className="bg-white border border-slate-200 p-3 rounded-2xl rounded-tl-none shadow-sm">
                                            <div className="flex gap-1">
                                                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
                                                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></span>
                                                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <form onSubmit={handleTestChat} className="p-4 border-t border-slate-100 bg-white rounded-b-xl">
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        value={testMessage}
                                        onChange={(e) => setTestMessage(e.target.value)}
                                        placeholder="Escribe una pregunta sobre tus documentos..."
                                        className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                                    />
                                    <button
                                        type="submit"
                                        disabled={loading || !testMessage.trim()}
                                        className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                                    >
                                        <Send className="w-5 h-5" />
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                {activeTab === 'chats' && (
                    <div className="bg-white p-12 rounded-xl shadow-sm border border-slate-100 text-center">
                        <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <MessageSquare className="w-8 h-8 text-slate-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-900">Sin chats activos</h3>
                        <p className="text-slate-500 mt-2">Conecta Evolution API para ver los mensajes de WhatsApp en tiempo real.</p>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
