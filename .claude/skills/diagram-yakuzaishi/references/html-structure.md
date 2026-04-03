# HTML構造ガイド

## 基本テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【薬名・テーマ】服薬指導図解</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    /* 薬局・医療ブランドカラー */
    :root {
      --pharm-primary: #0f766e;      /* teal-700 */
      --pharm-secondary: #0369a1;    /* sky-700  */
      --pharm-accent: #f59e0b;       /* amber-500 */
      --pharm-gradient: linear-gradient(90deg, #0f766e, #0369a1);
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
    }

    /* ヘッダーグラデーション */
    .header-gradient {
      background: var(--pharm-gradient);
    }

    /* セクションカード */
    .section-card {
      background: white;
      border-radius: 1rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      padding: 2rem;
      margin-bottom: 2rem;
    }

    /* 用語解説ボックス */
    .term-explain {
      background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
      border-left: 4px solid #14b8a6;
      padding: 1.5rem;
      border-radius: 0.75rem;
      margin: 1.5rem 0;
    }
    .term-word { color: #0f766e; }

    /* キャラクター吹き出し */
    .char-bubble {
      position: relative;
      padding: 1.25rem;
      border-radius: 1rem;
      margin-left: 0.75rem;
    }
    .char-bubble::before {
      content: '';
      position: absolute;
      left: -10px;
      top: 20px;
      border-width: 10px;
      border-style: solid;
    }
    .rookie-bubble {
      background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
      border: 2px solid #f59e0b;
    }
    .rookie-bubble::before {
      border-color: transparent #f59e0b transparent transparent;
    }
    .senior-bubble {
      background: linear-gradient(135deg, #ccfbf1 0%, #99f6e4 100%);
      border: 2px solid #14b8a6;
    }
    .senior-bubble::before {
      border-color: transparent #14b8a6 transparent transparent;
    }

    /* 重要度バッジ */
    .badge-essential {
      background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .badge-important {
      background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .badge-note {
      background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    /* 警告ボックス */
    .warning-box {
      background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
      border-left: 4px solid #f97316;
      padding: 1.25rem;
      border-radius: 0.75rem;
      margin: 1rem 0;
    }

    /* 受診タイミングボックス */
    .visit-box {
      background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
      border-left: 4px solid #ef4444;
      padding: 1.25rem;
      border-radius: 0.75rem;
      margin: 1rem 0;
    }

    /* 目次 */
    .toc {
      position: fixed;
      right: 2rem;
      top: 50%;
      transform: translateY(-50%);
      background: white;
      padding: 1rem;
      border-radius: 0.75rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      max-height: 80vh;
      overflow-y: auto;
      z-index: 50;
    }
    @media (max-width: 1280px) {
      .toc { display: none; }
    }
  </style>
</head>
<body class="bg-gray-50">

  <!-- ヘッダー -->
  <header class="header-gradient text-white py-8">
    <div class="max-w-4xl mx-auto px-4">
      <div class="flex items-center gap-3 mb-2">
        <i data-lucide="pill" class="w-8 h-8"></i>
        <span class="text-sm font-medium opacity-80">服薬指導図解</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-bold">【タイトル】</h1>
      <p class="mt-2 text-lg opacity-90">サブタイトル</p>
    </div>
  </header>

  <!-- メインコンテンツ -->
  <main class="max-w-4xl mx-auto px-4 py-8">
    <!-- セクションをここに追加 -->
  </main>

  <!-- Lucide初期化 -->
  <script>lucide.createIcons();</script>
</body>
</html>
```

---

## Lucide Icon の使い方

### 基本構文

```html
<i data-lucide="icon-name" class="w-6 h-6"></i>
```

### 薬局・医療でよく使うアイコン

| 用途 | アイコン名 | コード |
|-----|----------|--------|
| 薬・錠剤 | `pill` | `<i data-lucide="pill" class="w-6 h-6 text-teal-600"></i>` |
| 注意 | `alert-circle` | `<i data-lucide="alert-circle" class="w-6 h-6 text-red-500"></i>` |
| 受診 | `hospital` | `<i data-lucide="hospital" class="w-6 h-6 text-red-500"></i>` |
| チェック | `check-circle` | `<i data-lucide="check-circle" class="w-6 h-6 text-green-500"></i>` |
| 情報 | `info` | `<i data-lucide="info" class="w-6 h-6 text-blue-500"></i>` |
| 警告 | `triangle-alert` | `<i data-lucide="triangle-alert" class="w-6 h-6 text-orange-500"></i>` |
| 時計 | `clock` | `<i data-lucide="clock" class="w-6 h-6 text-gray-500"></i>` |
| 食事 | `utensils` | `<i data-lucide="utensils" class="w-6 h-6 text-amber-500"></i>` |
| 禁止 | `ban` | `<i data-lucide="ban" class="w-6 h-6 text-red-500"></i>` |
| リスト | `list` | `<i data-lucide="list" class="w-6 h-6 text-gray-500"></i>` |
| メモ | `clipboard` | `<i data-lucide="clipboard" class="w-6 h-6 text-blue-500"></i>` |
| 矢印 | `arrow-right` | `<i data-lucide="arrow-right" class="w-6 h-6 text-gray-400"></i>` |
| 比較 | `git-compare` | `<i data-lucide="git-compare" class="w-6 h-6 text-purple-500"></i>` |
| ハート（健康） | `heart-pulse` | `<i data-lucide="heart-pulse" class="w-6 h-6 text-red-500"></i>` |
| 電話 | `phone` | `<i data-lucide="phone" class="w-6 h-6 text-green-500"></i>` |

---

## 薬の比較表

2つの薬を比較する場合はこのパターンを使う。

```html
<div class="section-card">
  <div class="flex items-center gap-3 mb-6">
    <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
      <i data-lucide="git-compare" class="w-6 h-6 text-purple-600"></i>
    </div>
    <div>
      <h2 class="text-2xl font-bold text-gray-800">〇〇 と △△ の違い</h2>
      <p class="text-gray-500">切り替え前後で変わること・変わらないこと</p>
    </div>
  </div>

  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-3 text-left font-bold text-gray-600">比較ポイント</th>
          <th class="p-3 text-center font-bold text-teal-700 bg-teal-50">〇〇（変更前）</th>
          <th class="p-3 text-center font-bold text-sky-700 bg-sky-50">△△（変更後）</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr>
          <td class="p-3 font-medium text-gray-700">目的</td>
          <td class="p-3 text-center bg-teal-50">〜〜</td>
          <td class="p-3 text-center bg-sky-50">〜〜</td>
        </tr>
        <tr>
          <td class="p-3 font-medium text-gray-700">飲む回数</td>
          <td class="p-3 text-center bg-teal-50">1日〇回</td>
          <td class="p-3 text-center bg-sky-50">1日〇回</td>
        </tr>
        <tr>
          <td class="p-3 font-medium text-gray-700">主な副作用</td>
          <td class="p-3 text-center bg-teal-50">〜〜</td>
          <td class="p-3 text-center bg-sky-50">〜〜</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

---

## 「患者様に必ず伝えること3つ」の書き方

```html
<div class="section-card">
  <div class="flex items-center gap-3 mb-6">
    <div class="w-12 h-12 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center">
      <i data-lucide="clipboard" class="w-6 h-6 text-white"></i>
    </div>
    <div>
      <h2 class="text-2xl font-bold text-gray-800">患者様に必ず伝えること</h2>
      <p class="text-gray-500">この3つをまず説明しましょう</p>
    </div>
  </div>

  <div class="grid gap-4">
    <!-- 1つ目 -->
    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-xl border-l-4 border-red-500">
      <div class="w-10 h-10 bg-red-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">1</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gray-800">何のための薬か</span>
          <span class="badge-essential">必ず</span>
        </div>
        <p class="text-gray-600">「〇〇のために飲む薬です」と目的を最初に確認してもらう</p>
      </div>
    </div>

    <!-- 2つ目 -->
    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl border-l-4 border-blue-500">
      <div class="w-10 h-10 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">2</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gray-800">飲み方の注意</span>
          <span class="badge-important">重要</span>
        </div>
        <p class="text-gray-600">「1日〇回、〇〇と一緒に/食後に飲んでください」</p>
      </div>
    </div>

    <!-- 3つ目 -->
    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-xl border-l-4 border-orange-500">
      <div class="w-10 h-10 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">3</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gray-800">こんな症状が出たら連絡を</span>
          <span class="badge-note">要確認</span>
        </div>
        <p class="text-gray-600">「〇〇の症状が出たら、薬局か医師に相談してください」</p>
      </div>
    </div>
  </div>
</div>
```

---

## 副作用の「受診タイミング」ボックス

```html
<div class="visit-box">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="hospital" class="w-6 h-6 text-red-600"></i>
    <span class="font-bold text-red-700 text-lg">こんな症状が出たらすぐに受診</span>
  </div>
  <ul class="space-y-2">
    <li class="flex items-start gap-2">
      <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
      <span>〇〇（症状）が続く・ひどくなる</span>
    </li>
    <li class="flex items-start gap-2">
      <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
      <span>△△（症状）が突然起きる</span>
    </li>
  </ul>
  <p class="mt-3 text-sm text-red-600 font-medium">
    ※ 心配なことはいつでも薬局にご相談ください
  </p>
</div>
```

---

## フローチャートの表現（服薬フロー）

```html
<div class="flex flex-col md:flex-row items-center justify-center gap-4 my-8">
  <div class="bg-teal-100 px-6 py-4 rounded-xl text-center min-w-28">
    <i data-lucide="clock" class="w-8 h-8 text-teal-600 mx-auto mb-2"></i>
    <div class="font-bold text-sm">朝食後</div>
  </div>
  <i data-lucide="arrow-right" class="w-8 h-8 text-gray-400 hidden md:block"></i>
  <i data-lucide="arrow-down" class="w-8 h-8 text-gray-400 md:hidden"></i>
  <div class="bg-sky-100 px-6 py-4 rounded-xl text-center min-w-28">
    <i data-lucide="pill" class="w-8 h-8 text-sky-600 mx-auto mb-2"></i>
    <div class="font-bold text-sm">服薬</div>
  </div>
  <i data-lucide="arrow-right" class="w-8 h-8 text-gray-400 hidden md:block"></i>
  <i data-lucide="arrow-down" class="w-8 h-8 text-gray-400 md:hidden"></i>
  <div class="bg-green-100 px-6 py-4 rounded-xl text-center min-w-28">
    <i data-lucide="heart-pulse" class="w-8 h-8 text-green-600 mx-auto mb-2"></i>
    <div class="font-bold text-sm">効果が続く</div>
  </div>
</div>
```
