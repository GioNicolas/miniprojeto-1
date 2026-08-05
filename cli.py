"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""
import sys
from collections import deque

from catalogo import Catalogo

MENU = """
TrilhaSonora
============
1. Listar todos os usuários
2. Ver playlist completa de um usuário
3. Conteúdo na posição N da playlist
4. Interseção de playlists (N usuários)
5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)
6. Conteúdos de um gênero
7. Enfileirar conteúdo na fila de reprodução
8. Tocar próximo da fila
9. Ver fila atual
10. Ver histórico
0. Sair
"""

def pedir_usuario_id(catalogo, mensagem):
    nome = input(mensagem).strip()
    usuario_id = catalogo.buscar_usuario_por_nome(nome)
    if usuario_id is None:
        print(f"Usuário '{nome}' não encontrado.")
    return usuario_id

def opcao_listar_usuarios(catalogo):
    for nome in catalogo.listar_usuarios():
        print(nome)
    return "Listou os usuários"

def opcao_ver_playlist(catalogo):
    usuario_id = pedir_usuario_id(catalogo, "Nome do usuário: ")
    if usuario_id is None:
        return None

    playlist = catalogo.playlist_de(usuario_id)
    if not playlist:
        print("Playlist vazia.")
    else:
        for conteudo_id in playlist:
            print(catalogo.descricao_de(conteudo_id))
    return f"Viu a playlist de {usuario_id}"

def opcao_conteudo_na_posicao(catalogo):
    usuario_id = pedir_usuario_id(catalogo, "Nome do usuário: ")
    if usuario_id is None:
        return None

    playlist = catalogo.playlist_de(usuario_id)
    print(f"Playlist tem {len(playlist)} itens (posições 1 a {len(playlist)}).")
    posicao_digitada = input("Qual posição? > ").strip()
    if not posicao_digitada.isdigit():
        print("Posição inválida.")
        return None

    conteudo_id = catalogo.conteudo_na_posicao(usuario_id, int(posicao_digitada) - 1)
    if conteudo_id is None:
        print("Posição fora do intervalo.")
        return None

    print(catalogo.descricao_de(conteudo_id))
    return f"Posição {posicao_digitada} da playlist de {usuario_id}"

def opcao_intersecao_playlists(catalogo):
    quantidade_digitada = input("Quantos usuários? > ").strip()
    if not quantidade_digitada.isdigit() or int(quantidade_digitada) < 1:
        print("Quantidade inválida.")
        return None

    usuario_ids = []
    for numero in range(1, int(quantidade_digitada) + 1):
        usuario_id = pedir_usuario_id(catalogo, f"Nome do usuário {numero}: ")
        if usuario_id is None:
            return None
        usuario_ids.append(usuario_id)

    intersecao = catalogo.intersecao_playlists(usuario_ids)
    if not intersecao:
        print("Nenhum conteúdo em comum.")
    else:
        for conteudo_id in intersecao:
            print(catalogo.descricao_de(conteudo_id))
    return f"Interseção de {len(usuario_ids)} usuários"

def opcao_dados_conteudo(catalogo):
    conteudo_id = input("Id do conteúdo: ").strip()
    descricao = catalogo.descricao_de(conteudo_id)
    if descricao is None:
        print(f"Conteúdo '{conteudo_id}' não encontrado.")
        return None

    print(descricao)
    print(f"Rating: {catalogo.rating_de(conteudo_id)}")
    print(f"Duração total (s): {catalogo.duracao_total_de(conteudo_id)}")
    print(f"Gêneros: {', '.join(catalogo.generos_de(conteudo_id))}")
    print(f"Plataformas: {', '.join(catalogo.plataformas_de(conteudo_id))}")
    print(f"Adicionado em: {catalogo.data_adicionado_de(conteudo_id)}")
    if descricao.endswith("(música)"):
        print(f"Execuções: {catalogo.execucoes_de(conteudo_id)}")
    return f"Dados de {conteudo_id}"

def opcao_conteudos_do_genero(catalogo):
    genero = input("Gênero: ").strip()
    ids_do_genero = catalogo.conteudos_do_genero(genero)
    if not ids_do_genero:
        print(f"Nenhum conteúdo no gênero '{genero}'.")
    else:
        for conteudo_id in ids_do_genero:
            print(catalogo.descricao_de(conteudo_id))
    return f"Conteúdos do gênero {genero}"

def opcao_enfileirar(catalogo):
    conteudo_id = input("Id do conteúdo: ").strip()
    if catalogo.enfileirar(conteudo_id):
        print(f"'{conteudo_id}' enfileirado.")
    else:
        print(f"Conteúdo '{conteudo_id}' não encontrado, não foi enfileirado.")
    return f"Enfileirou {conteudo_id}"

def opcao_proximo(catalogo):
    conteudo_id = catalogo.proximo()
    if conteudo_id is None:
        print("Fila vazia.")
    else:
        print(catalogo.descricao_de(conteudo_id))
    return "Tocou o próximo da fila"

def opcao_fila_atual(catalogo):
    fila = catalogo.fila_atual()
    if not fila:
        print("Fila vazia.")
    else:
        for posicao, conteudo_id in enumerate(fila, start=1):
            print(f"{posicao}. {catalogo.descricao_de(conteudo_id)}")
    return "Viu a fila atual"

def opcao_ver_historico(historico):
    if not historico:
        print("Nenhuma consulta ainda.")
        return
    for entrada in historico:
        print(entrada)

OPCOES = {
    "1": opcao_listar_usuarios,
    "2": opcao_ver_playlist,
    "3": opcao_conteudo_na_posicao,
    "4": opcao_intersecao_playlists,
    "5": opcao_dados_conteudo,
    "6": opcao_conteudos_do_genero,
    "7": opcao_enfileirar,
    "8": opcao_proximo,
    "9": opcao_fila_atual,
}

def main():
    if len(sys.argv) < 2:
        print("Uso: python cli.py catalogo_final.json")
        return

    catalogo = Catalogo(sys.argv[1])
    historico = deque(maxlen=10)

    while True:
        print(MENU)
        escolha = input("> ").strip()

        if escolha == "0":
            break
        elif escolha == "10":
            opcao_ver_historico(historico)
        else:
            acao = OPCOES.get(escolha)
            if acao is None:
                print("Opção inválida.")
            else:
                entrada = acao(catalogo)
                if entrada is not None:
                    historico.append(entrada)
        print()

if __name__ == "__main__":
    main()
