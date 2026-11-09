:- encoding(utf8).
/*  exporta_caminhos.pl -- imprime, para cada réu e leitura, a resposta de cada pergunta da árvore A
    (usado por scripts/ver_arvore.py)
    swipl -g main -t halt prolog/exporta_caminhos.pl
    Saída (uma linha por réu x leitura, separada por TAB):
      caso  leitura  lei  primario  bons_antecedentes  nao_dedica  nao_integra_orcrim  decisao  indicadores
*/
:- ensure_loaded(arvore_a).
:- ensure_loaded(fatos_casos).
:- ensure_loaded(testes_arvore_a).   % traz também os réus inventados dos testes (t_...)

main :-
    forall(( caso(C, _, _), perfil(P), member(P, [garantista, intermediario, restritivo]) ),
      ( lei_aplicavel(C, Lei),
        findall(R, ( member(Q, [primario, bons_antecedentes, nao_dedica, nao_integra_orcrim]),
                     requisito(Q, C, P, R) ), Rs),
        decide(P, C, D, _), dedica(C, P, _, Inds),
        atomic_list_concat(Rs, '\t', RsA), term_to_atom(D, DA), term_to_atom(Inds, IA),
        format("~w\t~w\t~w\t~w\t~w\t~w~n", [C, P, Lei, RsA, DA, IA]) )).
