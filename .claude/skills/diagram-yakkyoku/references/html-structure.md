# HTML構造ガイド

## 基本テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【薬名】服薬指導</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['Noto Sans JP', 'sans-serif'] }
        }
      }
    }
  </script>
</head>
<body class="bg-teal-50 font-sans">

  <!-- ヘッダー -->
  <header class="bg-gradient-to-r from-teal-700 to-green-700 text-white py-6">
    <div class="max-w-2xl mx-auto px-4">
      <div class="text-sm font-medium text-teal-200 mb-1">服薬指導図解</div>
      <h1 class="text-2xl md:text-3xl font-bold">【薬名】</h1>
      <p class="mt-1 text-base text-teal-100">サブタイトル（例：前の薬との違い）</p>
    </div>
  </header>

  <!-- メインコンテンツ -->
  <main class="max-w-2xl mx-auto px-4 py-6 space-y-4">
    <!-- ここにコンポーネントを並べる -->
  </main>

  <!-- Lucide初期化 -->
  <script>lucide.createIcons();</script>
</body>
</html>
```

---

## コンポーネント一覧

### 1. 「患者さんへ必ず伝えること」ボックス（最上部に必ず置く）

```html
<div class="bg-red-50 border-2 border-red-500 rounded-2xl p-5">
  <div class="flex items-center gap-2 mb-3">
    <div class="w-9 h-9 bg-red-500 rounded-xl flex items-center justify-center flex-shrink-0">
      <i data-lucide="alert-circle" class="w-5 h-5 text-white"></i>
    </div>
    <h2 class="text-lg font-bold text-red-700">患者さんへ必ず伝えること</h2>
  </div>
  <ul class="space-y-2">
    <li class="flex items-start gap-2">
      <i data-lucide="check-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
      <span class="text-gray-800">（伝えること1）</span>
    </li>
    <li class="flex items-start gap-2">
      <i data-lucide="check-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
      <span class="text-gray-800">（伝えること2）</span>
    </li>
  </ul>
</div>
```

---

### 2. 薬の基本情報カード

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-teal-100 rounded-xl flex items-center justify-center">
      <i data-lucide="pill" class="w-5 h-5 text-teal-700"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">薬の基本情報</h2>
      <p class="text-sm text-gray-500">一般名 / 商品名</p>
    </div>
  </div>
  <dl class="space-y-2">
    <div class="flex gap-3">
      <dt class="text-sm font-medium text-gray-500 w-20 flex-shrink-0">商品名</dt>
      <dd class="text-gray-800 font-bold">（薬名）</dd>
    </div>
    <div class="flex gap-3">
      <dt class="text-sm font-medium text-gray-500 w-20 flex-shrink-0">一般名</dt>
      <dd class="text-gray-800">（一般名）</dd>
    </div>
    <div class="flex gap-3">
      <dt class="text-sm font-medium text-gray-500 w-20 flex-shrink-0">種類</dt>
      <dd class="text-gray-800">（薬効分類）</dd>
    </div>
    <div class="flex gap-3">
      <dt class="text-sm font-medium text-gray-500 w-20 flex-shrink-0">主な効果</dt>
      <dd class="text-gray-800">（効能を患者向けの言葉で）</dd>
    </div>
  </dl>
</div>
```

---

### 3. 服薬タイミング図

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
      <i data-lucide="clock" class="w-5 h-5 text-blue-700"></i>
    </div>
    <h2 class="text-lg font-bold text-gray-800">いつ飲む？</h2>
  </div>
  <div class="grid grid-cols-3 gap-3">
    <!-- 朝：飲む場合 -->
    <div class="bg-amber-50 border-2 border-amber-400 rounded-xl p-3 text-center">
      <i data-lucide="sunrise" class="w-7 h-7 text-amber-500 mx-auto mb-1"></i>
      <div class="text-sm font-bold text-amber-700">朝</div>
      <div class="text-xs text-amber-600 mt-1">食後 1錠</div>
    </div>
    <!-- 昼：飲まない場合 -->
    <div class="bg-gray-50 border-2 border-gray-200 rounded-xl p-3 text-center opacity-40">
      <i data-lucide="sun" class="w-7 h-7 text-gray-400 mx-auto mb-1"></i>
      <div class="text-sm font-bold text-gray-400">昼</div>
      <div class="text-xs text-gray-400 mt-1">なし</div>
    </div>
    <!-- 夕：飲む場合 -->
    <div class="bg-indigo-50 border-2 border-indigo-400 rounded-xl p-3 text-center">
      <i data-lucide="sunset" class="w-7 h-7 text-indigo-500 mx-auto mb-1"></i>
      <div class="text-sm font-bold text-indigo-700">夕</div>
      <div class="text-xs text-indigo-600 mt-1">食後 1錠</div>
    </div>
  </div>
  <!-- 食前/食後の補足（必要な場合） -->
  <div class="mt-3 bg-blue-50 rounded-xl p-3 flex items-start gap-2">
    <i data-lucide="info" class="w-4 h-4 text-blue-500 flex-shrink-0 mt-0.5"></i>
    <p class="text-sm text-blue-700">食後30分以内に飲んでください。食事を抜いた場合は飲み方を変えてください。</p>
  </div>
