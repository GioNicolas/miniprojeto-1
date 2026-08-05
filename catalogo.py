"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""
import json

class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self._conteudos = {} #ID: JSON completo,

        for item in dados["conteudos"]:
            self._conteudos[item["id"]] = item

        self._usuarios_por_nome = {} #nome minusculo: ID,
        self._nomes_usuarios = [] #Nome normal: ,
        self._playlist_por_usuario = {} #ID: Playlist
        for usuario in dados["usuarios"]:
            self._usuarios_por_nome[usuario["nome"].lower()] = usuario["id"]
            self._nomes_usuarios.append(usuario["nome"])
            self._playlist_por_usuario[usuario["id"]] = usuario["playlist"]

        self._ids_por_genero = {} #genero: lista de IDs
        for conteudo_id, conteudo in self._conteudos.items():
            for genero in self._achatar_generos(conteudo["generos"]):
                self._ids_por_genero.setdefault(genero, []).append(conteudo_id)

    def _achatar_generos(self, generos) -> list[str]:
        if isinstance(generos, str):
            return [generos]

        achatados = []
        for item in generos:
            achatados.extend(self._achatar_generos(item))
        return achatados

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
        usuarios = sorted(self._nomes_usuarios)

        return usuarios
    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        nome_minusculo = nome.lower()
        id_do_nome = self._usuarios_por_nome.get(nome_minusculo)

        return id_do_nome

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        playlist = self._playlist_por_usuario.get(usuario_id)

        return playlist
    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        playlist = self.playlist_de(usuario_id)
        if playlist is None:
            return None
        if 0 <= posicao < len(playlist):
            return playlist[posicao]
        return None
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        if not usuario_ids:
            return []

        playlists = []
        for usuario_id in usuario_ids:
            playlist = self._playlist_por_usuario.get(usuario_id)
            if playlist is None:
                return []
            playlists.append(set(playlist))

        intersecao = playlists[0]
        for playlist in playlists[1:]:
            intersecao &= playlist

        return sorted(intersecao)

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None

        generos = self._achatar_generos(conteudo["generos"])

        return sorted(generos)
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]:
        ids_do_genero = self._ids_por_genero.get(genero, [])

        return sorted(ids_do_genero)

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool: ...
    def proximo(self) -> str | None: ...
    def fila_atual(self) -> list[str]: ...
