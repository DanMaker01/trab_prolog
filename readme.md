# (acho que vai mudar, não temos dados oficiais sobre abordagem)

O que temos de dados relacionados:

1. Mortes decorrentes de intervenções policiais, por raça/cor (em %) — Brasil 2025

Esta é sua âncora empírica principal. Ela te dá a proporção de vítimas negras vs. brancas no elo final. Com a proporção populacional (PNAD/IBGE), você calcula a razão de risco.

O que escrever:

    "Os dados de letalidade policial mostram disparidade racial de [X] vezes. Essa disparidade no resultado é compatível com a hipótese de que o seletor σ opera também no nó de abordagem, mas não a isola. A demonstração em Prolog mostra que o protocolo P, sozinho, não impede σ — o que é condição necessária para explicar o padrão observado."

2. Taxa de mortes decorrentes de intervenções policiais por UF (2025)

Esta te dá variação entre estados. Se a disparidade racial varia entre UFs que compartilham o mesmo art. 244 CPP, isso é evidência de que σ (o seletor) varia localmente — o que é exatamente o que sua Proposição prevê (σ depende de interpretações admissíveis, que variam por contexto).

O que escrever:

    "O art. 244 do CPP é único para todo o Brasil, mas a taxa de letalidade policial varia [Y] vezes entre UFs. Isso é consistente com a hipótese de que o seletor σ, embora conforme ao protocolo, é localmente determinado."

3. Adolescentes vítimas de MDIP (em %) — Brasil 2025

Reforço etário. Jovens negros concentram a letalidade. Útil para mostrar que o padrão não é aleatório, mas estruturado por idade + raça.




---

## Ideia 1

**Título provisório:** Sistemas especialistas e protocolos de abordagem policial: preservação de viés externo sob regras explícitas

**Tese:** Um sistema especialista baseado em regras pode preservar vieses externos mesmo quando suas regras são explicitamente definidas e seguem um protocolo formal.

> **Legenda:** `[...]` marca o que ainda precisa de alteração, verificação ou decisão.

> `[...]` **"Preservar" é uma alegação causal.** Ela só se sustenta se **E0** (correlação zero, disparidade nula) e **E1** (disparidade cresce com a correlação) forem executados. Sem eles, trocar por **"não impede"** ou **"é compatível com"**.

> `[...]` **Definir "viés externo":** associação, na população de entrada, entre observáveis admitidos pelo protocolo e o atributo protegido.

---

# Parte 1 - Estrutura

## 1. Introdução

### 1.1 Justiça brasileira e controle da busca pessoal

- Persecução penal, polícias militares estaduais, controle judicial feito depois do fato.
- `[...]` Discutir um possível **viés de seleção** no controle judicial: só chegam ao juiz as buscas que produziram prova. **Precisa de fonte.**

### 1.2 Art. 244 e art. 240 §2 do CPP

- O **art. 244** dispensa mandado em três hipóteses: prisão, fundada suspeita e busca domiciliar em curso.
- O **art. 240 §2** define o que se procura (arma proibida e objetos das alíneas *b* a *f* e *h*).
- **Prisão/flagrante é distinta de fundada suspeita;** tratar separadamente.
- `[...]` Conferir a redação vigente dos dois artigos em **fonte primária (Planalto)**. O Manual (pp. 19-20) transcreve a redação de 2000/2007.

### 1.3 Fundada suspeita

- Conceito jurídico indeterminado `[realmete indeterminado?]`, relativo à **busca pessoal**, não à abordagem em si.

### 1.4 Discricionariedade

- Definição do próprio Manual (p. 24): **conveniência, oportunidade e *quantum* da interferência**, distinta de arbítrio.
- **Distinguir de conceito indeterminado:** discricionariedade é escolha entre alternativas lícitas; fundada suspeita é interpretação.
- `[...]` Uma frase de fonte de direito administrativo (doutrina) para sustentar a distinção, além do Manual.

### 1.5 Marcos jurisprudenciais

