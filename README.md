# Advisor Intelligence PoC (Canon TS6330 Support)

Canon TS6330 プリンターのトラブルシューティングを支援するAIアプリケーションです。
RAG (Retrieval-Augmented Generation) 技術を使用し、PDFマニュアルに基づいた回答を提供します。

## 事前準備

### 1. Google API Keyの取得
Google AI (Gemini) を使用するため、APIキーが必要です。
`backend/.env` ファイルを作成し、以下のように設定してください。

```bash
# backend/.env
GOOGLE_API_KEY=AIza...
```

### 2. 仮想環境のセットアップ (初回のみ)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. フロントエンドのセットアップ (初回のみ)
```powershell
cd frontend
npm install
```

## アプリケーションの起動方法

ターミナルを2つ開き、それぞれでバックエンドとフロントエンドを起動します。

### ターミナル1: バックエンド (FastAPI)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```
*   サーバーが `http://127.0.0.1:8000` で起動します。

### ターミナル2: フロントエンド (Next.js)
```powershell
cd frontend
npm run dev
```
*   サーバーが `http://localhost:3000` で起動します。

## 使いかた

1. **ブラウザでアクセス**
   `http://localhost:3000` を開きます。

2. **マニュアルの登録 (初回または更新時)**
   ページ下部の「ドキュメント登録」セクションに、Canon TS6330のマニュアルPDFをドラッグ＆ドロップ（またはクリックして選択）します。
   *   アップロード後、バックグラウンドでAIの学習（取り込み）が始まります。
   *   **注意**: 無料版API制限のため、取り込みはゆっくり行われます（10秒に1ページ程度）。完了までしばらくお待ちください。

3. **診断の実行**
   トップページの「症状を選択してください」から、該当する症状（例：「コピー時に変な模様が出る」）をクリックします。
   質問に回答し、「診断する」ボタンを押すと、マニュアルに基づいたAIの回答が表示されます。
