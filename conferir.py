"""Confere respostas.json contra gabarito_publico.json.

Uso: python conferir.py [gabarito_publico.json] [respostas.json]
"""
import json
import sys

def valores_batem(esperado, obtido):
    if isinstance(esperado, float) or isinstance(obtido, float):
        try:
            return abs(float(esperado) - float(obtido)) < 1e-6
        except (TypeError, ValueError):
            return False
    return esperado == obtido

def conferir(caminho_gabarito, caminho_respostas):
    with open(caminho_gabarito, "r", encoding="utf-8") as arquivo:
        gabarito = json.load(arquivo)
    with open(caminho_respostas, "r", encoding="utf-8") as arquivo:
        respostas = json.load(arquivo)

    acertos = []
    erros = []
    ausentes = []
    for id_consulta, esperado in gabarito.items():
        if id_consulta not in respostas:
            ausentes.append(id_consulta)
            continue

        obtido = respostas[id_consulta]
        if valores_batem(esperado, obtido):
            acertos.append(id_consulta)
        else:
            erros.append((id_consulta, esperado, obtido))

    print(f"{len(acertos)}/{len(gabarito)} bateram")

    if ausentes:
        print(f"\n{len(ausentes)} ausentes em respostas.json:")
        for id_consulta in ausentes:
            print(f"  {id_consulta}")

    if erros:
        print(f"\n{len(erros)} erradas:")
        for id_consulta, esperado, obtido in erros:
            print(f"  {id_consulta}: esperado {esperado!r}, veio {obtido!r}")

def main():
    caminho_gabarito = sys.argv[1] if len(sys.argv) > 1 else "gabarito_publico.json"
    caminho_respostas = sys.argv[2] if len(sys.argv) > 2 else "respostas.json"
    conferir(caminho_gabarito, caminho_respostas)

if __name__ == "__main__":
    main()
