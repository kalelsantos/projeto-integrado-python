import sqlite3

def conectar():
    return sqlite3.connect("maonamassa.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            status TEXT NOT NULL,
            tempo_prep INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            veiculo TEXT NOT NULL,
            telefone TEXT NOT NULL,
            status TEXT NOT NULL,
            entregas INTEGER DEFAULT 0,
            avaliacao REAL DEFAULT 5.0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            motoboy TEXT NOT NULL,
            endereco TEXT NOT NULL,
            valor_entrega REAL NOT NULL,
            tempo_estimado INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            descricao TEXT
        )
    """)

    conn.commit()
    conn.close()

def inserir_pedido (cliente, forma_pagamento, valor_total, status, tempo_prep):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (cliente, forma_pagamento, valor_total, status, tempo_prep)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente, forma_pagamento, valor_total, status, tempo_prep))

    cursor.execute("""
        INSERT INTO financeiro (tipo, valor, descricao)
        VALUES ('Valor dos Pedidos', ?, ?)
    """, (valor_total, f"Pedido de {cliente}"))

    conn.commit()
    conn.close()

def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente, valor_total, status, forma_pagamento, tempo_prep FROM pedidos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def inserir_entregador(nome, veiculo, telefone, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entregadores (nome, veiculo, telefone, status)
        VALUES (?, ?, ?, ?)
    """, (nome, veiculo, telefone, status))

    conn.commit()
    conn.close()

def listar_entregadores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, veiculo, telefone, status, entregas, avaliacao FROM entregadores ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def inserir_entrega(pedido_id, motoboy, endereco, valor_entrega, tempo_estimado, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entregas (pedido_id, motoboy, endereco, valor_entrega, tempo_estimado, status)
        VALUES (?, ?, ?, ?, ?, "Aguardando Retirada")

    """, (pedido_id, motoboy, endereco, valor_entrega, tempo_estimado, status))

    cursor.execute("""
        INSERT INTO financeiro (tipo, valor, descricao)
        VALUES ('Taxa de Entrega', ?, ?)""")


def listar_entregas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pedido_id, motoboy, endereco, valor_entrega, tempo_estimado, status FROM entregas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados
