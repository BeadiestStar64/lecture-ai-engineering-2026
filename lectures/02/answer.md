# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
- 自分で学習を実行したか（`executed_training_myself`）：はい / いいえ（実行できた範囲：　）
- 学習前：`format_rate` =　 / `content_rate` =　
- 学習後：`format_rate` =　 / `content_rate` =　
- 退行した質問：
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
- 学習で変わったこと・変わらなかったこと：

## 宿題

- 取り組んだレベル：基礎

- 変えた設定やデータ： 学習率 `lr` を $0.0002$ から $0.001$ に変更
- 結果（比較表や数字）：
  | 各項目 | 学習率 2e-4 | 学習率 1e-3 |
  | :---: | :---: | :---: |
  | ベースモデル | Qwen/Qwen3.5-0.8B | Qwen/Qwen3.5-0.8B |
  | format_rate | 1.0 | 1.0 |
  | content_rate | 0.9047619047619048 | 0.9047619047619048 |
  | both_rate | 0.9047619047619048 | 0.9047619047619048 |
  | seconds | 31.1 | 32.0 |

- ファインチューニングが向く場面・向かない場面についての考察：
  本講義や(GoogleのGemmaのファインチューニングのドキュメント)[https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora] などから、モデルに所定のフォーマットに従った出力をさせるにはファインチューニングが大いに適していると言える。その理由として、モデルに決められたフォーマットの「振る舞い」を学ばせるためであるから。
  逆に「オフィスアワーが何時から」といった知識は、ファインチューニングで焼き付けるのではなくRAGを使う方が最適だと言える。

- 使ったモデル・設定（`result.json` の `config` から）：
  初期設定での結果

```json
{
  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  }
}
```

```json
{
  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.001,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  }
}
```

- 自分で学習を実行したか（`executed_training_myself`）：はい
- 学習前：`format_rate` =　$0.09523809523809523(学習率 $0.0002, 0.001共$)$ / `content_rate` =　$0.0(学習率 $0.0002, 0.001共$)$
- 学習後：`format_rate` =　$1.0(学習率 $0.0002, 0.001共$)$ / `content_rate` =　$0.9047619047619048(学習率 $0.0002, 0.001共$)$
- 退行した質問： 無し
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
  「PDF 以外でも出せますか」という質問に対しては、本来は `needs_review` が `False` であるべきところが `True` になっていた。
