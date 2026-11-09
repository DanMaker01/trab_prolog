:- encoding(utf8).
% Gerado por scripts/gerar_fatos.py a partir de dados/*.csv -- não editar à mão.
% Um bloco por réu em que o §4º foi discutido. Fato ausente = desconhecido.

caso('t5_202504078750_2', t5, 'Messod Azulay Neto').
droga('t5_202504078750_2', maconha).
qtd_g('t5_202504078750_2', 80600.0).
indicio('t5_202504078750_2', arma).
indicio('t5_202504078750_2', celular).
referencia('t5_202504078750_2', sent_p4, negado).
referencia('t5_202504078750_2', tj_p4, negado).
referencia('t5_202504078750_2', stj_p4, negado).
referencia('t5_202504078750_2', resultado, 'desfavoravel').

caso('t5_202504724059_6', t5, 'Maria Marluce Caldas').
droga('t5_202504724059_6', maconha).
droga('t5_202504724059_6', haxixe).
referencia('t5_202504724059_6', sent_p4, concedido(1/6)).
referencia('t5_202504724059_6', tj_p4, concedido(1/6)).
referencia('t5_202504724059_6', stj_p4, concedido(1/6)).
referencia('t5_202504724059_6', resultado, 'desfavoravel').

caso('t5_202504855650_7', t5, 'Messod Azulay Neto').
droga('t5_202504855650_7', maconha).
qtd_g('t5_202504855650_7', 31.6).
ato_infracional('t5_202504855650_7', sim).
indicio('t5_202504855650_7', petrechos).
indicio('t5_202504855650_7', arma).
majorante('t5_202504855650_7', iv).
referencia('t5_202504855650_7', tj_p4, negado).
referencia('t5_202504855650_7', stj_p4, negado).
referencia('t5_202504855650_7', resultado, 'desfavoravel').

caso('t5_202600032704_9', t5, 'Maria Marluce Caldas').
droga('t5_202600032704_9', maconha).
qtd_g('t5_202600032704_9', 65.54).
majorante('t5_202600032704_9', iii).
referencia('t5_202600032704_9', tj_p4, negado).
referencia('t5_202600032704_9', stj_p4, negado).
referencia('t5_202600032704_9', resultado, 'desfavoravel').

caso('t5_202600121690_10', t5, 'Joel Ilan Paciornik').
majorante('t5_202600121690_10', v).
referencia('t5_202600121690_10', tj_p4, concedido(1/6)).
referencia('t5_202600121690_10', resultado, 'desfavoravel').

caso('t5_202600286910_11', t5, 'Messod Azulay Neto').
majorante('t5_202600286910_11', iii).
referencia('t5_202600286910_11', tj_p4, negado).
referencia('t5_202600286910_11', stj_p4, negado).
referencia('t5_202600286910_11', resultado, 'desfavoravel').

caso('t5_202600362855_12', t5, 'Messod Azulay Neto').
droga('t5_202600362855_12', crack).
qtd_g('t5_202600362855_12', 7.05).
ato_infracional('t5_202600362855_12', sim).
indicio('t5_202600362855_12', celular).
indicio('t5_202600362855_12', denuncias).
referencia('t5_202600362855_12', sent_p4, negado).
referencia('t5_202600362855_12', tj_p4, negado).
referencia('t5_202600362855_12', stj_p4, negado).
referencia('t5_202600362855_12', resultado, 'desfavoravel').

caso('t5_202600586060_17', t5, 'Joel Ilan Paciornik').
primario('t5_202600586060_17', sim).
ato_infracional('t5_202600586060_17', sim).
ultimo_ato_infracional('t5_202600586060_17', 2014).
referencia('t5_202600586060_17', sent_p4, negado).
referencia('t5_202600586060_17', tj_p4, negado).
referencia('t5_202600586060_17', stj_p4, negado).
referencia('t5_202600586060_17', resultado, 'desfavoravel').

caso('t5_202600720880_19', t5, 'Reynaldo Soares da Fonseca').
droga('t5_202600720880_19', maconha).
primario('t5_202600720880_19', nao).
reincidente('t5_202600720880_19', sim).
maus_antecedentes('t5_202600720880_19', sim).
indicio('t5_202600720880_19', denuncias).
referencia('t5_202600720880_19', tj_p4, negado).
referencia('t5_202600720880_19', stj_p4, negado).
referencia('t5_202600720880_19', resultado, 'desfavoravel').

caso('t5_202600826117_20', t5, 'Maria Marluce Caldas').
indicio('t5_202600826117_20', petrechos).
indicio('t5_202600826117_20', dinheiro).
indicio('t5_202600826117_20', variedade).
referencia('t5_202600826117_20', tj_p4, negado).
referencia('t5_202600826117_20', stj_p4, negado).
referencia('t5_202600826117_20', resultado, 'desfavoravel').

caso('t5_202600883848_21', t5, 'Messod Azulay Neto').
indicio('t5_202600883848_21', petrechos).
referencia('t5_202600883848_21', tj_p4, negado).
referencia('t5_202600883848_21', resultado, 'desfavoravel').

caso('t5_202601489800_31', t5, 'Ribeiro Dantas').
droga('t5_202601489800_31', cocaina).
qtd_g('t5_202601489800_31', 2893.8).
primario('t5_202601489800_31', sim).
indicio('t5_202601489800_31', logistica).
referencia('t5_202601489800_31', tj_p4, negado).
referencia('t5_202601489800_31', stj_p4, negado).
referencia('t5_202601489800_31', resultado, 'desfavoravel').

caso('t5_202601529394_32', t5, 'Reynaldo Soares da Fonseca').
data_fato('t5_202601529394_32', date(2022,1,11)).
droga('t5_202601529394_32', maconha).
maus_antecedentes('t5_202601529394_32', sim).
antecedente_ano('t5_202601529394_32', 2015).
indicio('t5_202601529394_32', petrechos).
referencia('t5_202601529394_32', sent_p4, negado).
referencia('t5_202601529394_32', tj_p4, negado).
referencia('t5_202601529394_32', stj_p4, negado).
referencia('t5_202601529394_32', resultado, 'desfavoravel').

caso('t5_202601658547_36', t5, 'Joel Ilan Paciornik').
droga('t5_202601658547_36', maconha).
qtd_g('t5_202601658547_36', 92270.0).
primario('t5_202601658547_36', sim).
maus_antecedentes('t5_202601658547_36', nao).
indicio('t5_202601658547_36', petrechos).
indicio('t5_202601658547_36', celular).
referencia('t5_202601658547_36', tj_p4, negado).
referencia('t5_202601658547_36', stj_p4, negado).
referencia('t5_202601658547_36', resultado, 'desfavoravel').

caso('t5_202601762630_37', t5, 'Ribeiro Dantas').
droga('t5_202601762630_37', cocaina).
primario('t5_202601762630_37', sim).
acoes_em_curso('t5_202601762630_37', sim).
indicio('t5_202601762630_37', petrechos).
indicio('t5_202601762630_37', dinheiro).
indicio('t5_202601762630_37', celular).
indicio('t5_202601762630_37', faccao).
referencia('t5_202601762630_37', sent_p4, negado).
referencia('t5_202601762630_37', tj_p4, negado).
referencia('t5_202601762630_37', stj_p4, concedido(2/3)).
referencia('t5_202601762630_37', resultado, 'parcial').

caso('t5_202601790446_38', t5, 'Reynaldo Soares da Fonseca').
droga('t5_202601790446_38', maconha).
droga('t5_202601790446_38', cocaina).
qtd_g('t5_202601790446_38', 120456.3).
primario('t5_202601790446_38', sim).
maus_antecedentes('t5_202601790446_38', nao).
indicio('t5_202601790446_38', petrechos).
referencia('t5_202601790446_38', sent_p4, negado).
referencia('t5_202601790446_38', tj_p4, negado).
referencia('t5_202601790446_38', stj_p4, negado).
referencia('t5_202601790446_38', resultado, 'desfavoravel').

caso('t5_202602218144_40', t5, 'Reynaldo Soares da Fonseca').
data_fato('t5_202602218144_40', date(2019,10,11)).
droga('t5_202602218144_40', maconha).
qtd_g('t5_202602218144_40', 162.25).
primario('t5_202602218144_40', nao).
reincidente('t5_202602218144_40', sim).
maus_antecedentes('t5_202602218144_40', sim).
indicio('t5_202602218144_40', petrechos).
indicio('t5_202602218144_40', celular).
majorante('t5_202602218144_40', iii).
referencia('t5_202602218144_40', sent_p4, negado).
referencia('t5_202602218144_40', tj_p4, negado).
referencia('t5_202602218144_40', stj_p4, negado).
referencia('t5_202602218144_40', resultado, 'desfavoravel').

caso('t6_202504226684_5', t6, 'Og Fernandes').
data_fato('t6_202504226684_5', date(2023,1,28)).
droga('t6_202504226684_5', cocaina).
qtd_g('t6_202504226684_5', 920.0).
indicio('t6_202504226684_5', celular).
referencia('t6_202504226684_5', tj_p4, negado).
referencia('t6_202504226684_5', stj_p4, negado).
referencia('t6_202504226684_5', resultado, 'desfavoravel').

caso('t6_202600230571_8', t6, 'Carlos Pires Brandao').
primario('t6_202600230571_8', sim).
referencia('t6_202600230571_8', resultado, 'favoravel').

caso('t6_202600615698_11', t6, 'Carlos Pires Brandao').
data_fato('t6_202600615698_11', date(2024,4,4)).
droga('t6_202600615698_11', cocaina).
qtd_g('t6_202600615698_11', 126200.0).
primario('t6_202600615698_11', sim).
maus_antecedentes('t6_202600615698_11', nao).
indicio('t6_202600615698_11', faccao).
indicio('t6_202600615698_11', logistica).
majorante('t6_202600615698_11', v).
referencia('t6_202600615698_11', sent_p4, negado).
referencia('t6_202600615698_11', tj_p4, negado).
referencia('t6_202600615698_11', stj_p4, negado).
referencia('t6_202600615698_11', resultado, 'desfavoravel').

caso('t6_202600641838_12', t6, 'Og Fernandes').
droga('t6_202600641838_12', maconha).
qtd_g('t6_202600641838_12', 196.52).
acoes_em_curso('t6_202600641838_12', sim).
indicio('t6_202600641838_12', petrechos).
indicio('t6_202600641838_12', dinheiro).
referencia('t6_202600641838_12', tj_p4, negado).
referencia('t6_202600641838_12', stj_p4, negado).
referencia('t6_202600641838_12', resultado, 'desfavoravel').

caso('t6_202600650874_14', t6, 'Nilsoni de Freitas (Desembargadora Convocada do TJDFT)').
droga('t6_202600650874_14', crack).
qtd_g('t6_202600650874_14', 150.0).
indicio('t6_202600650874_14', celular).
indicio('t6_202600650874_14', investigacao_previa).
indicio('t6_202600650874_14', faccao).
majorante('t6_202600650874_14', v).
referencia('t6_202600650874_14', sent_p4, negado).
referencia('t6_202600650874_14', tj_p4, negado).
referencia('t6_202600650874_14', stj_p4, negado).
referencia('t6_202600650874_14', resultado, 'desfavoravel').

caso('t6_202601318070_17', t6, 'Nilsoni de Freitas (Desembargadora Convocada do TJDFT)').
droga('t6_202601318070_17', maconha).
qtd_g('t6_202601318070_17', 5600.0).
primario('t6_202601318070_17', sim).
indicio('t6_202601318070_17', celular).
indicio('t6_202601318070_17', variedade).
referencia('t6_202601318070_17', sent_p4, negado).
referencia('t6_202601318070_17', tj_p4, negado).
referencia('t6_202601318070_17', stj_p4, negado).
referencia('t6_202601318070_17', resultado, 'desfavoravel').

caso('t6_202601748090_22', t6, 'Nilsoni de Freitas (Desembargadora Convocada do TJDFT)').
droga('t6_202601748090_22', maconha).
qtd_g('t6_202601748090_22', 416600.0).
majorante('t6_202601748090_22', v).
referencia('t6_202601748090_22', tj_p4, negado).
referencia('t6_202601748090_22', resultado, 'desfavoravel').

caso('t6_202404079440_24', t6, 'Sebastiao Reis Junior').
droga('t6_202404079440_24', maconha).
qtd_g('t6_202404079440_24', 84.0).
indicio('t6_202404079440_24', petrechos).
indicio('t6_202404079440_24', dinheiro).
indicio('t6_202404079440_24', local_conhecido).
referencia('t6_202404079440_24', sent_p4, negado).
referencia('t6_202404079440_24', tj_p4, negado).
referencia('t6_202404079440_24', resultado, 'desfavoravel').

caso('t6_202500655520_25', t6, 'Rogerio Schietti Cruz').
qtd_g('t6_202500655520_25', 107.0).
primario('t6_202500655520_25', sim).
maus_antecedentes('t6_202500655520_25', nao).
indicio('t6_202500655520_25', denuncias).
indicio('t6_202500655520_25', local_conhecido).
referencia('t6_202500655520_25', tj_p4, negado).
referencia('t6_202500655520_25', resultado, 'desfavoravel').

caso('t6_202600596763_31', t6, 'SEBASTIAO REIS JUNIOR').
primario('t6_202600596763_31', sim).
ato_infracional('t6_202600596763_31', sim).
referencia('t6_202600596763_31', tj_p4, negado).
referencia('t6_202600596763_31', stj_p4, negado).
referencia('t6_202600596763_31', resultado, 'desfavoravel').

caso('t6_202601135381_33', t6, 'SEBASTIAO REIS JUNIOR').
droga('t6_202601135381_33', cocaina).
droga('t6_202601135381_33', crack).
indicio('t6_202601135381_33', petrechos).
indicio('t6_202601135381_33', arma).
indicio('t6_202601135381_33', dinheiro).
indicio('t6_202601135381_33', logistica).
majorante('t6_202601135381_33', iv).
referencia('t6_202601135381_33', sent_p4, negado).
referencia('t6_202601135381_33', tj_p4, negado).
referencia('t6_202601135381_33', stj_p4, negado).
referencia('t6_202601135381_33', resultado, 'desfavoravel').

caso('t6_202601443356_37', t6, 'Rogerio Schietti Cruz').
droga('t6_202601443356_37', maconha).
droga('t6_202601443356_37', haxixe).
droga('t6_202601443356_37', cocaina).
droga('t6_202601443356_37', crack).
droga('t6_202601443356_37', sintetica).
indicio('t6_202601443356_37', petrechos).
indicio('t6_202601443356_37', variedade).
referencia('t6_202601443356_37', tj_p4, negado).
referencia('t6_202601443356_37', stj_p4, negado).
referencia('t6_202601443356_37', resultado, 'desfavoravel').

caso('t6_202602279716_42', t6, 'Sebastiao Reis Junior').
droga('t6_202602279716_42', maconha).
droga('t6_202602279716_42', cocaina).
droga('t6_202602279716_42', crack).
qtd_g('t6_202602279716_42', 1883.3).
indicio('t6_202602279716_42', arma).
indicio('t6_202602279716_42', variedade).
majorante('t6_202602279716_42', iii).
referencia('t6_202602279716_42', tj_p4, concedido(1/6)).
referencia('t6_202602279716_42', stj_p4, concedido(1/6)).
referencia('t6_202602279716_42', resultado, 'parcial').

caso('contraste_c01_0', contraste, 'Joel Ilan Paciornik').
ano_fato_informado('contraste_c01_0', 2024).
droga('contraste_c01_0', cocaina).
qtd_g('contraste_c01_0', 24.86).
indicio('contraste_c01_0', petrechos).
indicio('contraste_c01_0', local_conhecido).
referencia('contraste_c01_0', sent_p4, negado).
referencia('contraste_c01_0', tj_p4, negado).
referencia('contraste_c01_0', resultado, 'favoravel').

caso('contraste_c02_1', contraste, 'Ribeiro Dantas').
ano_fato_informado('contraste_c02_1', 2024).
droga('contraste_c02_1', maconha).
qtd_g('contraste_c02_1', 303500.0).
indicio('contraste_c02_1', logistica).
majorante('contraste_c02_1', i).
referencia('contraste_c02_1', sent_p4, negado).
referencia('contraste_c02_1', tj_p4, negado).
referencia('contraste_c02_1', stj_p4, negado).
referencia('contraste_c02_1', resultado, 'desfavoravel').

caso('contraste_c04_3', contraste, 'Reynaldo Soares da Fonseca').
data_fato('contraste_c04_3', date(2025,9,16)).
droga('contraste_c04_3', cocaina).
qtd_g('contraste_c04_3', 1255.0).
primario('contraste_c04_3', sim).
acoes_em_curso('contraste_c04_3', sim).
indicio('contraste_c04_3', investigacao_previa).
indicio('contraste_c04_3', denuncias).
referencia('contraste_c04_3', sent_p4, negado).
referencia('contraste_c04_3', tj_p4, negado).
referencia('contraste_c04_3', stj_p4, concedido(1/6)).
referencia('contraste_c04_3', resultado, 'parcial').

caso('contraste_c05_4', contraste, 'Reynaldo Soares da Fonseca').
data_fato('contraste_c05_4', date(2023,11,18)).
droga('contraste_c05_4', cocaina).
droga('contraste_c05_4', crack).
primario('contraste_c05_4', sim).
maus_antecedentes('contraste_c05_4', sim).
antecedente_ano('contraste_c05_4', 2010).
indicio('contraste_c05_4', dinheiro).
indicio('contraste_c05_4', local_conhecido).
referencia('contraste_c05_4', sent_p4, concedido(2/3)).
referencia('contraste_c05_4', tj_p4, negado).
referencia('contraste_c05_4', stj_p4, concedido(2/3)).
referencia('contraste_c05_4', resultado, 'parcial').

caso('contraste_c06_5', contraste, 'Ribeiro Dantas').
ano_fato_informado('contraste_c06_5', 2024).
droga('contraste_c06_5', maconha).
droga('contraste_c06_5', cocaina).
droga('contraste_c06_5', crack).
primario('contraste_c06_5', sim).
maus_antecedentes('contraste_c06_5', nao).
ato_infracional('contraste_c06_5', sim).
indicio('contraste_c06_5', variedade).
referencia('contraste_c06_5', tj_p4, negado).
referencia('contraste_c06_5', stj_p4, negado).
referencia('contraste_c06_5', resultado, 'desfavoravel').

caso('contraste_c07_6', contraste, 'Messod Azulay Neto').
data_fato('contraste_c07_6', date(2020,9,16)).
droga('contraste_c07_6', crack).
qtd_g('contraste_c07_6', 0.23).
ato_infracional('contraste_c07_6', sim).
indicio('contraste_c07_6', dinheiro).
indicio('contraste_c07_6', investigacao_previa).
indicio('contraste_c07_6', denuncias).
indicio('contraste_c07_6', local_conhecido).
indicio('contraste_c07_6', faccao).
majorante('contraste_c07_6', iii).
referencia('contraste_c07_6', sent_p4, negado).
referencia('contraste_c07_6', tj_p4, negado).
referencia('contraste_c07_6', resultado, 'desfavoravel').

caso('contraste_c10_9', contraste, 'Ribeiro Dantas').
ano_fato_informado('contraste_c10_9', 2023).
droga('contraste_c10_9', maconha).
qtd_g('contraste_c10_9', 17500.0).
primario('contraste_c10_9', sim).
maus_antecedentes('contraste_c10_9', nao).
ato_infracional('contraste_c10_9', nao).
indicio('contraste_c10_9', investigacao_previa).
majorante('contraste_c10_9', v).
referencia('contraste_c10_9', sent_p4, negado).
referencia('contraste_c10_9', tj_p4, concedido(1/2)).
referencia('contraste_c10_9', stj_p4, negado).
referencia('contraste_c10_9', resultado, 'desfavoravel').

caso('contraste_c11_10', contraste, 'Maria Marluce Caldas').
ano_fato_informado('contraste_c11_10', 2024).
droga('contraste_c11_10', maconha).
droga('contraste_c11_10', cocaina).
qtd_g('contraste_c11_10', 219.0).
indicio('contraste_c11_10', petrechos).
indicio('contraste_c11_10', local_conhecido).
referencia('contraste_c11_10', resultado, 'desfavoravel').

caso('contraste_c12_11', contraste, 'Joel Ilan Paciornik').
data_fato('contraste_c12_11', date(2024,1,27)).
droga('contraste_c12_11', cocaina).
qtd_g('contraste_c12_11', 1800.0).
primario('contraste_c12_11', sim).
maus_antecedentes('contraste_c12_11', nao).
ato_infracional('contraste_c12_11', sim).
ultimo_ato_infracional('contraste_c12_11', 2019).
referencia('contraste_c12_11', sent_p4, negado).
referencia('contraste_c12_11', tj_p4, negado).
referencia('contraste_c12_11', stj_p4, concedido(1/6)).
referencia('contraste_c12_11', resultado, 'parcial').

caso('contraste_c13_12', contraste, 'Joel Ilan Paciornik').
data_fato('contraste_c13_12', date(2019,9,10)).
droga('contraste_c13_12', maconha).
droga('contraste_c13_12', crack).
qtd_g('contraste_c13_12', 701.0).
primario('contraste_c13_12', sim).
indicio('contraste_c13_12', petrechos).
indicio('contraste_c13_12', arma).
indicio('contraste_c13_12', variedade).
referencia('contraste_c13_12', sent_p4, concedido(1/6)).
referencia('contraste_c13_12', tj_p4, concedido(1/6)).
referencia('contraste_c13_12', resultado, 'favoravel').

caso('contraste_c14_13', contraste, 'Maria Marluce Caldas').
data_fato('contraste_c14_13', date(2023,3,6)).
droga('contraste_c14_13', maconha).
qtd_g('contraste_c14_13', 12.19).
majorante('contraste_c14_13', iii).
referencia('contraste_c14_13', sent_p4, negado).
referencia('contraste_c14_13', tj_p4, negado).
referencia('contraste_c14_13', stj_p4, negado).
referencia('contraste_c14_13', resultado, 'desfavoravel').

caso('p4_202400047349_0', p4, 'SEBASTIAO REIS').
droga('p4_202400047349_0', maconha).
droga('p4_202400047349_0', haxixe).
qtd_g('p4_202400047349_0', 7751.0).
primario('p4_202400047349_0', sim).
reincidente('p4_202400047349_0', nao).
maus_antecedentes('p4_202400047349_0', nao).
indicio('p4_202400047349_0', arma).
indicio('p4_202400047349_0', denuncias).
referencia('p4_202400047349_0', sent_p4, negado).
referencia('p4_202400047349_0', tj_p4, negado).
referencia('p4_202400047349_0', stj_p4, negado).
referencia('p4_202400047349_0', resultado, 'parcial').

caso('p4_202402568600_1', p4, 'SEBASTIAO REIS').
droga('p4_202402568600_1', cocaina).
qtd_g('p4_202402568600_1', 13.4).
maus_antecedentes('p4_202402568600_1', nao).
referencia('p4_202402568600_1', sent_p4, concedido(1/6)).
referencia('p4_202402568600_1', tj_p4, concedido(1/6)).
referencia('p4_202402568600_1', stj_p4, concedido(2/3)).
referencia('p4_202402568600_1', resultado, 'parcial').

caso('p4_202402816428_2', p4, 'SEBASTIAO REIS').
data_fato('p4_202402816428_2', date(2020,9,8)).
droga('p4_202402816428_2', cocaina).
qtd_g('p4_202402816428_2', 972.7).
primario('p4_202402816428_2', nao).
maus_antecedentes('p4_202402816428_2', sim).
antecedente_ano('p4_202402816428_2', 2019).
indicio('p4_202402816428_2', petrechos).
indicio('p4_202402816428_2', celular).
referencia('p4_202402816428_2', sent_p4, negado).
referencia('p4_202402816428_2', tj_p4, negado).
referencia('p4_202402816428_2', stj_p4, negado).
referencia('p4_202402816428_2', resultado, 'parcial').

caso('p4_202402816428_3', p4, 'SEBASTIAO REIS').
data_fato('p4_202402816428_3', date(2020,9,8)).
droga('p4_202402816428_3', cocaina).
qtd_g('p4_202402816428_3', 972.7).
indicio('p4_202402816428_3', petrechos).
indicio('p4_202402816428_3', celular).
referencia('p4_202402816428_3', sent_p4, concedido(1/3)).
referencia('p4_202402816428_3', tj_p4, concedido(1/3)).
referencia('p4_202402816428_3', resultado, 'parcial').

caso('p4_202403049693_4', p4, 'SEBASTIAO REIS').
droga('p4_202403049693_4', maconha).
droga('p4_202403049693_4', cocaina).
droga('p4_202403049693_4', crack).
associacao('p4_202403049693_4', condenado).
indicio('p4_202403049693_4', celular).
indicio('p4_202403049693_4', investigacao_previa).
indicio('p4_202403049693_4', logistica).
indicio('p4_202403049693_4', variedade).
referencia('p4_202403049693_4', sent_p4, negado).
referencia('p4_202403049693_4', tj_p4, negado).
referencia('p4_202403049693_4', stj_p4, negado).
referencia('p4_202403049693_4', resultado, 'parcial').

caso('p4_202403049693_5', p4, 'SEBASTIAO REIS').
associacao('p4_202403049693_5', condenado).
indicio('p4_202403049693_5', celular).
indicio('p4_202403049693_5', investigacao_previa).
majorante('p4_202403049693_5', v).
referencia('p4_202403049693_5', sent_p4, negado).
referencia('p4_202403049693_5', tj_p4, negado).
referencia('p4_202403049693_5', stj_p4, negado).
referencia('p4_202403049693_5', resultado, 'desfavoravel').

caso('p4_202404276133_6', p4, 'SEBASTIAO REIS').
droga('p4_202404276133_6', crack).
qtd_g('p4_202404276133_6', 19.24).
indicio('p4_202404276133_6', celular).
indicio('p4_202404276133_6', investigacao_previa).
indicio('p4_202404276133_6', local_conhecido).
indicio('p4_202404276133_6', faccao).
referencia('p4_202404276133_6', sent_p4, negado).
referencia('p4_202404276133_6', tj_p4, negado).
referencia('p4_202404276133_6', stj_p4, negado).
referencia('p4_202404276133_6', resultado, 'parcial').

caso('p4_202404432728_7', p4, 'SEBASTIAO REIS').
droga('p4_202404432728_7', cocaina).
qtd_g('p4_202404432728_7', 530.0).
indicio('p4_202404432728_7', arma).
indicio('p4_202404432728_7', investigacao_previa).
referencia('p4_202404432728_7', tj_p4, negado).
referencia('p4_202404432728_7', stj_p4, negado).
referencia('p4_202404432728_7', resultado, 'parcial').

caso('p4_202404432728_8', p4, 'SEBASTIAO REIS').
droga('p4_202404432728_8', cocaina).
qtd_g('p4_202404432728_8', 530.0).
indicio('p4_202404432728_8', arma).
indicio('p4_202404432728_8', investigacao_previa).
referencia('p4_202404432728_8', tj_p4, negado).
referencia('p4_202404432728_8', stj_p4, negado).
referencia('p4_202404432728_8', resultado, 'parcial').

caso('p4_202501700751_9', p4, 'SEBASTIAO REIS').
data_fato('p4_202501700751_9', date(2017,4,22)).
reincidente('p4_202501700751_9', nao).
maus_antecedentes('p4_202501700751_9', sim).
antecedente_ano('p4_202501700751_9', 2015).
referencia('p4_202501700751_9', tj_p4, negado).
referencia('p4_202501700751_9', stj_p4, negado).
referencia('p4_202501700751_9', resultado, 'desfavoravel').

caso('p4_202501891953_10', p4, 'SEBASTIAO REIS').
droga('p4_202501891953_10', maconha).
qtd_g('p4_202501891953_10', 432000.0).
primario('p4_202501891953_10', sim).
maus_antecedentes('p4_202501891953_10', nao).
indicio('p4_202501891953_10', faccao).
indicio('p4_202501891953_10', logistica).
referencia('p4_202501891953_10', tj_p4, negado).
referencia('p4_202501891953_10', stj_p4, negado).
referencia('p4_202501891953_10', resultado, 'desfavoravel').

caso('p4_202502468442_11', p4, 'SEBASTIAO REIS').
droga('p4_202502468442_11', cocaina).
qtd_g('p4_202502468442_11', 2065.0).
primario('p4_202502468442_11', sim).
reincidente('p4_202502468442_11', nao).
maus_antecedentes('p4_202502468442_11', nao).
indicio('p4_202502468442_11', logistica).
referencia('p4_202502468442_11', sent_p4, concedido(1/6)).
referencia('p4_202502468442_11', tj_p4, concedido(1/6)).
referencia('p4_202502468442_11', stj_p4, concedido(1/6)).
referencia('p4_202502468442_11', resultado, 'desfavoravel').

caso('p4_202502487449_12', p4, 'SEBASTIAO REIS').
droga('p4_202502487449_12', maconha).
droga('p4_202502487449_12', cocaina).
droga('p4_202502487449_12', crack).
qtd_g('p4_202502487449_12', 16955.0).
primario('p4_202502487449_12', sim).
reincidente('p4_202502487449_12', nao).
indicio('p4_202502487449_12', petrechos).
indicio('p4_202502487449_12', denuncias).
indicio('p4_202502487449_12', variedade).
referencia('p4_202502487449_12', sent_p4, negado).
referencia('p4_202502487449_12', tj_p4, negado).
referencia('p4_202502487449_12', stj_p4, negado).
referencia('p4_202502487449_12', resultado, 'desfavoravel').

caso('p4_202503172686_13', p4, 'SEBASTIAO REIS').
data_fato('p4_202503172686_13', date(2020,11,11)).
droga('p4_202503172686_13', cocaina).
qtd_g('p4_202503172686_13', 6.9).
indicio('p4_202503172686_13', investigacao_previa).
indicio('p4_202503172686_13', local_conhecido).
referencia('p4_202503172686_13', sent_p4, negado).
referencia('p4_202503172686_13', tj_p4, concedido(1/2)).
referencia('p4_202503172686_13', stj_p4, concedido(2/3)).
referencia('p4_202503172686_13', resultado, 'parcial').

caso('p4_202504574280_14', p4, 'SEBASTIAO REIS').
droga('p4_202504574280_14', cocaina).
primario('p4_202504574280_14', sim).
reincidente('p4_202504574280_14', nao).
maus_antecedentes('p4_202504574280_14', nao).
indicio('p4_202504574280_14', petrechos).
indicio('p4_202504574280_14', arma).
majorante('p4_202504574280_14', iv).
referencia('p4_202504574280_14', sent_p4, negado).
referencia('p4_202504574280_14', tj_p4, negado).
referencia('p4_202504574280_14', stj_p4, negado).
referencia('p4_202504574280_14', resultado, 'parcial').

caso('p4_202504610772_15', p4, 'SEBASTIAO REIS').
droga('p4_202504610772_15', maconha).
droga('p4_202504610772_15', crack).
qtd_g('p4_202504610772_15', 556.0).
referencia('p4_202504610772_15', sent_p4, concedido(1/6)).
referencia('p4_202504610772_15', tj_p4, concedido(1/6)).
referencia('p4_202504610772_15', stj_p4, negado).
referencia('p4_202504610772_15', resultado, 'desfavoravel').

caso('p4_202504939960_16', p4, 'SEBASTIAO REIS').
droga('p4_202504939960_16', maconha).
qtd_g('p4_202504939960_16', 308406.0).
primario('p4_202504939960_16', sim).
indicio('p4_202504939960_16', petrechos).
indicio('p4_202504939960_16', logistica).
referencia('p4_202504939960_16', sent_p4, negado).
referencia('p4_202504939960_16', tj_p4, negado).
referencia('p4_202504939960_16', stj_p4, negado).
referencia('p4_202504939960_16', resultado, 'desfavoravel').

caso('p4_202600439821_17', p4, 'SEBASTIAO REIS').
indicio('p4_202600439821_17', petrechos).
indicio('p4_202600439821_17', arma).
referencia('p4_202600439821_17', tj_p4, concedido(1/6)).
referencia('p4_202600439821_17', stj_p4, negado).
referencia('p4_202600439821_17', resultado, 'desfavoravel').

caso('p4_202601211861_18', p4, 'SEBASTIAO REIS').
droga('p4_202601211861_18', maconha).
qtd_g('p4_202601211861_18', 1108.0).
primario('p4_202601211861_18', sim).
reincidente('p4_202601211861_18', nao).
maus_antecedentes('p4_202601211861_18', nao).
referencia('p4_202601211861_18', tj_p4, negado).
referencia('p4_202601211861_18', stj_p4, concedido(1/2)).
referencia('p4_202601211861_18', resultado, 'parcial').

caso('p4_202601353207_19', p4, 'SEBASTIAO REIS').
droga('p4_202601353207_19', cocaina).
primario('p4_202601353207_19', sim).
reincidente('p4_202601353207_19', nao).
acoes_em_curso('p4_202601353207_19', sim).
indicio('p4_202601353207_19', investigacao_previa).
indicio('p4_202601353207_19', faccao).
referencia('p4_202601353207_19', tj_p4, negado).
referencia('p4_202601353207_19', stj_p4, negado).
referencia('p4_202601353207_19', resultado, 'desfavoravel').

caso('p4_202601412926_20', p4, 'SEBASTIAO REIS').
droga('p4_202601412926_20', haxixe).
droga('p4_202601412926_20', sintetica).
primario('p4_202601412926_20', sim).
reincidente('p4_202601412926_20', nao).
indicio('p4_202601412926_20', petrechos).
indicio('p4_202601412926_20', celular).
indicio('p4_202601412926_20', investigacao_previa).
indicio('p4_202601412926_20', denuncias).
referencia('p4_202601412926_20', sent_p4, negado).
referencia('p4_202601412926_20', tj_p4, negado).
referencia('p4_202601412926_20', stj_p4, negado).
referencia('p4_202601412926_20', resultado, 'desfavoravel').

caso('p4_202601674889_21', p4, 'SEBASTIAO REIS').
indicio('p4_202601674889_21', celular).
indicio('p4_202601674889_21', investigacao_previa).
referencia('p4_202601674889_21', sent_p4, negado).
referencia('p4_202601674889_21', tj_p4, negado).
referencia('p4_202601674889_21', stj_p4, negado).
referencia('p4_202601674889_21', resultado, 'desfavoravel').

