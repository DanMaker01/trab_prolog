:- encoding(utf8).
/*  experimentos.pl -- experimentos com a árvore A sobre os réus reais
    swipl -g main -t halt prolog/experimentos.pl
    Gera em resultados/:
      e1_decisoes.csv  caso x perfil x política de dado faltante: decisão, fração, pena, regime
      e1_ablacao.csv   a partir do perfil intermediário, troca UM parâmetro por vez e conta
                       quantas decisões mudam
*/
:- ensure_loaded(arvore_a).
:- ensure_loaded(fatos_casos).
:- dynamic dir_exp/1.
:- prolog_load_context(directory, D), retractall(dir_exp(_)), assertz(dir_exp(D)).
saida(Nome, Arq) :- dir_exp(D), atomic_list_concat([D, '/../resultados/', Nome], Arq).

real(C) :- caso(C, _, _), \+ sub_atom(C, 0, _, _, t_).

dec_atom(concede(F), concede, F) :- !.
dec_atom(D, D, '').

% ---------------- E1a: decisões e penas ----------------
e1a :-
    saida('e1_decisoes.csv', Arq), open(Arq, write, S),
    format(S, "caso,fonte,perfil,politica,decisao,fracao,meses,regime,substituicao,motivos~n", []),
    forall(( member(Pol, [pro_reo, onus_defesa]), member(P, [garantista, intermediario, restritivo]),
             real(C) ),
      ( retractall(politica_global(_)), assertz(politica_global(Pol)),
        caso(C, Fonte, _),
        decide(P, C, D, M), dec_atom(D, DA, F), pena(P, C, Me, Reg, Sub),
        term_to_atom(M, MA),
        format(S, "~w,~w,~w,~w,~w,~w,~w,~w,~w,\"~w\"~n", [C, Fonte, P, Pol, DA, F, Me, Reg, Sub, MA]) )),
    retractall(politica_global(_)), close(S).

% ---------------- E1b: um parâmetro por vez ----------------
% variante(Nome, PerfilFonte, Functor): copia do intermediário, trocando os parâmetros
% com esse functor pelos do perfil fonte
variante(quantidade_isolada_basta,  restritivo, quantidade_isolada_basta).
variante(limites_menores,           restritivo, limite_qtd).
variante(janela_atos_5_anos,        restritivo, janela_ato_infracional).
variante(ato_sem_data_conta,        restritivo, ato_sem_data_conta).
variante(acoes_em_curso_contam,     restritivo, acoes_em_curso_contam).
variante(indicios_amplos,           restritivo, indicios_aceitos).
variante(minimo_1_indicador,        restritivo, minimo_indicadores).
variante(fracao_restritiva,         restritivo, fracao_por_qtd).
variante(quantidade_nao_indica,     garantista, quantidade_indica_dedicacao).
variante(atos_nao_contam,           garantista, janela_ato_infracional).
variante(esquecimento_5_anos,       garantista, esquecimento_anos).
variante(indicios_restritos,        garantista, indicios_aceitos).
variante(fracao_garantista,         garantista, fracao_por_qtd).

cria_variante(Nome, Fonte, Fun) :-
    retractall(param(Nome, _)), retractall(perfil(Nome)),
    forall(( param(intermediario, X), \+ functor(X, Fun, _) ), assertz(param(Nome, X))),
    forall(( param(Fonte, X), functor(X, Fun, _) ), assertz(param(Nome, X))),
    assertz(perfil(Nome)).

e1b :-
    saida('e1_ablacao.csv', Arq), open(Arq, write, S),
    format(S, "variante,origem,parametro,mudam_decisao,mudam_fracao,concede_base,concede_variante,n~n", []),
    retractall(politica_global(_)),
    forall(variante(V, Fonte, Fun),
      ( cria_variante(V, Fonte, Fun),
        findall(B-X, ( real(C), decide(intermediario, C, B, _), decide(V, C, X, _) ), Ps),
        length(Ps, N),
        aggregate_all(count, ( member(B-X, Ps), \+ mesma_decisao(B, X) ), MD),
        aggregate_all(count, ( member(concede(F1)-concede(F2), Ps), F1 \== F2 ), MF),
        aggregate_all(count, member(concede(_)-_, Ps), CB),
        aggregate_all(count, member(_-concede(_), Ps), CV),
        format(S, "~w,~w,~w,~w,~w,~w,~w,~w~n", [V, Fonte, Fun, MD, MF, CB, CV, N]),
        retractall(param(V, _)), retractall(perfil(V)) )),
    close(S).

mesma_decisao(concede(_), concede(_)) :- !.
mesma_decisao(X, X).

main :- e1a, e1b.
