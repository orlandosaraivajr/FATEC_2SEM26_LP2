"""
Script de testes para a API FastAPI - Fatec CRUD
Execute com: python test_api.py
Certifique-se que o servidor está rodando: uvicorn main:app --reload
"""

import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

# ──────────────────────────────────────────────
# Helpers de exibição
# ──────────────────────────────────────────────

def separador(titulo: str):
    print("\n" + "=" * 55)
    print(f"  {titulo}")
    print("=" * 55)

def exibir_resposta(resp: requests.Response):
    cor_ok    = "\033[92m"  # verde
    cor_err   = "\033[91m"  # vermelho
    cor_reset = "\033[0m"

    status = resp.status_code
    cor = cor_ok if status < 400 else cor_err
    print(f"  Status : {cor}{status}{cor_reset}")
    try:
        corpo = resp.json()
        print(f"  Resposta: {json.dumps(corpo, ensure_ascii=False, indent=4)}")
    except Exception:
        print(f"  Resposta: {resp.text}")

def ok_ou_falhou(resp: requests.Response, esperado: int = 200) -> bool:
    passou = resp.status_code == esperado
    icone = "✔" if passou else "✘"
    print(f"  [{icone}] Esperado {esperado} — obtido {resp.status_code}")
    return passou

# ──────────────────────────────────────────────
# Dados de teste
# ──────────────────────────────────────────────

USUARIO_TESTE = {
    "nome":            "Maria Oliveira",
    "cpf":             "987.654.321-00",
    "email":           "maria.oliveira@teste.com",
    "telefone":        "(19) 99999-0001",
    "data_nascimento": "1995-03-22",
}

ID_CRIADO = None  # preenchido após o POST

# ──────────────────────────────────────────────
# Testes
# ──────────────────────────────────────────────

def teste_listar_usuarios():
    separador("GET /usuarios — listar todos")
    resp = requests.get(f"{BASE_URL}/usuarios")
    exibir_resposta(resp)
    ok_ou_falhou(resp, 200)
    if resp.ok:
        dados = resp.json()
        print(f"  Total de registros retornados: {len(dados)}")
        # Verifica anonimização LGPD no primeiro registro
        if dados:
            primeiro = dados[0]
            nome = primeiro.get("nome", "")
            cpf  = primeiro.get("cpf",  "")
            email = primeiro.get("email", "")
            lgpd_ok = (
                "*" in nome  and
                "***" in cpf and
                "*" in email
            )
            icone = "✔" if lgpd_ok else "✘"
            print(f"  [{icone}] Anonimização LGPD aplicada")


def teste_criar_usuario() -> int | None:
    separador("POST /usuarios — criar usuário")
    resp = requests.post(f"{BASE_URL}/usuarios", params=USUARIO_TESTE)
    exibir_resposta(resp)
    ok_ou_falhou(resp, 200)
    if resp.ok:
        novo_id = resp.json().get("id")
        print(f"  [✔] Usuário criado com ID = {novo_id}")
        return novo_id
    return None


def teste_buscar_usuario(user_id: int):
    separador(f"GET /usuarios/{user_id} — buscar por ID")
    resp = requests.get(f"{BASE_URL}/usuarios/{user_id}")
    exibir_resposta(resp)
    ok_ou_falhou(resp, 200)
    if resp.ok:
        dados = resp.json()
        # Verifica LGPD no registro individual
        lgpd_ok = (
            "*" in dados.get("nome",  "") and
            "*" in dados.get("cpf",   "") and
            "*" in dados.get("email", "")
        )
        icone = "✔" if lgpd_ok else "✘"
        print(f"  [{icone}] Anonimização LGPD no registro individual")


def teste_buscar_usuario_inexistente():
    separador("GET /usuarios/999999 — ID inexistente (esperado 404)")
    resp = requests.get(f"{BASE_URL}/usuarios/999999")
    exibir_resposta(resp)
    ok_ou_falhou(resp, 404)


