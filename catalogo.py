"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""
import json

class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self._conteudos = {}

        for item in dados["conteudos"]:
            self._conteudos[item["id"]] = item    

        self._usuarios_por_nome = {}
        for usuario in dados["usuarios"]:
            self._usuarios_por_nome[usuario["nome"].lower()] = usuario["id"]    

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]: ...
    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        nome_minusculo = nome.lower()
        id_do_nome = self._usuarios_por_nome.get(nome_minusculo)

        return id_do_nome
        







    def playlist_de(self, usuario_id: str) -> list[str] | None: ...
    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: ...
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: ...

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool: ...
    def proximo(self) -> str | None: ...
    def fila_atual(self) -> list[str]: ...