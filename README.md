# README

## bookq2pdf
BookQからスライドをPDF形式で頂戴するプログラムです．

## 実行環境
Python3で動作します．

## 事前準備
必要なライブラリは`requirements.txt`に記述されています．以下のコマンドで一括インストールできます．
```bash
pip install -r requirements.txt
```

また，実行前に以下のような`secrets.json`ファイルを作成しておく必要があります．"id"にはSSO-KIDを，"passwd"にはパスワードを記述してください．
```json
{
    "id":"0000000000",
    "passwd":"XXXXXXXXXXX"
}
```

## 使い方
`main.ipynb`にサンプルコードを記述しています．メソッドの詳細については以下を参照してください．

**Bookq.login()**
```python
login(
    secrets_file='secrets.json'
)
```
BookQへログインを行うメソッドです．
|Args||
|--|--|
|secrets_file|IDとパスワードを保存しているJSONファイルへのパス|

**Bookq.get_pdf()**
```python
get_pdf(
    book_url, page_num, file_name='output.pdf', sleep_time=1
)
```
スライドを取得するメソッドです．
|Args||
|--|--|
|book_url|スライドのURL|
|page_num|取得するスライドの枚数を指定|
|file_name|出力するPDFの名前|
|sleep_time|スライド取得毎に入るスリープの間隔（秒）|

## 注意点
スライドは著作物です．取得したスライドの取扱いには十分注意してください．

## ライセンス
"bookq2pdf" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).