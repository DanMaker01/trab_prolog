:- encoding(utf8).
% Gerado por scripts/arvore_b.py -- não editar à mão.
% arvore_b(+Modelo, +Caso, -Classe): Classe = vence | perde (para a defesa)
:- discontiguous arvore_b/3.

arvore_b(com_relator, C, Classe) :-
    (   tem(C, classe, 'REsp')
    ->
        (   tem(C, relator, 'SEBASTIAO REIS')
        ->
            Classe = vence
        ;
            (   tem(C, relator, 'MARIA MARLUCE')
            ->
                Classe = vence
            ;
                (   tem(C, relator, 'OG FERNANDES')
                ->
                    Classe = vence
                ;
                    Classe = perde
                )
            )
        )
    ;
        (   tem(C, relator, 'OG FERNANDES')
        ->
            (   tem(C, objeto, 'nulidade_busca')
            ->
                Classe = vence
            ;
                Classe = perde
            )
        ;
            Classe = perde
        )
    ).

arvore_b(sem_relator, C, Classe) :-
    (   tem(C, classe, 'REsp')
    ->
        (   tem(C, marcador, 'fuga_mudanca_direcao')
        ->
            Classe = perde
        ;
            Classe = vence
        )
    ;
        (   tem(C, objeto, 'outro')
        ->
            Classe = perde
        ;
            (   tem(C, marcador, 'denuncia_anonima')
            ->
                Classe = vence
            ;
                (   tem(C, marcador, 'local_conhecido')
                ->
                    Classe = vence
                ;
                    Classe = perde
                )
            )
        )
    ).

