from sqlalchemy import create_engine, MetaData, Table, select, delete, text

# 1️⃣ Conexão com o banco PostgreSQL
engine = create_engine("postgresql+psycopg2://orlando:123mudar@172.24.53.232:5432/clientes")

metadata = MetaData()
metadata.reflect(bind=engine)

# 2️⃣ Obtém a referência da tabela 'usuarios'
if 'usuarios' in metadata.tables:
    usuarios = metadata.tables['usuarios']
else:
    print("A tabela 'usuarios' não existe.")
    exit()

# 3️⃣ Remove apenas o primeiro usuário (menor ID)
with engine.connect() as conn:
    # Busca o menor ID existente
    result = conn.execute(select(usuarios.c.id).order_by(usuarios.c.id.asc()).limit(1))
    first_user = result.fetchone()
    
    if first_user:
        stmt = delete(usuarios).where(usuarios.c.id == first_user.id)
        conn.execute(stmt)
        conn.commit()
        print(f"✅ Usuário com ID {first_user.id} removido com sucesso.")
    else:
        print("Nenhum usuário encontrado para exclusão.")

# 4️⃣ Remove todos os demais registros
with engine.connect() as conn:
    stmt = delete(usuarios)
    result = conn.execute(stmt)
    conn.commit()
    print(f"🧹 Foram deletados {result.rowcount} registros restantes da tabela 'usuarios'.")

# 5️⃣ Remove a tabela completamente
with engine.connect() as conn:
    usuarios.drop(engine)
    print("🗑️  Tabela 'usuarios' removida com sucesso.")
