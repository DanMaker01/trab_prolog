:- encoding(utf8).
/*  arvore_a.pl -- "juiz virtual": art. 33, § 4º, da Lei 11.343/2006 (tráfico privilegiado)

    Texto legal (leis/drogas.md):
      § 4º  as penas poderão ser reduzidas de um sexto a dois terços [...] desde que o agente
            seja primário, de bons antecedentes, não se dedique às atividades criminosas nem
            integre organização criminosa.
      Art. 42  o juiz considerará, com preponderância [...], a natureza e a quantidade da substância.

    A lei fixa quatro requisitos, mas dois deles ("não se dedique às atividades criminosas" e a
    fração entre 1/6 e 2/3) não dizem COMO decidir. Para virar código, alguém tem de escolher.
    Aqui cada escolha é um PARÂMETRO de um PERFIL (seção 5). A árvore é a mesma; só os
    parâmetros mudam. Isso permite medir quanto a decisão depende de escolhas que a lei não fez.

    Uso:
      ?- [arvore_a, fatos_casos].
      ?- decide(garantista, Caso, Decisao, Motivos).
      ?- pena(restritivo, Caso, Meses, Regime, Substituicao).
      ?- explica(intermediario, Caso).
*/

:- multifile caso/3, data_fato/2, ano_fato_informado/2, droga/2, qtd_g/2, primario/2,
             reincidente/2, maus_antecedentes/2, antecedente_ano/2, ato_infracional/2,
             ultimo_ato_infracional/2, acoes_em_curso/2, associacao/2, indicio/2,
             majorante/2, referencia/3.
:- dynamic   caso/3, data_fato/2, ano_fato_informado/2, droga/2, qtd_g/2, primario/2,
             reincidente/2, maus_antecedentes/2, antecedente_ano/2, ato_infracional/2,
             ultimo_ato_infracional/2, acoes_em_curso/2, associacao/2, indicio/2,
             majorante/2, referencia/3.
:- discontiguous param/2, requisito/4.

/* ------------------------------------------------------------------
   1. Lei aplicável (data do fato)
   O § 4º só existe a partir da Lei 11.343/2006 (vigência: 8/10/2006).
   Antes, valia a Lei 6.368/1976, sem tráfico privilegiado.
   Sem data do fato, presume-se a lei atual.
   ------------------------------------------------------------------ */
vigencia_lei_11343(date(2006, 10, 8)).

lei_aplicavel(C, lei_6368) :-
    data_fato(C, D), vigencia_lei_11343(V), D @< V, !.
lei_aplicavel(C, lei_6368) :-
    \+ data_fato(C, _), ano_fato_informado(C, A), A < 2006, !.
lei_aplicavel(_, lei_11343).

ano_fato(C, A) :- data_fato(C, date(A, _, _)), !.
ano_fato(C, A) :- ano_fato_informado(C, A).

/* ------------------------------------------------------------------
   2. Fatos com três valores: sim | nao | desconhecido
   ------------------------------------------------------------------ */
status(Pred, C, V) :-
    G =.. [Pred, C, V0], catch(G, _, fail), !, V = V0.
status(_, _, desconhecido).

/* ------------------------------------------------------------------
   3. Os quatro requisitos do § 4º
   Cada um devolve: atende | nao_atende | desconhecido
   ------------------------------------------------------------------ */

% 3.1 primário (reincidência afasta a primariedade)
requisito(primario, C, _, nao_atende) :- status(reincidente, C, sim), !.
requisito(primario, C, _, R) :-
    status(primario, C, V), valor(V, R).

% 3.2 bons antecedentes (com ou sem "direito ao esquecimento", conforme o perfil)
requisito(bons_antecedentes, C, P, R) :-
    status(maus_antecedentes, C, V),
    (   V == sim, esquecido(C, P) -> R = atende
    ;   V == sim                  -> R = nao_atende
    ;   V == nao                  -> R = atende
    ;   R = desconhecido ).

esquecido(C, P) :-
    param(P, esquecimento_anos(N)), integer(N),
    antecedente_ano(C, A), ano_fato(C, F), F - A > N.

% 3.3 não se dedicar às atividades criminosas  (o critério vago: ver seção 4)
requisito(nao_dedica, C, P, R) :-
    dedica(C, P, D, _),
    ( D == sim -> R = nao_atende ; R = atende ).

% 3.4 não integrar organização criminosa
requisito(nao_integra_orcrim, C, _, nao_atende) :- associacao(C, condenado), !.
requisito(nao_integra_orcrim, _, _, atende).

valor(sim, atende).
valor(nao, nao_atende).
valor(desconhecido, desconhecido).

/* ------------------------------------------------------------------
   4. "Dedicação a atividades criminosas"
   A lei não define. Cada perfil diz QUAIS indicadores contam e QUANTOS bastam.
   ------------------------------------------------------------------ */
indicador(C, P, quantidade(G)) :-
    param(P, quantidade_indica_dedicacao(sim)),
    qtd_g(C, G), limite_caso(C, P, L), G > L.
indicador(C, P, ato_infracional) :-
    param(P, janela_ato_infracional(J)), J > 0,
    status(ato_infracional, C, sim),
    (   ultimo_ato_infracional(C, A), ano_fato(C, F)
    ->  F - A =< J
    ;   param(P, ato_sem_data_conta(sim)) ).
indicador(C, P, acoes_em_curso) :-
    param(P, acoes_em_curso_contam(sim)),
    status(acoes_em_curso, C, sim).
indicador(C, P, I) :-
    indicio(C, I), param(P, indicios_aceitos(L)), memberchk(I, L).

% limite de quantidade: o mais baixo entre as drogas apreendidas
limite_caso(C, P, L) :-
    findall(X, (droga(C, D), param(P, limite_qtd(D, X))), Xs),
    (   Xs == [] -> param(P, limite_qtd(outra, L)) ; min_list(Xs, L) ).

dedica(C, P, D, Indicadores) :-
    findall(I, indicador(C, P, I), L0), sort(L0, Indicadores),
    length(Indicadores, N),
    param(P, minimo_indicadores(M)),
    (   N >= M                                                  -> D = sim
    ;   param(P, quantidade_isolada_basta(sim)),
        memberchk(quantidade(_), Indicadores)                   -> D = sim
    ;   D = nao ).

/* ------------------------------------------------------------------
   5. Decisão
   decide(+Perfil, ?Caso, -Decisao, -Motivos)
     Decisao = concede(Fracao) | nega | nao_aplicavel
     Motivos = requisitos não atendidos (ou não comprovados)
   ------------------------------------------------------------------ */
decide(P, C, nao_aplicavel, [lei_6368]) :-
    perfil(P), caso(C, _, _), lei_aplicavel(C, lei_6368), !.
decide(P, C, Decisao, Motivos) :-
    perfil(P), caso(C, _, _),
    findall(Req-R, (member(Req, [primario, bons_antecedentes, nao_dedica, nao_integra_orcrim]),
                    requisito(Req, C, P, R)), Rs),
    politica_faltante(P, Pol),
    findall(M, (member(Req-R, Rs), falha(R, Pol, Req, M)), Motivos),
    (   Motivos == [] -> fracao(C, P, F), Decisao = concede(F)
    ;   Decisao = nega ).

% A politica para dado faltante é um eixo separado do perfil: por padrão, a do perfil;
% o experimento pode fixá-la para todos com  assertz(politica_global(onus_defesa)).
:- dynamic politica_global/1.
politica_faltante(_, Pol) :- politica_global(Pol), !.
politica_faltante(P, Pol) :- param(P, dado_faltante(Pol)).

falha(nao_atende,   _,            Req, Req).
falha(desconhecido, onus_defesa,  Req, nao_comprovado(Req)).
% dado_faltante(pro_reo): o que não está provado conta a favor do réu

% fração: a lei dá o intervalo 1/6 a 2/3; o perfil diz como a quantidade (art. 42) modula
fracao(C, P, F) :-
    (   qtd_g(C, G)
    ->  param(P, fracao_por_qtd(Faixas)), faixa(G, Faixas, F)
    ;   param(P, fracao_sem_qtd(F)) ).

faixa(G, [Lim-F | _], F) :- ( Lim == inf ; G =< Lim ), !.
faixa(G, [_ | T], F) :- faixa(G, T, F).

/* ------------------------------------------------------------------
   6. Pena (dosimetria simplificada, para isolar o efeito do § 4º)
   Pena-base no mínimo legal (5 anos = 60 meses); majorante do art. 40 em 1/6;
   § 4º na terceira fase. Regime: art. 33, § 2º, do CP. Substituição: art. 44 do CP
   (possível no tráfico privilegiado desde a Resolução 5/2012 do Senado).
   ------------------------------------------------------------------ */
pena_base(60).

pena(P, C, Meses, Regime, Substituicao) :-
    decide(P, C, Dec, _),
    pena_base(B0),
    ( majorante(C, _) -> B is B0 * 7 / 6 ; B = B0 ),
    ( Dec = concede(F) -> M0 is B * (1 - F) ; M0 = B ),
    Meses is round(M0 * 10) / 10,
    regime(C, Meses, Regime),
    ( Meses =< 48, \+ status(reincidente, C, sim) -> Substituicao = sim ; Substituicao = nao ).

