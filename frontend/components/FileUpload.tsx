"use client";

import { useState, useCallback, useEffect } from "react";
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function FileUpload() {
    const [isDragging, setIsDragging] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [message, setMessage] = useState("");

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const selectedFile = e.dataTransfer.files[0];
            if (selectedFile.type === "application/pdf") {
                setFile(selectedFile);
                setStatus("idle");
                setMessage("");
            } else {
                setMessage("PDFファイルのみアップロード可能です。");
                setStatus("error");
            }
        }
    }, []);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (selectedFile.type === "application/pdf") {
                setFile(selectedFile);
                setStatus("idle");
                setMessage("");
            } else {
                setMessage("PDFファイルのみアップロード可能です。");
                setStatus("error");
            }
        }
    };

    const uploadFile = async () => {
        if (!file) return;

        setStatus("uploading");
        const formData = new FormData();
        formData.append("file", file);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const response = await fetch(`${apiUrl}/api/upload`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setStatus("success");
                setMessage("アップロード完了。診断情報の更新を開始しました。");
                setFile(null);
            } else {
                setStatus("error");
                const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
                setMessage(`アップロード失敗: ${errorData.detail || "サーバーエラー"}`);
            }
        } catch (error) {
            console.error(error);
            setStatus("error");
            setMessage(`エラー: ${(error as any).message}`);
        }
    };

    return (
        <div className="w-full max-w-md mx-auto p-4 bg-white rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-indigo-600" />
                マニュアル登録
            </h3>

            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`
          relative border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer
          ${isDragging ? "border-indigo-500 bg-indigo-50" : "border-slate-300 hover:border-slate-400"}
          ${status === "uploading" ? "opacity-50 pointer-events-none" : ""}
        `}
            >
                <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileSelect}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />

                <div className="flex flex-col items-center gap-3">
                    {file ? (
                        <FileText className="w-10 h-10 text-indigo-600" />
                    ) : (
                        <Upload className="w-10 h-10 text-slate-400" />
                    )}

                    <div className="text-sm text-slate-600">
                        {file ? (
                            <span className="font-medium text-slate-900">{file.name}</span>
                        ) : (
                            <span>
                                PDFファイルをドラッグ＆ドロップ
                                <br />
                                またはクリックして選択
                            </span>
                        )}
                    </div>
                </div>
            </div>

            {message && (
                <div className={`mt-4 p-3 rounded-lg flex items-start gap-2 text-sm ${status === "success" ? "bg-green-50 text-green-700" :
                    status === "error" ? "bg-red-50 text-red-700" : "bg-slate-50 text-slate-600"
                    }`}>
                    {status === "success" ? <CheckCircle className="w-4 h-4 mt-0.5 shrink-0" /> :
                        status === "error" ? <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" /> : null}
                    {message}
                </div>
            )}

            <button
                onClick={uploadFile}
                disabled={!file || status === "uploading"}
                className={`
          mt-4 w-full py-2.5 px-4 rounded-lg font-medium text-white transition-all
          ${!file || status === "uploading"
                        ? "bg-slate-300 cursor-not-allowed"
                        : "bg-indigo-600 hover:bg-indigo-700 shadow-md hover:shadow-lg active:scale-[0.98]"}
          flex items-center justify-center gap-2
        `}
            >
                {status === "uploading" ? (
                    <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        アップロード中...
                    </>
                ) : "アップロード"}
            </button>
            <LoadedManuals />
        </div >
    );
}

function LoadedManuals() {
    const [status, setStatus] = useState<any>(null);

    const fetchStatus = async () => {
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${apiUrl}/api/status`);
            if (res.ok) {
                const data = await res.json();
                setStatus(data);
            }
        } catch (e) {
            console.error(e);
        }
    };

    // Fetch on mount and polling every 5s
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    if (!status) return null;

    return (
        <div className="mt-8 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-semibold text-slate-700 mb-2">登録済みマニュアル:</h4>
            {status.manuals.length === 0 ? (
                <p className="text-sm text-slate-400">なし</p>
            ) : (
                <ul className="space-y-1">
                    {status.manuals.map((m: string) => (
                        <li key={m} className="text-sm text-slate-600 flex items-center gap-2">
                            <FileText className="w-4 h-4 text-slate-400" />
                            {m}
                        </li>
                    ))}
                </ul>
            )}
            <div className="mt-2 text-xs text-slate-400">
                Context Status: {status.is_context_loaded ? "Ready" : "Not Loaded"} ({status.context_length} chars)
            </div>
        </div>
    );
}
