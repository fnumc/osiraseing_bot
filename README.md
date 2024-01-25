# osiraseing_bot
Bolt for pythonを使用したSlack bot  
オンラインIDEの[Glitch](https://glitch.com/dashboard)の上で動きます.  

# 導入手順
   [GlitchとBolt for Pythonを使ってSlackアプリを爆速開発 - Zenn](https://zenn.dev/cazziwork/articles/50ac3df78096d3a9a44c)も参考に


# なにができる
| Command                     | Action                               | 
| --------------------------- | ------------------------------------ | 
| `/notify add {MESSAGE}`       | メッセージをリストに追加する         | 
| `/notify remove {ID}`         | IDで指定されたメッセージを削除       | 
| `/notify edit {ID} {MESSAGE}` | IDで指定されたメッセージを書き換える | 
| `/notify list`               | メッセージのID付きリストを出力する   | 
| `/notify help`               | 使うことができるコマンドを表示する   | 

# やること
- ソケットモードに書き換える
- Dockerfile, composeファイルを書く
  
# See also
- https://scrapbox.io/greenland/お知らせし続けるbot
 