- **RHC 158.580/BA** (STJ, 6ª Turma, Rel. Min. Rogerio Schietti, 2022): busca fundada em impressão subjetiva sobre atitude ou aparência é ilegal; a suspeita se afere pelo que se sabia antes da busca.
- **HC 208.240/SP** (STF, Plenário, 11/04/2024): a busca pessoal sem mandado não pode ser motivada por raça, sexo, orientação sexual, cor da pele ou aparência física; vedadas generalizações discriminatórias.
- `[...]` **Data exata do julgamento do RHC** e transcrição dos trechos relevantes: ler os votos nos sites do STJ e do STF. Hoje só tenho fontes secundárias.

### 1.6 Premissa em teste

- Resumo da hipótese **H** (seção 4.1) e por que ela é material e não espantalho.

### 1.7 Contribuição e trabalhos relacionados

- Combinação: **protocolo brasileiro concreto + tese do STF como critério normativo + simulação com controle.**
- `[...]` Seção de trabalhos relacionados ausente: textura aberta (Hart), Prolog aplicado à legislação (Sergot et al.; crítica de Leith), definições de justiça algorítmica, policiamento preditivo. **Conferir autoria, ano e conteúdo de cada referência antes de citar.**

---

## 2. Definição do problema

### 2.1 Definições formais

| Símbolo | Significado                                        |
| -------- | -------------------------------------------------- |
| *s*    | Situação                                         |
| *F*    | Fatos legalmente relevantes                        |
| *O*    | Observáveis                                       |
| *A*    | Atributo protegido                                 |
| *B*    | Comportamento real (porta ou não objeto ilícito) |
| *D*    | Decisão                                           |

- **Subdeterminação:** existe *s* e interpretações admissíveis **I1** e **I2** com `D(I1,s) ≠ D(I2,s)`.
- **Viés (contrafactual):** dois casos iguais em (*B*, *F*) e diferentes em *A* recebem decisões diferentes.
- **Disparidade:** razão entre as taxas de busca de pessoas com *B* = 0, por grupo de *A*.
- **Seletor σ:** função que escolhe a interpretação aplicada em cada caso.
- **Proxy X:** observável admitido pelo protocolo e correlacionado com *A*.
- `[...]` **"Comportamento real" só existe na simulação.** Declarar isso na própria definição.

### 2.2 Níveis de abordagem (1, 2 e 3; Manual p. 62)

- Nível 2 ("preventiva") leva a **busca ligeira** sem vínculo explícito com fundada suspeita (conflito aparente com o art. 244).
- **Inconsistência:** Quadro 1 diz que o nível 3 não tem busca; a p. 68 manda busca ligeira nos níveis 2 e 3.
- `[...]` **"Conflito aparente" precisa de argumento:** o Manual não diz que a busca ligeira é a busca do art. 244.

### 2.3 Três nós de decisão, com padrões legais distintos

1. **Abordar** (interpelar)
2. **Buscar**
3. **Usar força/algemas** (SV 11)

- `[...]` **Padrão legal de cada nó:** para abordar, qual é? Pesquisar e definir.

### 2.4 QUEM será abordado

- Percepção como **entrada livre** (pp. 60-61, 67); ausência de critérios para pedestres; lista aberta de suspeição de veículos (pp. 79-80).
- **Atenção:** as "características físicas" da p. 67 são ambíguas entre **atributo protegido** e **proxy**.

### 2.5 Fundada suspeita como oráculo

- O protocolo a toma como **entrada**; o sistema formal não a define.

---

## 3. Metodologia

### 3.1 Corpus e proveniência

- **Manual Básico de Abordagem Policial** (PMBA; curso de 2000, quadros de 2007): fonte primária.
- **POP-SP:** material complementar, **proveniência não verificada**.
- `[...]` Verificar se há versão mais recente do Manual ou do POP. **Decidir se o POP fica no corpus.**

### 3.2 Inventário de regras

- 26 regras (21 na camada de decisão), classes `norm`, `cond`, `interp` e `disc`; camadas `base_legal` e `decisao`.
- `[...]` **Padronizar nomes:** o esboço antigo dizia "determinística, condicional, interpretativa". Usar as classes do inventário.
- `[...]` **Segundo anotador independente** e medida de concordância (kappa de Cohen). Sem isso, a classificação é interpretação sua.
- `[...]` Ampliar a cobertura ou justificar a exclusão de posicionamento tático, transporte coletivo, edificação e progressão de tropa.

