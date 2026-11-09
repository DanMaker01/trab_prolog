:- encoding(utf8).
% Gerado por scripts/arvore_b.py -- não editar à mão.
% arvore_b(+Modelo, +Caso, -Classe): Classe = vence | perde (para a defesa)
:- discontiguous arvore_b/3.

arvore_b(com_relator, C, Classe) :-
    (   tem(C, relator, 'DANIELA TEIXEIRA')
    ->
        (   tem(C, classe, 'REsp')
        ->
            Classe = vence
        ;
            (   tem(C, objeto, 'outro')
            ->
                (   tem(C, classe, 'HC')
                ->
                    Classe = perde
                ;
                    Classe = vence
                )
            ;
                Classe = vence
            )
        )
    ;
        (   tem(C, classe, 'REsp')
        ->
            (   tem(C, turma, 'QUINTA TURMA')
            ->
                (   tem(C, objeto, 'autoria')
                ->
                    Classe = vence
                ;
                    Classe = perde
                )
            ;
                Classe = vence
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
            (   tem(C, marcador, 'denuncia_anonima')
            ->
                Classe = perde
            ;
                (   tem(C, marcador, 'local_conhecido')
                ->
                    Classe = perde
                ;
                    Classe = vence
                )
            )
        ;
            Classe = vence
        )
    ;
        (   tem(C, classe, 'HC')
        ->
            (   tem(C, marcador, 'fuga_mudanca_direcao')
            ->
                (   tem(C, marcador, 'denuncia_anonima')
                ->
                    Classe = vence
                ;
                    Classe = perde
                )
            ;
                Classe = perde
            )
        ;
            (   tem(C, objeto, 'outro')
            ->
                Classe = perde
            ;
                (   tem(C, objeto, 'autoria')
                ->
                    Classe = perde
                ;
                    Classe = vence
                )
            )
        )
    ).

