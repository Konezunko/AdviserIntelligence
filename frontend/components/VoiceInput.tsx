'use client';

import React, { useState, useEffect } from 'react';
import 'regenerator-runtime/runtime';
import { Mic, Square } from 'lucide-react';

interface VoiceInputProps {
    onTranscript: (text: string) => void;
}

const VoiceInput: React.FC<VoiceInputProps> = ({ onTranscript }) => {
    const [isListening, setIsListening] = useState(false);
    const [recognition, setRecognition] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognitionInstance = new SpeechRecognition();
                recognitionInstance.lang = 'ja-JP';
                recognitionInstance.continuous = false;
                recognitionInstance.interimResults = false;

                recognitionInstance.onresult = (event: any) => {
                    const transcript = event.results[0][0].transcript;
                    onTranscript(transcript);
                    setIsListening(false);
                    setError(null);
                };

                recognitionInstance.onerror = (event: any) => {
                    console.error('Speech recognition error', event.error);
                    setIsListening(false);
                    if (event.error === 'not-allowed') {
                        setError("マイクの使用が許可されていません。ブラウザの設定を確認してください。");
                    } else if (event.error === 'no-speech') {
                        // Ignore no-speech, just reset
                        setError(null);
                    } else {
                        setError("音声認識エラーが発生しました。");
                    }
                };

                recognitionInstance.onend = () => {
                    setIsListening(false);
                }

                setRecognition(recognitionInstance);
            }
        }
    }, [onTranscript]);

    const toggleListening = () => {
        setError(null);
        if (isListening) {
            recognition?.stop();
        } else {
            try {
                recognition?.start();
                setIsListening(true);
            } catch (e) {
                console.error("Failed to start recognition", e);
            }
        }
    };

    if (!recognition) {
        return <div className="text-red-500">お使いのブラウザは音声入力に対応していません。Google Chromeをご利用ください。</div>;
    }

    return (
        <div className="flex flex-col items-center justify-center p-4">
            <button
                onClick={toggleListening}
                className={`w-64 h-64 rounded-full flex flex-col items-center justify-center transition-all duration-300 shadow-xl ${isListening
                    ? 'bg-red-500 animate-pulse scale-105'
                    : 'bg-blue-600 hover:bg-blue-700 hover:scale-105'
                    }`}
            >
                {isListening ? (
                    <>
                        <Square size={80} color="white" />
                        <span className="text-white text-2xl mt-4 font-bold">聞いています...</span>
                    </>
                ) : (
                    <>
                        <Mic size={80} color="white" />
                        <span className="text-white text-2xl mt-4 font-bold">困ったときは<br />ここを押して話す</span>
                    </>
                )}
            </button>
            <p className="mt-8 text-gray-600 text-lg">
                {error ? <span className="text-red-500 font-bold">{error}</span> :
                    (isListening ? "お話しください..." : "ボタンを押して、「インクが出ない」のように話しかけてください")}
            </p>

            <div className="mt-8 w-full max-w-md">
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        const input = (e.currentTarget.elements.namedItem('query') as HTMLInputElement);
                        if (input.value.trim()) {
                            onTranscript(input.value.trim());
                            input.value = '';
                        }
                    }}
                    className="flex flex-col items-center"
                >
                    <p className="text-gray-500 mb-2">または、文字で入力することもできます</p>
                    <div className="flex w-full">
                        <input
                            type="text"
                            name="query"
                            placeholder="例：インクが出ない"
                            className="flex-1 px-4 py-3 rounded-l-full border-2 border-gray-300 focus:border-blue-500 focus:outline-none text-lg"
                        />
                        <button
                            type="submit"
                            className="bg-blue-600 text-white px-6 py-3 rounded-r-full font-bold hover:bg-blue-700 transition-colors"
                        >
                            送信
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default VoiceInput;