regime(C, _, fechado)    :- status(reincidente, C, sim), !.
regime(_, M, fechado)    :- M > 96, !.
regime(_, M, semiaberto) :- M > 48, !.
regime(_, _, aberto).

/* ------------------------------------------------------------------
   7. Explicação (por que o juiz virtual decidiu assim)
   ------------------------------------------------------------------ */
explica(P, C) :-
    decide(P, C, D, Ms), dedica(C, P, Ded, Inds),
    format("~w | perfil ~w: ~w~n", [C, P, D]),
    forall(member(Req, [primario, bons_antecedentes, nao_dedica, nao_integra_orcrim]),
           ( requisito(Req, C, P, R), format("   ~w: ~w~n", [Req, R]) )),
    format("   dedicacao: ~w (indicadores: ~w)~n   motivos: ~w~n", [Ded, Inds, Ms]).

/* ------------------------------------------------------------------
   8. PERFIS: as escolhas que a lei deixou em aberto
   São parametrizações ilustrativas, ancoradas em leituras que aparecem nas decisões
   estudadas; não são retratos de ministros.
     garantista    ~ a monocrática que concedeu o § 4º para 308 kg e 432 kg de maconha
                     (HC 1.060.758; AREsp 2.946.226): quantidade só modula a fração.
     intermediario ~ leitura "de manual" da jurisprudência: quantidade grande indica
                     dedicação junto com outros elementos; atos infracionais recentes
                     contam (EREsp 1.916.596); ações em curso não (Tema 1.139).
     restritivo    ~ o acórdão da Turma que derrubou aquelas monocráticas: quantidade
                     sozinha basta; qualquer indício conta; o que não foi provado pesa
                     contra o réu.
   ------------------------------------------------------------------ */
perfil(garantista).
perfil(intermediario).
perfil(restritivo).

param(garantista, quantidade_indica_dedicacao(nao)).
param(garantista, quantidade_isolada_basta(nao)).
param(garantista, janela_ato_infracional(0)).
param(garantista, ato_sem_data_conta(nao)).
param(garantista, acoes_em_curso_contam(nao)).
param(garantista, esquecimento_anos(5)).
param(garantista, indicios_aceitos([arma, faccao])).
param(garantista, minimo_indicadores(2)).
param(garantista, dado_faltante(pro_reo)).
param(garantista, fracao_por_qtd([100-2/3, 1000-1/2, 10000-1/3, inf-1/6])).
param(garantista, fracao_sem_qtd(2/3)).

param(intermediario, quantidade_indica_dedicacao(sim)).
param(intermediario, quantidade_isolada_basta(nao)).
param(intermediario, limite_qtd(maconha, 10000)).
param(intermediario, limite_qtd(haxixe, 5000)).
param(intermediario, limite_qtd(cocaina, 1000)).
param(intermediario, limite_qtd(crack, 1000)).
param(intermediario, limite_qtd(sintetica, 500)).
param(intermediario, limite_qtd(outra, 1000)).
param(intermediario, janela_ato_infracional(3)).
param(intermediario, ato_sem_data_conta(nao)).
param(intermediario, acoes_em_curso_contam(nao)).
param(intermediario, esquecimento_anos(nenhum)).
param(intermediario, indicios_aceitos([arma, faccao, petrechos, celular, investigacao_previa, logistica])).
param(intermediario, minimo_indicadores(2)).
param(intermediario, dado_faltante(pro_reo)).
param(intermediario, fracao_por_qtd([100-2/3, 1000-1/2, 10000-1/6, inf-1/6])).
param(intermediario, fracao_sem_qtd(2/3)).

param(restritivo, quantidade_indica_dedicacao(sim)).
param(restritivo, quantidade_isolada_basta(sim)).
param(restritivo, limite_qtd(maconha, 1000)).
param(restritivo, limite_qtd(haxixe, 500)).
param(restritivo, limite_qtd(cocaina, 100)).
param(restritivo, limite_qtd(crack, 100)).
param(restritivo, limite_qtd(sintetica, 50)).
param(restritivo, limite_qtd(outra, 100)).
param(restritivo, janela_ato_infracional(5)).
param(restritivo, ato_sem_data_conta(sim)).
param(restritivo, acoes_em_curso_contam(sim)).
param(restritivo, esquecimento_anos(nenhum)).
param(restritivo, indicios_aceitos([arma, faccao, petrechos, celular, investigacao_previa, logistica,
                                    denuncias, local_conhecido, dinheiro, variedade])).
param(restritivo, minimo_indicadores(1)).
param(restritivo, dado_faltante(pro_reo)).
param(restritivo, fracao_por_qtd([10-2/3, 100-1/2, 1000-1/3, inf-1/6])).
param(restritivo, fracao_sem_qtd(1/6)).
