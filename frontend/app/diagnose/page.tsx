'use client';

import React, { useState, useEffect } from 'react';
import VideoPlayer from '../../components/VideoPlayer';
import VoiceInput from '../../components/VoiceInput';

interface DiagnoseResponse {
    probable_causes: string[];
    confidence: number;
    steps: string[];
    cautions: string[];
    next_actions: any;
    disclaimer: string;
    referenced_pages: number[];
    visual_page_base64?: string;
    source_file?: string;
    request_id?: string;
}

export default function DiagnosePage() {
    const [loading, setLoading] = useState(false);
    const [diagnosisData, setDiagnosisData] = useState<DiagnoseResponse | null>(null);
    const [videoData, setVideoData] = useState<any>(null);
    const [query, setQuery] = useState("");
    const [videoLoading, setVideoLoading] = useState(false);
    const [persona, setPersona] = useState("Technical"); // Technical, YouTuber, Teacher

    const handleTranscript = async (text: string) => {
        setQuery(text);
        setLoading(true);
        setDiagnosisData(null);
        setVideoData(null);
        setVideoLoading(false);

        try {
            const formData = new FormData();
            formData.append('query', text);
            formData.append('persona', persona);

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${apiUrl}/api/diagnose`, {
                method: 'POST',
                body: formData,
            });

            if (res.status === 504 || res.status === 502) {
                throw new Error("サーバーが混み合っているか、マニュアルの解析に時間がかかっています。もう一度お試しいただくか、少しお待ちください。");
            }

            if (!res.ok) {
                throw new Error("診断に失敗しました。インターネット接続やAPIの設定、マニュアルの有無を確認してください。");
            }

            const data: DiagnoseResponse = await res.json();
            setDiagnosisData(data);
            handleGenerateVideo(text, persona);

        } catch (error: any) {
            console.error(error);
            alert(error.message || "診断エラーが発生しました。しばらく待ってから再度お試しください。");
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateVideo = async (currentQuery: string, currentPersona: string) => {
        if (!currentQuery) return;
        setVideoLoading(true);
        try {
            const formData = new FormData();
            formData.append('query', currentQuery);
            formData.append('persona', currentPersona);

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${apiUrl}/api/generate_video`, {
                method: 'POST',
                body: formData,
            });

            if (!res.ok) {
                throw new Error("Failed to generate video");
            }

            const data = await res.json();
            setVideoData(data);
        } catch (error) {
            console.error("Video Generation Error", error);
        } finally {
            setVideoLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-sky-50 flex flex-col items-center py-12">
            <h1 className="text-4xl font-bold text-gray-800 mb-8 font-serif">Advisor Intelligence</h1>

            {!diagnosisData && !loading && (
                <div className="flex flex-col items-center">
                    <div className="flex gap-4 mb-8">
                        {[
                            { id: "Technical", label: "技術者モード", icon: "🔧" },
                            { id: "YouTuber", label: "YouTuber風", icon: "🎥" },
                            { id: "Teacher", label: "先生モード", icon: "🎓" }
                        ].map((p) => (
                            <button
                                key={p.id}
                                onClick={() => setPersona(p.id)}
                                className={`px-6 py-3 rounded-2xl flex items-center gap-2 transition-all shadow-md ${persona === p.id ? 'bg-orange-500 text-white scale-105 ring-4 ring-orange-200' : 'bg-white text-gray-600 hover:bg-gray-50'}`}
                            >
                                <span className="text-xl">{p.icon}</span>
                                <span className="font-bold">{p.label}</span>
                            </button>
                        ))}
                    </div>

                    <div className="bg-white p-12 rounded-3xl shadow-xl flex flex-col items-center">
                        <VoiceInput onTranscript={handleTranscript} />
                    </div>
                    {query && <p className="mt-4 text-xl text-gray-700">あなたの質問: 「{query}」</p>}
                </div>
            )}

            {loading && (
                <div className="flex flex-col items-center">
                    <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                    <p className="text-2xl text-gray-600 font-bold">マニュアルから解決策を探しています...</p>
                    <p className="text-gray-400 mt-2 animate-pulse">※初回や大きな質問は30秒ほどかかる場合があります</p>
                </div>
            )}

            {diagnosisData && (
                <div className="w-full max-w-4xl px-4 flex flex-col items-center animate-fade-in-up">
                    <button
                        onClick={() => { setDiagnosisData(null); setVideoData(null); setQuery(""); }}
                        className="mb-6 px-6 py-2 bg-gray-500 text-white rounded-full hover:bg-gray-600 transition-colors"
                    >
                        ← 別の質問をする
                    </button>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full mb-8">
                        {/* Diagnosis Card */}
                        <div className="bg-white p-8 rounded-3xl shadow-xl">
                            <h2 className="text-2xl font-bold text-gray-800 mb-4 border-b pb-2">💡 診断結果</h2>
                            <div className="space-y-4">
                                <div>
                                    <h3 className="font-bold text-orange-600">考えられる原因:</h3>
                                    <ul className="list-disc list-inside text-gray-700">
                                        {diagnosisData.probable_causes.map((cause, i) => (
                                            <li key={i}>{cause}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="font-bold text-blue-600">解決手順:</h3>
                                    <ol className="list-decimal list-inside text-gray-700 space-y-1">
                                        {diagnosisData.steps.map((step, i) => (
                                            <li key={i}>{step}</li>
                                        ))}
                                    </ol>
                                </div>
                                {diagnosisData.referenced_pages.length > 0 && (
                                    <p className="text-sm text-gray-500 mt-2">
                                        参照: マニュアル {diagnosisData.referenced_pages.join(", ")} ページ
                                    </p>
                                )}

                                {diagnosisData.visual_page_base64 && (
                                    <div className="mt-6 border rounded-xl overflow-hidden shadow-sm">
                                        <p className="bg-gray-50 text-[10px] uppercase tracking-wider text-gray-400 px-3 py-1 border-b">
                                            Manual Reference: {diagnosisData.source_file} (Page {diagnosisData.referenced_pages[0]})
                                        </p>
                                        <img
                                            src={`data:image/png;base64,${diagnosisData.visual_page_base64}`}
                                            alt="Manual Diagram"
                                            className="w-full h-auto cursor-zoom-in hover:scale-[1.02] transition-transform"
                                        />
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Video Card */}
                        <div className="bg-white p-8 rounded-3xl shadow-xl flex flex-col items-center justify-center min-h-[300px]">
                            <h2 className="text-2xl font-bold text-gray-800 mb-4 border-b pb-2 w-full text-center">📺 動画解説</h2>

                            {videoData ? (
                                <div className="w-full">
                                    <p className="mb-4 text-center text-gray-600">音声とスライドで解説します。</p>
                                    <VideoPlayer
                                        script={videoData.script}
                                        audioBase64={videoData.audio_base64}
                                        slides={videoData.slides}
                                    />
                                </div>
                            ) : videoLoading ? (
                                <div className="flex flex-col items-center">
                                    <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                                    <p className="text-orange-600 font-bold animate-pulse">解説動画を生成中...</p>
                                    <p className="text-sm text-gray-400 mt-2">※左の診断結果はすぐにご覧いただけます</p>
                                </div>
                            ) : (
                                <p className="text-gray-400">動画読み込みエラー</p>
                            )}
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100 mt-4 italic text-sm text-gray-500">
                        {diagnosisData.disclaimer}
                    </div>
                </div>
            )}
        </div>
    );
}