</div>
```

---

### 4. 副作用リスト（重要度バッジ付き）

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-orange-100 rounded-xl flex items-center justify-center">
      <i data-lucide="triangle-alert" class="w-5 h-5 text-orange-600"></i>
    </div>
    <h2 class="text-lg font-bold text-gray-800">副作用について</h2>
  </div>
  <div class="space-y-2">
    <!-- 必ず伝える -->
    <div class="flex items-start gap-3 p-3 bg-red-50 rounded-xl border-l-4 border-red-500">
      <span class="text-xs font-bold bg-red-500 text-white px-2 py-0.5 rounded-full flex-shrink-0 mt-0.5">必ず伝える</span>
      <div>
        <p class="font-bold text-gray-800 text-sm">（副作用名）</p>
        <p class="text-xs text-gray-600 mt-0.5">（患者向けの説明。例：めまいがすることがあります。立ち上がるときはゆっくり）</p>
      </div>
    </div>
    <!-- 知っておくと良い -->
    <div class="flex items-start gap-3 p-3 bg-amber-50 rounded-xl border-l-4 border-amber-400">
      <span class="text-xs font-bold bg-amber-400 text-white px-2 py-0.5 rounded-full flex-shrink-0 mt-0.5">知っておくと良い</span>
      <div>
        <p class="font-bold text-gray-800 text-sm">（副作用名）</p>
        <p class="text-xs text-gray-600 mt-0.5">（患者向けの説明）</p>
      </div>
    </div>
    <!-- まれ -->
    <div class="flex items-start gap-3 p-3 bg-gray-50 rounded-xl border-l-4 border-gray-300">
      <span class="text-xs font-bold bg-gray-400 text-white px-2 py-0.5 rounded-full flex-shrink-0 mt-0.5">まれ</span>
      <div>
        <p class="font-bold text-gray-800 text-sm">（副作用名）</p>
        <p class="text-xs text-gray-600 mt-0.5">（患者向けの説明）</p>
      </div>
    </div>
  </div>
</div>
```

---

### 5. 薬の比較カード（左右対比）

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
      <i data-lucide="arrow-left-right" class="w-5 h-5 text-purple-700"></i>
    </div>
    <h2 class="text-lg font-bold text-gray-800">前の薬との違い</h2>
  </div>
  <div class="grid grid-cols-2 gap-3 mb-4">
    <div class="bg-gray-100 rounded-xl p-3 text-center">
      <div class="text-xs text-gray-500 mb-1">前の薬</div>
      <div class="font-bold text-gray-700">（前の薬名）</div>
    </div>
    <div class="bg-teal-100 rounded-xl p-3 text-center">
      <div class="text-xs text-teal-600 mb-1">新しい薬</div>
      <div class="font-bold text-teal-800">（新しい薬名）</div>
    </div>
  </div>
  <!-- 比較行 -->
  <div class="space-y-2">
    <div class="grid grid-cols-3 gap-2 items-center text-sm">
      <div class="text-center p-2 bg-gray-50 rounded-lg text-gray-700">（前薬の値/特徴）</div>
      <div class="text-center text-xs font-medium text-gray-500">用法</div>
      <div class="text-center p-2 bg-teal-50 rounded-lg text-teal-700 font-medium">（新薬の値/特徴）</div>
    </div>
    <div class="grid grid-cols-3 gap-2 items-center text-sm">
      <div class="text-center p-2 bg-gray-50 rounded-lg text-gray-700">（前薬の値）</div>
      <div class="text-center text-xs font-medium text-gray-500">主な副作用</div>
      <div class="text-center p-2 bg-teal-50 rounded-lg text-teal-700 font-medium">（新薬の値）</div>
    </div>
    <div class="grid grid-cols-3 gap-2 items-center text-sm">
      <div class="text-center p-2 bg-gray-50 rounded-lg text-gray-700">（前薬の値）</div>
      <div class="text-center text-xs font-medium text-gray-500">注意が必要な人</div>
      <div class="text-center p-2 bg-teal-50 rounded-lg text-teal-700 font-medium">（新薬の値）</div>
    </div>
  </div>
