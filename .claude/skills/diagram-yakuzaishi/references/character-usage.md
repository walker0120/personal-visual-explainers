# キャラクター利用ガイド

## キャラクターの役割

| キャラクター | 役割 | 設定 |
|------------|------|------|
| **ルーキーさん** | 読者（新人薬剤師）の代弁者。患者さんへの説明に迷うことがある | 入局1〜2年目の新人薬剤師 |
| **センパイさん** | 導き手。患者さんにわかりやすく伝えるノウハウを持つ | 10年以上の経験を持つベテラン薬剤師 |

---

## アバターの実装

キャラクター画像は使わず、イニシャルアバターで表現する。

```html
<!-- ルーキーさんのアバター -->
<div class="w-16 h-16 rounded-full bg-amber-400 flex items-center justify-center flex-shrink-0">
  <span class="text-white font-bold text-xl">R</span>
</div>

<!-- センパイさんのアバター -->
<div class="w-16 h-16 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0">
  <span class="text-white font-bold text-xl">S</span>
</div>
```

---

## 対話パターン

### 1. 導入パターン（疑問→答え）

```html
<!-- ルーキーさん: 疑問を投げかける -->
<div class="flex items-start gap-4 mb-6">
  <div class="w-16 h-16 rounded-full bg-amber-400 flex items-center justify-center flex-shrink-0">
    <span class="text-white font-bold text-xl">R</span>
  </div>
  <div class="char-bubble rookie-bubble flex-1">
    <p class="text-base">
      <span class="font-bold text-amber-700">ルーキーさん:</span><br>
      センパイ、患者さんに〇〇から△△に切り替わりましたって説明するんですが、
      何をどう話せばいいか迷ってしまって…
    </p>
  </div>
</div>

<!-- センパイさん: 本質を説明 -->
<div class="flex items-start gap-4 mb-6">
  <div class="w-16 h-16 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0">
    <span class="text-white font-bold text-xl">S</span>
  </div>
  <div class="char-bubble senior-bubble flex-1">
    <p class="text-base">
      <span class="font-bold text-teal-700">センパイさん:</span><br>
      まずは「何のための薬か」を確認してもらうところから始めると、
      患者さんも安心してくれますよ。
    </p>
  </div>
</div>
```

### 2. 驚きパターン（気づきの瞬間）

```html
<div class="flex items-start gap-4 mb-6">
  <div class="w-16 h-16 rounded-full bg-amber-400 flex items-center justify-center flex-shrink-0">
    <span class="text-white font-bold text-xl">R</span>
  </div>
  <div class="char-bubble rookie-bubble flex-1">
    <p class="text-base">
      <span class="font-bold text-amber-700">ルーキーさん:</span><br>
      そっか！成分が違っても目的は同じ、だから患者さんの生活には
      ほとんど変化がないってことを伝えればいいんですね！
    </p>
  </div>
</div>
```

### 3. まとめパターン（確認）

```html
<div class="flex items-start gap-4 mb-6">
  <div class="w-16 h-16 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0">
    <span class="text-white font-bold text-xl">S</span>
  </div>
  <div class="char-bubble senior-bubble flex-1">
    <p class="text-base">
      <span class="font-bold text-teal-700">センパイさん:</span><br>
      整理すると、患者さんに必ず伝えることは3つです。
    </p>
  </div>
</div>

<div class="flex items-start gap-4 mb-6">
  <div class="w-16 h-16 rounded-full bg-amber-400 flex items-center justify-center flex-shrink-0">
    <span class="text-white font-bold text-xl">R</span>
  </div>
  <div class="char-bubble rookie-bubble flex-1">
    <p class="text-base">
      <span class="font-bold text-amber-700">ルーキーさん:</span><br>
      これなら自信を持って説明できます！ありがとうございます！
    </p>
  </div>
</div>
```

---

## セリフの書き方

### ルーキーさんの特徴

- **一人称**: 「私」
- **口調**: 丁寧語、少し不安げ
- **疑問の切り口**: 患者さんが聞きそうなことを薬剤師視点で代弁する
- **気づき**: 少し大げさに「そっか！」「なるほど！」

```
❌ 悪い例: 「この薬はCa拮抗薬ですよね？」
✅ 良い例: 「患者さんに副作用が出たとき、どのタイミングで受診を勧めればいいですか？」
```

### センパイさんの特徴

- **一人称**: 「私」
- **口調**: 落ち着いた丁寧語
- **説明**: 患者さんへの伝え方をそのまま示す
- **名前呼び**: 「ルーキーさん」

```
❌ 悪い例: 「アムロジピンの血中半減期は約35〜50時間です」
✅ 良い例: 「患者さんには『ゆっくり効いて、ゆっくり抜けていく薬なので、飲み忘れても慌てなくて大丈夫です』と伝えてみてください」
```

---

## 配置ルール

1. **対話シーンは上から順番に配置**（左右固定しない）
2. **アバターサイズ**: `w-16 h-16`（64px）が基本
3. **吹き出しの向き**: アバター側に尖端
4. **余白**: `gap-4`、`mb-6` で統一