### 3.3 Formalização em Prolog

- Conceitos que o Manual não define entram como **oráculos explícitos**.
- `[...]` O arquivo `regras_manual.pl` ainda **não foi carregado em interpretador**. Testar.

### 3.4 Camada C

- Restrições do STJ e do STF como regras adicionais: base *ex ante*, elementos objetivos e concretos, relação com posse de objeto ilícito, atributos protegidos vedados como motivo.
- **Parâmetro *k*:** número mínimo de elementos objetivos exigidos.
- `[...]` **Textura aberta também aqui:** "objetivo e concreto" é indeterminado. Extrair dos acórdãos exemplos do que foi aceito e rejeitado.

### 3.5 Simulação

- **População sintética:** *N*, proporção de *A*, prevalência de *B*, proxy *X* com correlação **ρ** com *A*, poder preditivo **λ = P(B | X)**.
- **Módulos:** protocolo, interpretações, seletor, auditoria.
- **Verificação de cegueira** com `clause/2`: garante só cegueira **sintática**; proxies a contornam.
- `[...]` Justificar cada parâmetro (assumir *B* independente de *A* é uma escolha forte). **Fazer análise de sensibilidade.**

### 3.6 Métricas

- Taxas de abordagem e de busca por grupo;
- Taxa de busca de inocentes (*B* = 0) por grupo;
- Taxa de acerto por grupo;
- Razão de disparidade;
- Teste contrafactual com pares.
- Repetições com sementes distintas.
- `[...]` Se *X* tem poder preditivo, parte da disparidade pode ser "eficiência". **Medir o trade-off (disparidade × acerto).**

### 3.7 Ética

- Dados sintéticos, nenhuma pessoa real, instrumento de auditoria, **não de uso operacional**.
- `[...]` Redigir a declaração ética no formato exigido pela disciplina.

---

## 4. Experimentos

- **4.1** Hipótese material **H** (ver Parte 2)
- **4.2** Proposição e prova por contradição (ver Parte 2)
- **4.3** Protocolo experimental
  - **E0 (controle):** ρ = 0. A disparidade deve ser nula. Se não for, há erro.
  - **E1 (dose-resposta):** variar ρ e λ; medir a disparidade.
  - **E2 (seletor):** seletor guiado por proxy contra seletor neutro (ordem das cláusulas).
  - **E3 (retroalimentação):** abordagens passadas alimentam o policiamento futuro. **Fora do escopo desta fase.**
  - **E4 (camada C):** aplicar P ∪ C com *k* = 1, 2, 3 e medir a redução da disparidade.
- `[...]` "Se fizermos robôs de abordagem, seria diferente?" foi substituído por **E2**. Se quiser manter a pergunta, formular como política de desempate fixa.
- **4.4** Ameaças à validade
  - Circularidade dos parâmetros; simulação não é a rua; um anotador; uma só PM e documento anterior à jurisprudência; infra-marginalidade; textura aberta da camada C.
  - `[...]` **Responder cada ameaça** com um controle ou com uma limitação declarada.

---

## 5. Conclusão

- **Resultados:** o que a Proposição e E0 a E4 mostram.
- **Limitações:** ver 4.4.
- **O que não se conclui:** prevalência de viés na rua, causalidade, comportamento de qualquer polícia real.
- **Fechamento e trabalhos futuros:** aprendizado com abordagens passadas (fase 2).

---

# Parte 2 - Texto-base dos Experimentos

## 4.1 Hipótese H (premissa material)

> **H (suficiência da objetividade):** se toda busca pessoal exigir suspeita fundada em elementos objetivos e concretos, verificáveis *ex ante* e sem atributo protegido como motivo (protocolo P ∪ C), então a prática não gera disparidade racial a comportamento constante.

**Por que é material.** Não é a afirmação de que o protocolo, sozinho, elimina viés. É a premissa de **meio e fim** que fundamenta a política: o STJ justificou a exigência de elementos objetivos, entre outras razões, para evitar a repetição de práticas que reproduzem preconceitos estruturais, como o perfilamento racial. O experimento avalia se o meio atinge o fim.

