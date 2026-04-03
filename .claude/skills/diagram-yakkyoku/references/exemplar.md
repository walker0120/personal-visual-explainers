# 模範構造パターン

## パターン1: 薬の切り替え（前薬→新薬）

処方変更があったとき、前の薬との違いを患者に説明するための構造。

```
1. ヘッダー
   └─ タイトル（例:「○○から△△に変わります」）
   └─ サブタイトル（変更の理由を1行で）

2. 患者さんへ必ず伝えること ← 最上部に配置
   └─ 変更後の飲み方
   └─ 前の薬との一番大きな違い
   └─ すぐ受診が必要な症状

3. 前の薬との違い（比較カード）
   └─ 左: 前の薬  右: 新しい薬
   └─ 用法・副作用・注意が必要な人 を比較

4. 新しい薬の基本情報
   └─ 商品名・一般名・種類・主な効果

5. いつ飲む？（服薬タイミング図）
   └─ 朝/昼/夕/就寝のグリッドで視覚化
   └─ 食前/食後の補足

6. 副作用について
   └─ 「必ず伝える」（赤）
   └─ 「知っておくと良い」（黄）
   └─ 「まれ」（グレー）

7. 飲んではいけない・注意が必要な方（薬剤師確認）
   └─ 禁忌（赤）
   └─ 慎重投与（黄）
```

### HTMLの並べ方（例）

```html
<main class="max-w-2xl mx-auto px-4 py-6 space-y-4">
  <!-- 1. 必ず伝えること（最上部） -->
  <div class="bg-red-50 border-2 border-red-500 rounded-2xl p-5">...</div>

  <!-- 2. 前の薬との違い -->
  <div class="bg-white rounded-2xl shadow-sm p-5">...</div>

  <!-- 3. 新しい薬の基本情報 -->
  <div class="bg-white rounded-2xl shadow-sm p-5">...</div>

  <!-- 4. いつ飲む -->
  <div class="bg-white rounded-2xl shadow-sm p-5">...</div>

  <!-- 5. 副作用 -->
  <div class="bg-white rounded-2xl shadow-sm p-5">...</div>

  <!-- 6. 禁忌・注意（薬剤師確認） -->
  <div class="bg-white rounded-2xl shadow-sm p-5">...</div>
</main>
```

---

## パターン2: 副作用の説明（1剤）

副作用が多い薬や患者が不安を持ちやすい薬の説明に特化した構造。

```
1. ヘッダー
   └─ タイトル（例:「○○の副作用と対処法」）

2. 患者さんへ必ず伝えること
   └─ 出たらすぐ受診すべき症状（重篤な副作用）
   └─ 自分で対処できる軽い副作用

3. 薬の基本情報（簡略版）
   └─ 何の薬か・いつ飲むか を一言で

4. 副作用リスト
   └─ 必ず伝える（日常生活に影響が出るもの）
   └─ 知っておくと良い（出ることがある）
   └─ まれ（ごくまれだが注意）

5. 副作用が出たときの対処マップ
   └─ 「こんな症状が出たら → こうする」をフローで示す

6. 受診の目安カード
   └─ 「すぐ連絡」「次回受診時に相談」「経過観察で良い」
```

### 副作用が出たときの対処マップ（フロー例）

```html
<div class="bg-white rounded-2xl shadow-sm p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
      <i data-lucide="map" class="w-5 h-5 text-blue-700"></i>
    </div>
    <h2 class="text-lg font-bold text-gray-800">副作用が出たら</h2>
  </div>
  <div class="space-y-3">

    <!-- 重篤な副作用 -->
    <div class="flex items-start gap-3 p-3 bg-red-50 rounded-xl">
      <i data-lucide="siren" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
      <div class="flex-1">
        <p class="text-sm font-bold text-red-700">（症状）が出たら</p>
        <div class="flex items-center gap-2 mt-1">
          <i data-lucide="arrow-right" class="w-4 h-4 text-red-500"></i>
          <span class="text-sm font-bold text-red-700 bg-red-100 px-2 py-0.5 rounded-full">すぐに受診・連絡</span>
        </div>
      </div>
    </div>

    <!-- 日常的な副作用 -->
    <div class="flex items-start gap-3 p-3 bg-amber-50 rounded-xl">
      <i data-lucide="alert-circle" class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5"></i>
      <div class="flex-1">
        <p class="text-sm font-bold text-amber-700">（症状）が出たら</p>
        <div class="flex items-center gap-2 mt-1">
          <i data-lucide="arrow-right" class="w-4 h-4 text-amber-500"></i>
          <span class="text-sm text-amber-700">（対処法）。続く場合は次回受診時に相談</span>
        </div>
      </div>
    </div>

    <!-- 軽微な副作用 -->
    <div class="flex items-start gap-3 p-3 bg-green-50 rounded-xl">
      <i data-lucide="check-circle" class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5"></i>
      <div class="flex-1">
        <p class="text-sm font-bold text-green-700">（症状）が出たら</p>
        <div class="flex items-center gap-2 mt-1">
          <i data-lucide="arrow-right" class="w-4 h-4 text-green-500"></i>
          <span class="text-sm text-green-700">（対処法）。多くは続けるうちに慣れます</span>
        </div>
      </div>
    </div>

  </div>
</div>
```

---

## 図解全体の設計方針

### 情報の優先順位
1. **患者が今日から行動すべきこと**（一番上）
2. **違い・変化**（前の薬と比較）
3. **日常の注意**（飲み方・副作用）
4. **薬剤師確認事項**（禁忌・慎重投与）

### ボリュームの目安
- セクション数: 4〜6個
- 1セクションの行数: 3〜6項目まで
- 全体の読了時間: 1分以内

### 色の意味を統一する

| 色 | 意味 | 使う場面 |
|---|------|---------|
| 赤（red） | 緊急・禁止 | 必ず伝えること、禁忌、すぐ受診 |
| 黄・橙（amber/orange） | 注意 | 副作用「知っておくと良い」、慎重投与 |
| 緑（green/teal） | 通常・安心 | 薬の情報、対処できる副作用 |
| 青（blue） | 参考情報 | 服薬タイミング、ヒント |
| グレー（gray） | 軽微・任意 | まれな副作用、省略可能な情報 |
