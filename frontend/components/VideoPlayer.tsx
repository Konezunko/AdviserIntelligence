'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Rewind } from 'lucide-react';

interface Slide {
    type: string;
    text: string;
    image?: string;
}

interface VideoPlayerProps {
    script: string;
    audioBase64: string;
    slides: Slide[];
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ script, audioBase64, slides }) => {
    const audioRef = useRef<HTMLAudioElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.src = `data:audio/mp3;base64,${audioBase64}`;
            audioRef.current.load();
        }
    }, [audioBase64]);

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const rewind10 = () => {
        if (audioRef.current) {
            audioRef.current.currentTime = Math.max(0, audioRef.current.currentTime - 10);
        }
    };

    const handleTimeUpdate = () => {
        if (audioRef.current) {
            setCurrentTime(audioRef.current.currentTime);
        }
    };

    const handleLoadedMetadata = () => {
        if (audioRef.current) {
            setDuration(audioRef.current.duration);
        }
    }

    const handleEnded = () => {
        setIsPlaying(false);
    }

    // Simple slide logic: just show the first slide for now, or rotate if multiple
    // In a real app, we'd map timestamps to slides.
    const currentSlide = slides[0];

    return (
        <div className="flex flex-col items-center w-full max-w-2xl mx-auto p-4 bg-white rounded-xl shadow-lg">

            {/* Visual Area (Slide) */}
            <div className="w-full aspect-video bg-gray-100 mb-6 rounded-lg flex items-center justify-center border-2 border-gray-200 overflow-hidden relative">
                {currentSlide?.image ? (
                    <img src={currentSlide.image} alt="Slide" className="object-cover w-full h-full" />
                ) : (
                    <div className="p-8 text-center">
                        <h2 className="text-3xl font-bold text-gray-800 mb-4">{currentSlide?.text || "解説"}</h2>
                        <p className="text-gray-500">（ここにマニュアルの図解が表示されます）</p>
                    </div>
                )}

                {/* Audio Element (Hidden) */}
                <audio
                    ref={audioRef}
                    onTimeUpdate={handleTimeUpdate}
                    onLoadedMetadata={handleLoadedMetadata}
                    onEnded={handleEnded}
                />
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-4 mb-6">
                <div
                    className="bg-blue-600 h-4 rounded-full transition-all duration-300"
                    style={{ width: `${(currentTime / duration) * 100}%` }}
                ></div>
            </div>

            {/* Controls */}
            <div className="flex gap-8">
                <button
                    onClick={rewind10}
                    className="flex flex-col items-center justify-center w-24 h-24 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
                >
                    <Rewind size={40} className="text-gray-700" />
                    <span className="text-sm font-bold text-gray-700 mt-1">10秒戻る</span>
                </button>

                <button
                    onClick={togglePlay}
                    className="flex flex-col items-center justify-center w-32 h-32 bg-blue-600 rounded-full hover:bg-blue-700 transition-colors shadow-lg"
                >
                    {isPlaying ? (
                        <>
                            <Pause size={60} className="text-white" />
                            <span className="text-lg font-bold text-white mt-1">一時停止</span>
                        </>
                    ) : (
                        <>
                            <Play size={60} className="text-white ml-2" />
                            <span className="text-lg font-bold text-white mt-1">再生</span>
                        </>
                    )}
                </button>
            </div>

            {/* Script Display (Optional) */}
            <div className="mt-8 p-4 bg-gray-50 rounded w-full h-48 overflow-y-auto border border-gray-200">
                <p className="text-gray-700 whitespace-pre-wrap leading-relaxed text-lg">{script}</p>
            </div>

        </div>
    );
};

export default VideoPlayer;
