# Neural generation of Russian news headlines using abstractive text summarization approach  <img src="https://assets.website-files.com/5e77aebfc78e1c7a72b9201b/5ecfce32a80336a92e83b544_icon_subscribe_plane_animation_starts-with-quartplane.gif" width="70px">

The code is taken from: https://github.com/leshanbog/PreSumm

We also present the new Bumaga dataset and reach BLEU score 48.51, ROUGE-1 score 44.1 and ROUGE-mean 38.3 on it. 

### Description of the Bumaga dataset

The dataset contains 38 499 Russian language news texts with headlines published on the [Bumaga's](https://paperpaper.ru/) website from 28.06.2013 to 31.03.2021.

The dataset is available in CSV and JSON formats. The dataset consists of 4 fields: `URL` of the news article, `date` of the news article, `text` which is a body of the news article and `title` which is a news headline. Dataset splits are also proposed.

   :small_orange_diamond: Bumaga original dataset in [JSON](https://www.dropbox.com/s/mq3bemyc3jdpr2z/bumaga.json?dl=0)

   :small_orange_diamond: Bumaga original dataset in [CSV](https://www.dropbox.com/s/ib9xv1pt2xrct61/bumaga.csv?dl=0)

   :small_orange_diamond: Bumaga [train/val/test](https://www.dropbox.com/s/6oxdb52l029zt5l/bumaga_shuf.zip?dl=0) 


### Trained on the RIA model

BertSumAbs checkpoint: https://yadi.sk/d/2jcjmdEXp0EX-Q


### Data Preprocessing

The authors of [Advances of Transformer-Based Models for News Headline Generation](https://arxiv.org/abs/2007.05044) use [RuBERT](http://docs.deeppavlov.ai/en/master/features/models/bert.html) from DeepPavlov:  as a pretrained BERT.

```
python3 /PreSumm/src/convert_to_presumm.py --config-path /PreSumm/src/readers/configs/ria_reader_config.json --file-path ~/dataset/bumaga_shuf_train.json --save-path ~/dataset/bumaga_shuf_bert/train.bert.pt --bert-path ~/models/rubert_cased_L-12_H-768_A-12_pt

python3 /PreSumm/src/convert_to_presumm.py --config-path /PreSumm/src/readers/configs/ria_reader_config.json --file-path ~/dataset/bumaga_shuf_val.json --save-path ~/dataset/bumaga_shuf_bert/test.bert.pt --bert-path ~/models/rubert_cased_L-12_H-768_A-12_pt

```

### Model Training

```
python3 /PreSumm/src/train.py -task abs -mode train -bert_data_path ~/dataset/bumaga_shuf_bert/ -train_from  ~/models/rubert_cased_L-12_H-768_A-12_pt/model_step_40000.pt -visible_gpus 0 -dec_dropout 0.2 -model_path ~/models/rubert_cased_L-12_H-768_A-12_pt -sep_optim true -lr_bert 0.002 -lr_dec 0.2 -save_checkpoint_steps 600 -batch_size 128 -train_steps 47000 -report_every 100 -accum_count 95 -use_bert_emb true -use_interval true -warmup_steps_bert 20000 -warmup_steps_dec 10000 -max_pos 256 -log_file /PreSumm/logs/abs_bert_bum_shuf

```

### Predicting

```
python3 /PreSumm/src/train.py -task abs -mode validate -batch_size 128 -visible_gpus 0 -test_batch_size 128 -bert_data_path ~/dataset/bumaga_shuf_bert/ -log_file /PreSumm/logs/val_abs_bert_bum_shuf -model_path ~/models/rubert_cased_L-12_H-768_A-12_pt/ -sep_optim true -use_interval true -max_pos 256 -max_length 18 -min_length 4 -result_path ../Bumaga_shuf

```

### Evaluating

```
python3 /PreSumm/src/eval_results.py /Bumaga_shuf.44700.gold /Bumaga_shuf.44700.candidate

```
