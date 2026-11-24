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
            tempo_prep INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            veiculo TEXT NOT NULL,
            telefone REAL NOT NULL,
            status REAL NOT NULL,
            entregas INTEGER DEFAULT 0,
            avaliacao REAL DEFAULT 5.0
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