def teste_atualizar_usuario(user_id: int):
    separador(f"PUT /usuarios/{user_id} — atualizar nome e telefone")
    params = {
        "nome":     "Maria S. Oliveira",
        "telefone": "(19) 98888-0002",
    }
    resp = requests.put(f"{BASE_URL}/usuarios/{user_id}", params=params)
    exibir_resposta(resp)
    ok_ou_falhou(resp, 200)

    # Confirma que os dados foram atualizados de fato
    verificacao = requests.get(f"{BASE_URL}/usuarios/{user_id}")
    if verificacao.ok:
        dados = verificacao.json()
        telefone = dados.get("telefone", "")
        # O telefone é anonimizado — verifica apenas os últimos 4 dígitos
        atualizou = "0002" in telefone
        icone = "✔" if atualizou else "✘"
        print(f"  [{icone}] Dados persistidos corretamente após o PUT")


def teste_atualizar_usuario_inexistente():
    separador("PUT /usuarios/999999 — ID inexistente (esperado 404)")
    resp = requests.put(
        f"{BASE_URL}/usuarios/999999",
        params={"nome": "Fantasma"},
    )
    exibir_resposta(resp)
    ok_ou_falhou(resp, 404)


def teste_deletar_usuario(user_id: int):
    separador(f"DELETE /usuarios/{user_id} — remover usuário")
    resp = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
    exibir_resposta(resp)
    ok_ou_falhou(resp, 200)

    # Confirma que o registro não existe mais
    verificacao = requests.get(f"{BASE_URL}/usuarios/{user_id}")
    icone = "✔" if verificacao.status_code == 404 else "✘"
    print(f"  [{icone}] Registro removido — GET retorna 404 após DELETE")


def teste_deletar_usuario_inexistente():
    separador("DELETE /usuarios/999999 — ID inexistente (esperado 404)")
    resp = requests.delete(f"{BASE_URL}/usuarios/999999")
    exibir_resposta(resp)
    ok_ou_falhou(resp, 404)


def teste_criar_email_duplicado(email_existente: str):
    separador("POST /usuarios — e-mail duplicado (esperado 4xx ou 5xx)")
    dados = USUARIO_TESTE.copy()
    dados["email"] = email_existente   # mesmo e-mail já inserido
    dados["cpf"]   = "111.222.333-44"  # CPF diferente
    resp = requests.post(f"{BASE_URL}/usuarios", params=dados)
    exibir_resposta(resp)
    passou = resp.status_code >= 400
    icone = "✔" if passou else "✘"
    print(f"  [{icone}] API recusou e-mail duplicado ({resp.status_code})")

# ──────────────────────────────────────────────
# Suíte principal
# ──────────────────────────────────────────────

def main():
    print("\n" + "█" * 55)
    print("  SUITE DE TESTES — FastAPI Usuários")
    print(f"  Base URL: {BASE_URL}")
    print("█" * 55)

    # Verifica se o servidor está acessível
    try:
        requests.get(BASE_URL, timeout=3)
    except requests.ConnectionError:
        print(f"\n  ✘ Não foi possível conectar em {BASE_URL}")
        print("    Suba o servidor com:  uvicorn main:app --reload\n")
        return

    # 1. Leitura geral antes de qualquer inserção
    teste_listar_usuarios()

    # 2. Criação
    user_id = teste_criar_usuario()

    if user_id:
        # 3. Leitura individual
        teste_buscar_usuario(user_id)

        # 4. E-mail duplicado
        teste_criar_email_duplicado(USUARIO_TESTE["email"])

        # 5. Atualização
        teste_atualizar_usuario(user_id)

        # 6. Remoção
        teste_deletar_usuario(user_id)
    else:
        print("\n  [!] POST falhou — pulando testes dependentes do ID.")

    # 7. Casos de erro (IDs inexistentes)
    teste_buscar_usuario_inexistente()
    teste_atualizar_usuario_inexistente()
    teste_deletar_usuario_inexistente()

    print("\n" + "=" * 55)
    print("  Testes concluídos.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
