# TrilhaSonora: decisões de modelagem

## Por que só a classe `Catalogo`

Pensei em criar `Musica`, `Album`, `Usuario` e `Faixa`, mas nenhuma ia ter
comportamento próprio além dos campos que já vêm no JSON. A lógica de
achatar gênero, converter data e somar duração de faixa já trabalha em cima
do dado bruto, então ficou melhor como método da própria `Catalogo`, que é
quem tem os índices pra fazer isso rápido.

## Os índices do `__init__`

O `__init__` carrega o JSON uma vez e monta:

- `_conteudos`: id → conteúdo inteiro. Usei isso pra evitar varrer a lista
  toda em cada consulta.
- `_usuarios_por_nome` e `_playlist_por_usuario`: nome em minúsculo → id, e
  id → playlist. Assim `buscar_usuario_por_nome` e `playlist_de` viram
  acesso direto de dicionário.
- `_ids_por_genero`: gênero → lista de ids. Construí achatando o gênero de
  cada conteúdo uma vez só, no carregamento, pra `conteudos_do_genero` não
  precisar varrer os 20 mil conteúdos toda vez que é chamado.

Com 20 mil conteúdos e 10 mil consultas no lote, qualquer método que
varresse a lista inteira toda vez ia ficar pesado. Os índices resolvem
isso: cada consulta vira um acesso a dicionário.

## O que não dá pra indexar

`intersecao_playlists` recebe uma lista de usuários que pode ser qualquer
combinação, então não dá pra pré-computar a interseção de todo subconjunto
possível dos 33 usuários. Seriam muitas combinações. Por isso esse método
calcula na hora: transforma cada playlist num `set` e intersecta. Ainda
assim sai rápido porque buscar a playlist de cada usuário já é O(1) (por
conta do `_playlist_por_usuario`), e a interseção de sets em si só depende
do tamanho da menor playlist, não do catálogo inteiro.

## A fila de reprodução

Pesquisei e existe esse `deque` da biblioteca padrão que deixa remover
itens de uma lista nas pontas sem complexidade alta. Usei ele em
`enfileirar`, `proximo` e `fila_atual` em vez de uma `list` normal, porque
`proximo()` precisa tirar o primeiro item da fila toda vez que é chamado, e
`list.pop(0)` desloca o resto da lista inteira pra frente. Com `deque`,
isso fica rápido nas duas pontas. A fila é a única parte da `Catalogo` que
muda depois do `__init__`: começa vazia e não guarda nada de uma execução
pra outra.

## `cli.py`

Cada opção do menu é uma função pequena que só chama métodos públicos da
`Catalogo`, sem lógica de negócio no `cli.py`. Nome de usuário digitado
sempre passa por `buscar_usuario_por_nome` antes de virar id. Id de
conteúdo sempre passa por `descricao_de` antes de aparecer na tela, pra
nunca mostrar id cru pra quem tá usando o menu.