> `[...]` **Risco de espantalho persiste.** É improvável que algum tribunal alegue que a objetividade, por si, basta. Duas saídas:
>
> **(a)** Reformular H como **"a exigência de objetividade reduz substancialmente a disparidade"** e testar com E4 (redução quantitativa). A prova por contradição só refuta a versão "elimina".
>
> **(b)** Ler os votos e documentar onde se afirma ou se pressupõe suficiência.
>
> **Escolher.**

> `[...]` Como contraexemplo prático, o **HC 208.240/SP**: a condenação foi mantida por maioria, ficando vencidos o relator e dois ministros. Verificar no acórdão se o "local" pesou na decisão antes de usá-lo como exemplo de proxy objetivo.

---

## 4.2 Proposição e prova

**Proposição.** Sejam P ∪ C um protocolo de decisão *D* e *c* um critério ("elemento objetivo e concreto") com ao menos duas interpretações admissíveis **I1** e **I2** tais que `D(I1,s) ≠ D(I2,s)` para alguma *s*. Seja *X* um proxy observável, admissível em P ∪ C, com correlação **ρ > 0** com *A* na população. Então existe um seletor **σ**, função apenas de *X*, cujas execuções são todas conformes a P ∪ C e produzem disparidade por *A* a comportamento constante.

**Escopo.** Resultado de **existência**, não de prevalência. Vale para o protocolo especificado (P ou P ∪ C).

**Prova por contradição.**

1. Suponha **H**.
2. Formalize P ∪ C, com `elemento_objetivo/2` como oráculo.
3. Exiba **I1** e **I2** admissíveis para "elemento objetivo e concreto" com decisões diferentes (por exemplo, **I1:** apenas fato verificável por terceiro ou registro; **I2:** inclui local, horário e comportamento descrito pelo agente).
   > `[...]` Cada interpretação precisa de **apoio textual** (Manual, acórdãos). Sem isso, "admissível" é afirmação sua.
   >
4. Construa **σ(X)** que aplica **I2** quando *X* ocorre e **I1** caso contrário, usando só proxies que não sejam o atributo protegido (local, horário, vestuário, comportamento), com ρ controlada. Cada decisão é admissível; logo toda execução é conforme P ∪ C.
5. **σ** produz razão de disparidade **> 1** para ρ > 0, enquanto **E0** (ρ = 0) dá razão **≈ 1**. Existe execução conforme P ∪ C e disparatada, contradizendo H.

> `[...]` O passo 4 constrói a disparidade a partir de um parâmetro que você escolhe. A prova é de **existência**; o peso empírico vem de **E1** (dose-resposta) e da justificativa dos parâmetros.

> `[...]` **Corolário (versão fraca):** sem a camada C, o mesmo resultado vale para **P sozinho**. É o caso histórico (Manual anterior a 2022 e 2024) e serve de linha de base para **E4**.

---

# Referências provisórias

**Fontes secundárias já consultadas** (substituir por primárias):

- STJ, notícia sobre o RHC 158.580: [https://www.sedep.com.br/?p=129818](https://www.sedep.com.br/?p=129818)
- Informativos e artigos sobre a jurisprudência do STJ: [https://jus.com.br/artigos/106195/novos-contornos-da-busca-pessoal-a-partir-da-recente-jurisprudencia-do-stj](https://jus.com.br/artigos/106195/novos-contornos-da-busca-pessoal-a-partir-da-recente-jurisprudencia-do-stj)
- STF, notícia sobre o HC 208.240 (fonte primária): [https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=532098&amp;ori=1](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=532098&ori=1)
- Tese do STF, comentário: [https://www.dizerodireito.com.br/2024/05/a-busca-pessoal-sem-mandado-judicial.html](https://www.dizerodireito.com.br/2024/05/a-busca-pessoal-sem-mandado-judicial.html)

> `[...]` **Baixar os acórdãos completos** (STJ e STF) e o texto dos **arts. 240 e 244 do CPP**.

**Literatura citada de memória, a verificar:** Hart (textura aberta); Sergot et al., 1986; Leith, 1986; Lum e Isaac, 2016; Ensign et al., 2018; Simoiu, Corbett-Davies e Goel, 2017; Kusner et al. (justiça contrafactual).
