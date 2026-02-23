# Advisor Intelligence PoC システム仕様書

## 1. プロダクト概要
製品名: Advisor Intelligence (TS6330 向け PoC 版)
目的: 既存の PDF マニュアルをソースとし、ユーザーの質問に対して AI が最適な解決手順を抽出、ナレーション付きのレクチャー動画をオンデマンドで生成・提示する 。
ターゲット: プリンターの操作に不慣れな高齢者、長文マニュアルを読みたくない若年層 。

## 2. システム構成 (ワークフロー)

以下の 3 つのレイヤーで構成します。

| レイヤー | 使用技術 (想定) | 役割 |
| :--- | :--- | :--- |
| **データソース** | Canon TS6330 PDF マニュアル | 知識の源泉 。 |
| **ナレッジ解析 (RAG)** | LLM (Gemini 1.5 Pro / Flash) | ユーザーの質問に対し、PDF から該当箇所を検索・要約 。 |
| **動画生成エンジン** | Mock Engine (Slideshow + TTS) | 抽出した手順を元に、ナレーション（NotebookLM風の対話形式）とスライド動画を自動合成 。 |

3. 機能要件

① インテリジェント検索・要約機能
*   ユーザーが「インクの替え方は？」と入力すると、LLM がマニュアルの該当ページを特定する 。
*   専門用語（例：プリントヘッドホルダー）を、初心者でも分かる表現（例：インクを入れる場所）に変換して解説文を作成する 。

② オンデマンド動画生成機能
*   ナレーション生成: テキストから聞き取りやすい音声を合成する 。
*   ビジュアル合成: マニュアル内の図解やイラストをズームアップし、操作箇所を強調する演出を加える (PoCではスライドショー形式を想定)。
*   短尺化: 1 動画あたり 30 秒〜 60 秒に収め、視聴者の集中力を維持する 。

③ 超シンプル UI/UX
*   入力: テキスト入力だけでなく、音声入力（ボイスコマンド）にも対応。
*   出力: 「再生」「一時停止」「10秒戻し」の 3 つの巨大ボタンのみを配置した専用プレーヤー 。


4. データフロー (RAG + Video Generation Logic)

1.  **Ingestion (学習)**:
    *   管理者（または初回起動時）が `/api/ingest` を実行。
    *   `backend/manuals/*.pdf` を読み込み、チャンク分割してEmbedding（ベクトル化）を行い、ChromaDBに保存。

2.  **Diagnosis & Generation (診断・動画生成)**:
    *   ユーザーが音声またはテキストで質問（例：「インク交換」）。
    *   フロントエンドが `POST /api/diagnose` (または `/api/generate_video`) をコール。
    *   バックエンドが質問内容を解析し、ベクトル検索を実行。
    *   LLM (GPT-4o) がマニュアル情報を元に「わかりやすい解説スクリプト」と「視覚演出指示（スライド/ズーム）」を生成。
    *   (PoC) 音声合成 (TTS) で解説スクリプトを音声化 + 視覚演出指示を元にスライドショー情報をJSONで返す。
    *   フロントエンドが音声と画像を同期再生 (動画プレーヤー風UI)。

5. ディレクトリ構成

```
AdviserIntelligence/
├── backend/
│   ├── app/
│   │   ├── main.py       # APIエントリーポイント
│   │   ├── rag.py        # RAGロジック（Ingestion/Retrieval）
│   │   ├── video_gen.py  # (New) 動画生成ロジック (Mock/TTS)
│   │   └── schemas.py    # Pydanticモデル
│   ├── manuals/          # PDFマニュアル配置場所
│   ├── db/               # ChromaDB 永続化データ
│   └── requirements.txt  # 依存ライブラリ
└── frontend/
    ├── app/
    │   ├── page.tsx          # トップページ (Simple Dashboard)
    │   ├── diagnose/page.tsx # お悩み解決ページ (Video Player)
    │   └── ...
    └── components/
        ├── VideoPlayer.tsx   # (New) 動画再生・操作UI
        └── VoiceInput.tsx    # (New) 音声入力コンポーネント
```

6. 前提条件
*   **OpenAI API Key**: バックエンドの `.env` に設定が必要。
*   **PDFマニュアル**: `backend/manuals` に配置が必要。
*   (Optional) **Voice API**: Browser Native API or External Service.

7. 今後の拡張性
*   本格的な動画生成 (Sora / HeyGen) の統合。
*   画像解析による症状特定（マルチモーダルRAG）。
*   フィードバックループによる精度向上。
