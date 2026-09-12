import sqlite3


conexao = sqlite3.connect("rbmk.db")
cursor = conexao.cursor()

cursor.execute("""
    SELECT * FROM partidas
    ORDER BY id DESC
""")

partidas = cursor.fetchall()

for partida in partidas:
    print(partida)

conexao.close()