# クイックカード HTMLテンプレート

現場で即使えるミニマム版。フル版を待たずに最初に出力する。

## 含む内容（この順番で）

1. ヘッダー（薬名・タグライン）
2. 30秒まとめ（3点カード）
3. 患者さんに必ず伝えること（3項目）
4. 比較表（比較がある場合）
5. すぐに受診すべき症状（赤ボックス）
6. フッター（「詳しくはフル版を参照」の案内）

## キャラクターについて

クイックカードにはキャラクター対話を**入れない**。
情報を素早く参照するためのカードなので、スッキリさせる。

## テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【薬名】服薬指導クイックカード</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Noto Sans JP', sans-serif; }

    /* 印刷時にも使いやすくする */
    @media print {
      .no-print { display: none; }
      body { background: white; }
      .section-card { box-shadow: none; border: 1px solid #e5e7eb; }
    }

    .header-gradient { background: linear-gradient(135deg, #0f766e, #0369a1); }

    .section-card {
      background: white;
      border-radius: 0.75rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      padding: 1.5rem;
      margin-bottom: 1.25rem;
    }

    .badge-essential {
      background: linear-gradient(135deg, #dc2626, #ef4444);
      color: white; padding: 0.15rem 0.55rem;
      border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
    }
    .badge-important {
      background: linear-gradient(135deg, #0369a1, #0284c7);
      color: white; padding: 0.15rem 0.55rem;
      border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
    }
    .badge-note {
      background: linear-gradient(135deg, #6b7280, #9ca3af);
      color: white; padding: 0.15rem 0.55rem;
      border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
    }
    .badge-danger {
      background: linear-gradient(135deg, #7c2d12, #b91c1c);
      color: white; padding: 0.15rem 0.55rem;
      border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
    }

    .visit-box {
      background: linear-gradient(135deg, #fef2f2, #fee2e2);
      border-left: 4px solid #dc2626;
      padding: 1.25rem; border-radius: 0.75rem;
    }
  </style>
</head>
<body class="bg-gray-50">

<!-- ヘッダー -->
<header class="header-gradient text-white py-6">
  <div class="max-w-2xl mx-auto px-4">
    <div class="flex items-center justify-between">
      <div>
        <div class="flex items-center gap-2 mb-1 opacity-80">
          <i data-lucide="pill" class="w-4 h-4"></i>
          <span class="text-xs font-medium">服薬指導クイックカード</span>
        </div>
        <h1 class="text-2xl font-bold">【薬名・テーマ】</h1>
      </div>
      <!-- 印刷ボタン（画面表示時のみ） -->
      <button onclick="window.print()"
        class="no-print bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-2 rounded-lg flex items-center gap-1 transition">
        <i data-lucide="printer" class="w-4 h-4"></i> 印刷
      </button>
    </div>
  </div>
</header>

<main class="max-w-2xl mx-auto px-4 py-5">

  <!-- 30秒まとめ -->
  <div class="bg-gradient-to-r from-teal-600 to-sky-700 text-white rounded-xl p-4 mb-5">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="zap" class="w-4 h-4 text-yellow-300"></i>
      <span class="font-bold text-xs tracking-wide">30秒まとめ</span>
    </div>
    <div class="grid grid-cols-3 gap-2">
      <div class="bg-white/15 rounded-lg p-2">
        <div class="font-bold text-xs mb-0.5">① ポイント1</div>
        <div class="text-xs opacity-90">説明文</div>
      </div>
      <div class="bg-white/15 rounded-lg p-2">
        <div class="font-bold text-xs mb-0.5">② ポイント2</div>
        <div class="text-xs opacity-90">説明文</div>
      </div>
      <div class="bg-white/15 rounded-lg p-2">
        <div class="font-bold text-xs mb-0.5">③ ポイント3</div>
        <div class="text-xs opacity-90">説明文</div>
      </div>
    </div>
  </div>

  <!-- 患者さんに必ず伝えること -->
  <div class="section-card">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center">
        <i data-lucide="clipboard" class="w-4 h-4 text-white"></i>
      </div>
      <h2 class="font-bold text-gray-800">患者さんに必ず伝えること</h2>
    </div>

    <div class="space-y-3">
      <!-- 1つ目 -->
      <div class="flex items-start gap-3 p-3 bg-red-50 rounded-xl border-l-4 border-red-500">
        <div class="w-7 h-7 bg-red-500 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">1</div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-bold text-sm text-gray-800">項目名</span>
            <span class="badge-essential">必ず</span>
          </div>
          <p class="text-gray-600 text-xs mt-0.5">説明文</p>
        </div>
      </div>

      <!-- 2つ目 -->
      <div class="flex items-start gap-3 p-3 bg-blue-50 rounded-xl border-l-4 border-blue-500">
        <div class="w-7 h-7 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">2</div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-bold text-sm text-gray-800">項目名</span>
            <span class="badge-important">重要</span>
          </div>
          <p class="text-gray-600 text-xs mt-0.5">説明文</p>
        </div>
      </div>

      <!-- 3つ目 -->
      <div class="flex items-start gap-3 p-3 bg-orange-50 rounded-xl border-l-4 border-orange-500">
        <div class="w-7 h-7 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">3</div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-bold text-sm text-gray-800">項目名</span>
            <span class="badge-note">注意</span>
          </div>
          <p class="text-gray-600 text-xs mt-0.5">説明文</p>
        </div>
      </div>
    </div>
  </div>

  <!-- 比較表（比較がある場合のみ） -->
  <div class="section-card">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
        <i data-lucide="git-compare" class="w-4 h-4 text-purple-600"></i>
      </div>
      <h2 class="font-bold text-gray-800">〇〇 と △△ の違い</h2>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-xs border-collapse">
        <thead>
          <tr class="bg-gray-50">
            <th class="p-2 text-left font-bold text-gray-500 border-b border-gray-200">比較</th>
            <th class="p-2 text-center font-bold text-teal-700 bg-teal-50 border-b border-teal-200">〇〇</th>
            <th class="p-2 text-center font-bold text-blue-700 bg-blue-50 border-b border-blue-200">△△</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr>
            <td class="p-2 font-medium text-gray-700">薬の形</td>
            <td class="p-2 text-center bg-teal-50">〜〜</td>
            <td class="p-2 text-center bg-blue-50">〜〜</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-gray-700">1日の回数</td>
            <td class="p-2 text-center bg-teal-50">〜〜</td>
            <td class="p-2 text-center bg-blue-50">〜〜</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-gray-700">特に注意</td>
            <td class="p-2 text-center bg-teal-50 text-red-600 font-medium">〜〜</td>
            <td class="p-2 text-center bg-blue-50 text-red-600 font-medium">〜〜</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- すぐに受診・連絡 -->
  <div class="visit-box mb-5">
    <div class="flex items-center gap-2 mb-2">
      <i data-lucide="hospital" class="w-4 h-4 text-red-600"></i>
      <span class="font-bold text-red-700 text-sm">こんな症状が出たらすぐ連絡</span>
    </div>
    <ul class="space-y-1 text-xs text-gray-700">
      <li class="flex items-start gap-1.5">
        <i data-lucide="alert-circle" class="w-3.5 h-3.5 text-red-500 flex-shrink-0 mt-0.5"></i>
        <span>症状1</span>
      </li>
      <li class="flex items-start gap-1.5">
        <i data-lucide="alert-circle" class="w-3.5 h-3.5 text-red-500 flex-shrink-0 mt-0.5"></i>
        <span>症状2</span>
      </li>
    </ul>
  </div>

  <!-- フル版へのリンク案内 -->
  <div class="no-print text-center py-3">
    <a href="./index.html"
      class="inline-flex items-center gap-2 bg-teal-600 hover:bg-teal-700 text-white text-sm px-5 py-2.5 rounded-xl transition font-medium">
      <i data-lucide="book-open" class="w-4 h-4"></i>
      フル版を見る（詳しい説明・たとえ話付き）
    </a>
  </div>

</main>

<footer class="bg-gray-100 border-t border-gray-200 py-4 mt-2">
  <div class="max-w-2xl mx-auto px-4 text-xs text-gray-400">
    服薬指導の参考資料です。最新の電子添付文書・処方内容に従ってください。
  </div>
</footer>

<script>lucide.createIcons();</script>
</body>
</html>
```

## クイックカード設計のポイント

- **最大2スクロールで読み終わる**量にする
- キャラクター対話・たとえ話は入れない（フル版に任せる）
- **印刷ボタンを必ず付ける**（カウンターで印刷して渡せる）
- フル版へのリンクボタンを末尾に置く
- フォントサイズは `text-xs` / `text-sm` で引き締める（情報密度を上げる）
