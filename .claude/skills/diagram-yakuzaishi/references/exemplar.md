# 模範解答パターン

## 成功する図解の構造

```
1. ヘッダー（ティールグラデーション背景）
   └─ 薬名・テーマ + 「服薬指導図解」のラベル

2. 導入（キャラクター対話）
   └─ ルーキーさん: 「この薬、患者さんにどう説明すれば…」
   └─ センパイさん: たとえ話で概要説明

3. 用語解説ボックス
   └─ 最初に出てくる医療用語を全て解説

4. 患者様に必ず伝えること3つ
   └─ 何のための薬か / 飲み方 / こんな時は連絡を
   └─ 重要度バッジ（必ず/重要/要確認）

5. 薬の比較表（切り替えがある場合）
   └─ 変わること・変わらないことを表形式で

6. 各セクション詳細
   └─ セクションカード形式
   └─ Lucide iconでビジュアル化
   └─ 身近なたとえ話で補足
   └─ 副作用には「受診タイミング」を必ず付ける

7. まとめ（キャラクター対話）
   └─ センパイさん: 要点を3つで整理
   └─ ルーキーさん: 「これで説明できます！」

8. 目次（フローティング、デスクトップのみ）
```

---

## 「たとえ話」の展開パターン

### パターン1: 薬の作用を日常のもので例える

```html
<div class="bg-gradient-to-r from-teal-50 to-cyan-50 p-6 rounded-xl border border-teal-200 my-6">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="lightbulb" class="w-6 h-6 text-teal-600"></i>
    <span class="font-bold text-teal-800">たとえ話：血圧の薬は「水道管の弁」</span>
  </div>
  <div class="space-y-3 text-gray-700">
    <p>血圧が高い状態は、水道管の水圧が上がりすぎているイメージです。</p>
    <ul class="list-disc list-inside space-y-1 ml-2">
      <li><strong>血管 = 水道管</strong>：ここに高い圧力がかかると傷みやすい</li>
      <li><strong>降圧薬 = 圧力を調整する弁</strong>：水圧を適切なレベルに保つ</li>
      <li><strong>毎日飲む = 弁を常に動かす</strong>：薬をやめると圧力が戻る</li>
    </ul>
    <p>だから<strong>症状がなくても毎日飲み続けること</strong>が大切なんです。</p>
  </div>
</div>
```

### パターン2: 副作用を「ありえる副作用」として正直に伝える

```html
<div class="bg-gradient-to-r from-amber-50 to-orange-50 p-6 rounded-xl border border-amber-200 my-6">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="triangle-alert" class="w-6 h-6 text-amber-600"></i>
    <span class="font-bold text-amber-800">副作用について</span>
  </div>
  <div class="space-y-3 text-gray-700">
    <p>「副作用」と聞くと怖いイメージがありますが、<strong>多くの人には起きません</strong>。</p>
    <p>車の排気ガスみたいなもので、本来の目的（移動）とは別の「意図しない影響」です。</p>
    <p>万が一、以下のような体験をした場合は遠慮なくご相談ください。</p>
  </div>
</div>
```

### パターン3: 薬の切り替えを「同じ目的で道具が変わる」と伝える

```html
<div class="bg-gradient-to-r from-sky-50 to-blue-50 p-6 rounded-xl border border-sky-200 my-6">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="git-compare" class="w-6 h-6 text-sky-600"></i>
    <span class="font-bold text-sky-800">薬が変わっても目的は同じです</span>
  </div>
  <div class="space-y-3 text-gray-700">
    <p>「薬が変わって大丈夫かな」と不安に思われる方もいます。</p>
    <p>例えば、同じ場所に行くのに「電車」から「バス」に変わるようなもの。<br>
       <strong>目的地（血圧を下げる・症状を抑える）は同じ</strong>です。</p>
    <p>変更の理由（副作用が少ない・費用が抑えられるなど）も一緒にお伝えするとより安心してもらえます。</p>
  </div>
</div>
```

---

## 詳細セクションの書き方

```html
<div class="section-card" id="side-effects">
  <!-- セクションヘッダー -->
  <div class="flex items-center gap-3 mb-6">
    <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
      <i data-lucide="triangle-alert" class="w-6 h-6 text-orange-500"></i>
    </div>
    <div>
      <h2 class="text-2xl font-bold text-gray-800">気をつけたい副作用</h2>
      <p class="text-gray-500">こんな症状が出たらご連絡ください</p>
    </div>
  </div>

  <!-- キャラクター対話 -->
  <div class="flex items-start gap-4 mb-6">
    <div class="w-16 h-16 rounded-full bg-amber-400 flex items-center justify-center flex-shrink-0">
      <span class="text-white font-bold text-xl">R</span>
    </div>
    <div class="char-bubble rookie-bubble flex-1">
      <p class="text-base">
        <span class="font-bold text-amber-700">ルーキーさん:</span><br>
        副作用をどこまで説明すればいいか、いつも迷ってしまって…
        全部言ったら怖がらせてしまうし
      </p>
    </div>
  </div>

  <div class="flex items-start gap-4 mb-6">
    <div class="w-16 h-16 rounded-full bg-teal-600 flex items-center justify-center flex-shrink-0">
      <span class="text-white font-bold text-xl">S</span>
    </div>
    <div class="char-bubble senior-bubble flex-1">
      <p class="text-base">
        <span class="font-bold text-teal-700">センパイさん:</span><br>
        コツは「症状の名前」より「こんな体験をしたら教えてください」という伝え方です。
        患者さんが行動できる言葉にするんです。
      </p>
    </div>
  </div>

  <!-- 本文 -->
  <div class="space-y-4">
    <h3 class="text-xl font-bold text-gray-700 flex items-center gap-2">
      <i data-lucide="list" class="w-5 h-5 text-orange-500"></i>
      よくある副作用
    </h3>
    <ul class="space-y-2">
      <li class="flex items-start gap-2">
        <i data-lucide="check" class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5"></i>
        <span><strong>〇〇</strong>（副作用名）：〜のような感覚が出ることがあります</span>
      </li>
    </ul>
  </div>

  <!-- 受診タイミング -->
  <div class="visit-box mt-6">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="hospital" class="w-6 h-6 text-red-600"></i>
      <span class="font-bold text-red-700 text-lg">こんな症状が出たらすぐに受診</span>
    </div>
    <ul class="space-y-2">
      <li class="flex items-start gap-2">
        <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"></i>
        <span>〇〇の症状がひどくなる、または続く</span>
      </li>
    </ul>
    <p class="mt-3 text-sm text-red-600 font-medium">
      ※ 心配なことはいつでも薬局にご相談ください
    </p>
  </div>
</div>
```

---

## 品質チェックリスト

作成後、以下を確認：

- [ ] 全ての医療用語に用語解説ボックスがある
- [ ] 「患者様に必ず伝えること3つ」がある
- [ ] 副作用に「受診タイミング」が明記されている
- [ ] 薬の切り替えがある場合は比較表がある
- [ ] たとえ話が3つ以上ある
- [ ] 導入・中間・まとめにキャラクター対話がある
- [ ] Lucide iconのみ使用（絵文字なし）
- [ ] 医療・薬局ブランドカラーが適用されている
- [ ] スマホで読みやすい（レスポンシブ）
- [ ] 目次がフローティング表示される（デスクトップ）