</div>
```

---

### 6. 禁忌・注意カード（薬剤師確認セクション）

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
      <i data-lucide="shield-x" class="w-5 h-5 text-red-600"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">飲んではいけない・注意が必要な方</h2>
      <p class="text-xs text-gray-500">薬剤師確認ポイント</p>
    </div>
  </div>
  <!-- 禁忌 -->
  <div class="mb-3">
    <div class="text-xs font-bold text-red-600 mb-2 flex items-center gap-1">
      <i data-lucide="x-circle" class="w-4 h-4"></i> 飲んではいけない方（禁忌）
    </div>
    <ul class="space-y-1">
      <li class="flex items-center gap-2 text-sm text-gray-700">
        <i data-lucide="x" class="w-4 h-4 text-red-500 flex-shrink-0"></i>
        （禁忌の内容）
      </li>
    </ul>
  </div>
  <!-- 慎重投与 -->
  <div>
    <div class="text-xs font-bold text-amber-600 mb-2 flex items-center gap-1">
      <i data-lucide="alert-triangle" class="w-4 h-4"></i> 特に注意が必要な方
    </div>
    <ul class="space-y-1">
      <li class="flex items-center gap-2 text-sm text-gray-700">
        <i data-lucide="alert-circle" class="w-4 h-4 text-amber-500 flex-shrink-0"></i>
        （慎重投与の内容）
      </li>
    </ul>
  </div>
</div>
```

---

### 7. 用語解説ボックス（専門用語を使うとき）

```html
<div class="bg-purple-50 border-l-4 border-purple-500 rounded-xl p-4 my-3">
  <div class="flex items-start gap-3">
    <i data-lucide="lightbulb" class="w-5 h-5 text-purple-500 flex-shrink-0 mt-0.5"></i>
    <div>
      <div class="font-bold text-purple-700 text-sm">「（専門用語）」とは？</div>
      <div class="text-sm text-gray-700 mt-1">
        （患者向けの平易な説明。term-dictionary.md を参照）
      </div>
    </div>
  </div>
</div>
```

---

## Lucide Icon — 薬局でよく使うアイコン

| 用途 | アイコン名 | コード例 |
|-----|----------|---------|
| 薬・錠剤 | `pill` | `<i data-lucide="pill" class="w-5 h-5 text-teal-600"></i>` |
| 時間・タイミング | `clock` | `<i data-lucide="clock" class="w-5 h-5 text-blue-600"></i>` |
| 警告・副作用 | `triangle-alert` | `<i data-lucide="triangle-alert" class="w-5 h-5 text-orange-500"></i>` |
| 禁止 | `shield-x` | `<i data-lucide="shield-x" class="w-5 h-5 text-red-600"></i>` |
| 必須確認 | `alert-circle` | `<i data-lucide="alert-circle" class="w-5 h-5 text-red-500"></i>` |
| 朝 | `sunrise` | `<i data-lucide="sunrise" class="w-6 h-6 text-amber-500"></i>` |
| 昼 | `sun` | `<i data-lucide="sun" class="w-6 h-6 text-yellow-500"></i>` |
| 夕・夜 | `sunset` | `<i data-lucide="sunset" class="w-6 h-6 text-indigo-500"></i>` |
| 就寝 | `moon` | `<i data-lucide="moon" class="w-6 h-6 text-blue-800"></i>` |
| チェック | `check-circle` | `<i data-lucide="check-circle" class="w-5 h-5 text-green-500"></i>` |
| 比較 | `arrow-left-right` | `<i data-lucide="arrow-left-right" class="w-5 h-5 text-purple-600"></i>` |
| 情報 | `info` | `<i data-lucide="info" class="w-5 h-5 text-blue-500"></i>` |
| ヒント | `lightbulb` | `<i data-lucide="lightbulb" class="w-5 h-5 text-yellow-500"></i>` |
| 病院・通院 | `hospital` | `<i data-lucide="hospital" class="w-5 h-5 text-blue-600"></i>` |
