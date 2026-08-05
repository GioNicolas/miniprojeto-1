"""Modo batch: lê consultas.json, responde em ordem, grava respostas.json.

Uso: python main.py consultas.json respostas.json
"""
import json
import sys

from catalogo import Catalogo

def main():
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2]

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, "r", encoding="utf-8") as arquivo:
        consultas = json.load(arquivo)["consultas"]

    respostas = {}
    for consulta in consultas:
        metodo = getattr(catalogo, consulta["tipo"])
        resultado = metodo(**consulta["parametros"])
        respostas[str(consulta["id"])] = resultado

    with open(caminho_respostas, "w", encoding="utf-8") as arquivo:
        json.dump(respostas, arquivo, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
