from slack_bolt.async_app import AsyncApp
import sqlite3

dbname = 'database.db'
table_name = "messages"
message_content_column_name = "content"
message_pk_column_name = "id"

def bootstrap_db():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS  {table_name}({message_pk_column_name} INTEGER PRIMARY KEY AUTOINCREMENT,{message_content_column_name} TEXT)")
    conn.commit()
    conn.close()


app = AsyncApp()

@app.command("/notify")
async def command(ack, body, respond):
    await ack() #この関数を,コマンドが入力されてから３秒以内に返さないとoperation_timeoutになる
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    print(body)
    if 'text' not in body:
        await respond("Error!")
        conn.close
        return
  
    message_content = body['text']
    command, *args = message_content.split(maxsplit=1)
    if command == "add": # /notify add {message}
        if len(args) == 0:
            await respond("引数が不足しています.")
        message = args[0]
        c.execute(f"INSERT INTO {table_name} ({message_content_column_name}) VALUES (?)", (message,))
        conn.commit()
        await respond("メッセージを追加しました")
    elif command == "remove": # /notify remove {message_id}
        if len(args) == 0:
            await respond("引数が不足しています.")
        message_id = args[0]
        c.execute(f"DELETE FROM {table_name} WHERE {message_pk_column_name}=?", (message_id,))
        conn.commit()
        await respond("メッセージを削除しました")
    elif command == "edit": # /notify edit {message_id} {content}
        if len(args) == 0:
            await respond("引数が不足しています.")
        # args: ["1　aaaa"], ["1"], ["aaaa"], ["1 aaaa bbbb"]
        sub_args = args[0].split(maxsplit=1)
        if len(sub_args) == 1:
            await respond("引数が不足しています.")
        # sub_args は length が2なので、そのまま unpack 出来る
        message_id, content = sub_args
        c.execute(f"UPDATE {table_name} SET {message_content_column_name}=? WHERE {message_pk_column_name}=?", (content, message_id))
        conn.commit()
        await respond("メッセージを更新しました")
    elif command == "list": # /notify list 
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        for row in rows:
            await respond(f"ID: {row[message_pk_column_name]}, Message: {row[message_content_column_name]}")
    elif command == "help": # /notify help
        await respond("add:メッセージをリストに追加します, remove:メッセージをリストから削除します, edit, IDで指定されたメッセージを書き換えます, list:リストに登録されたメッセージの一覧を出力します")
    else:
        await respond("使えるのはadd, remove, edit, list, helpです。")
    conn.close()

if __name__ == "__main__":
    app.start(3000)
    bootstrap_db()
