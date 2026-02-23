
import Link from 'next/link';
import FileUpload from "@/components/FileUpload";

export default function Home() {
  return (
    <div className="min-h-screen bg-sky-50 flex flex-col items-center justify-center p-4">
      <main className="w-full max-w-2xl text-center space-y-12">

        <div className="space-y-4">
          <h1 className="text-5xl font-extrabold text-blue-900 tracking-tight">
            Advisor Intelligence
          </h1>
          <p className="text-xl text-blue-700">
            Canon TS6330 専用サポート AI
          </p>
        </div>

        <Link
          href="/diagnose"
          className="block w-full max-w-md mx-auto bg-blue-600 hover:bg-blue-700 text-white text-3xl font-bold py-8 rounded-3xl shadow-2xl transition transform hover:scale-105"
        >
          相談をはじめる
        </Link>

        <div className="pt-20 border-t border-gray-200">
          <p className="text-sm font-bold text-gray-500 mb-4">管理者用メニュー</p>
          <FileUpload />
        </div>

      </main>
    </div>
  );
}
