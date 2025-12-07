import React, { useState } from 'react';
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle } from 'lucide-react';

export default function Upload() {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState(null); // 'success' | 'error' | null

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setStatus(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setStatus('success');
                setFile(null);
            } else {
                setStatus('error');
            }
        } catch (error) {
            console.error("Upload failed", error);
            setStatus('error');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <h2 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <UploadIcon className="w-5 h-5 text-indigo-600" />
                Subir Documentos
            </h2>

            <div className="border-2 border-dashed border-slate-200 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors">
                <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    accept=".pdf,.txt"
                    onChange={handleFileChange}
                />
                <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center gap-2">
                    <div className="w-12 h-12 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-600">
                        <FileText className="w-6 h-6" />
                    </div>
                    <span className="text-slate-600 font-medium">
                        {file ? file.name : "Click para seleccionar PDF o TXT"}
                    </span>
                    <span className="text-xs text-slate-400">Máximo 10MB</span>
                </label>
            </div>

            {file && (
                <button
                    onClick={handleUpload}
                    disabled={uploading}
                    className="mt-4 w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                    {uploading ? 'Subiendo...' : 'Subir a Base de Conocimiento'}
                </button>
            )}

            {status === 'success' && (
                <div className="mt-4 p-3 bg-green-50 text-green-700 rounded-lg flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4" />
                    Documento procesado correctamente.
                </div>
            )}

            {status === 'error' && (
                <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center gap-2 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    Error al subir el documento.
                </div>
            )}
        </div>
    );
}
