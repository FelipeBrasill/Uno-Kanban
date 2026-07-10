CREATE TABLE Usuario 
( 
 Id_Usuario NUMBER,  
 Nome_Usuario VARCHAR(200) NOT NULL,  
 Email_Usuario VARCHAR(100) NOT NULL,  
 Senha_Usuario VARCHAR(50) NOT NULL,  
 Data_Criacao_Usuario DATE,  
 Id_Conquistas NUMBER,  
 UNIQUE (Email_Usuario,Senha_Usuario),
 CONSTRAINT Pk_Usuario PRIMARY KEY (Id_Usuario)
); 

COMMENT ON TABLE Usuario IS 'Armazena os dados cadastrais dos jogadores/usuarios do sistema Uno KanBAN.';
COMMENT ON COLUMN Usuario.Id_Usuario IS 'Identificador unico do usuario (chave primaria).';
COMMENT ON COLUMN Usuario.Nome_Usuario IS 'Nome de exibicao do usuario.';
COMMENT ON COLUMN Usuario.Email_Usuario IS 'Email do usuario, utilizado para login (unico em conjunto com a senha).';
COMMENT ON COLUMN Usuario.Senha_Usuario IS 'Senha do usuario utilizada para autenticacao.';
COMMENT ON COLUMN Usuario.Data_Criacao_Usuario IS 'Data em que a conta do usuario foi criada.';
COMMENT ON COLUMN Usuario.Id_Conquistas IS 'Referencia a conquista de destaque associada ao usuario.';


CREATE TABLE Partida 
( 
 Id_Partida NUMBER,  
 Data_Inicio_Partida DATE,  
 Data_FIm_Partida DATE,  
 Status_Partida JSON,
 CONSTRAINT Pk_Partida PRIMARY KEY (Id_Partida)
); 

COMMENT ON TABLE Partida IS 'Representa uma partida de Uno, contendo periodo de execucao e status geral.';
COMMENT ON COLUMN Partida.Id_Partida IS 'Identificador unico da partida (chave primaria).';
COMMENT ON COLUMN Partida.Data_Inicio_Partida IS 'Data de inicio da partida.';
COMMENT ON COLUMN Partida.Data_FIm_Partida IS 'Data de termino da partida, nula enquanto a partida estiver em andamento.';
COMMENT ON COLUMN Partida.Status_Partida IS 'Status da partida em formato JSON (ex.: se esta finalizada).';


CREATE TABLE Participante_da_partida 
( 
 Id_Pdp NUMBER,  
 Id_Partida NUMBER,  
 Id_Usuario NUMBER,  
 Status_Pdp JSON,  
 Flag_Vencedor_Pdp BOOLEAN DEFAULT 0,
 CONSTRAINT Pk_Pdp PRIMARY KEY (Id_Pdp,Id_Partida, Id_Usuario)
); 

COMMENT ON TABLE Participante_da_partida IS 'Associa usuarios as partidas das quais participam, registrando seu status individual.';
COMMENT ON COLUMN Participante_da_partida.Id_Pdp IS 'Identificador do participante dentro da partida (compoe a chave primaria).';
COMMENT ON COLUMN Participante_da_partida.Id_Partida IS 'Referencia a partida da qual o usuario participa.';
COMMENT ON COLUMN Participante_da_partida.Id_Usuario IS 'Referencia ao usuario participante.';
COMMENT ON COLUMN Participante_da_partida.Status_Pdp IS 'Status do participante na partida em formato JSON (ex.: numero de cartas na mao, se gritou UNO).';
COMMENT ON COLUMN Participante_da_partida.Flag_Vencedor_Pdp IS 'Indica se o participante foi o vencedor da partida (1 = sim, 0 = nao).';


CREATE TABLE Estado_da_Partida 
( 
 Id_Edp NUMBER,  
 Id_Partida NUMBER,  
 Estado_Partida_Edp JSON,
 CONSTRAINT Pk_Edp PRIMARY KEY (Id_Edp,Id_Partida)
); 

COMMENT ON TABLE Estado_da_Partida IS 'Registra snapshots do estado de uma partida ao longo do tempo, para persistencia de estado.';
COMMENT ON COLUMN Estado_da_Partida.Id_Edp IS 'Identificador do estado registrado (compoe a chave primaria).';
COMMENT ON COLUMN Estado_da_Partida.Id_Partida IS 'Referencia a partida a qual o estado pertence.';
COMMENT ON COLUMN Estado_da_Partida.Estado_Partida_Edp IS 'Estado da partida em formato JSON (ex.: etapa atual da partida).';


CREATE TABLE HistoricoJogada 
( 
 id_hj NUMBER,  
 tipo_acao_hj VARCHAR2(20),  
 carta_jogada_hj VARCHAR2(20),  
 data_hora_hj TIMESTAMP,  
 turno_hj NUMBER(10) DEFAULT 0 NOT NULL, 
 id_pdp NUMBER,
 CONSTRAINT pk_hj PRIMARY KEY (id_hj)
);

COMMENT ON TABLE HistoricoJogada IS 'Registra o historico de jogadas realizadas por cada participante durante as partidas.';
COMMENT ON COLUMN HistoricoJogada.Id_Hj IS 'Identificador unico da jogada (chave primaria).';
COMMENT ON COLUMN HistoricoJogada.Tipo_Acao_Hj IS 'Tipo de acao realizada na jogada (ex.: Jogar Carta, Comprar).';
COMMENT ON COLUMN HistoricoJogada.Carta_jogada_Hj IS 'Descricao da carta jogada, quando aplicavel.';
COMMENT ON COLUMN HistoricoJogada.Data_hora_Hj IS 'Data e hora em que a jogada foi realizada.';
COMMENT ON COLUMN HistoricoJogada.Turno_Hj IS 'Numero do turno em que a jogada ocorreu.';
COMMENT ON COLUMN HistoricoJogada.Id_Pdp IS 'Referencia ao participante da partida que executou a jogada.';


CREATE TABLE Conquistas 
( 
 Id_Conquistas NUMBER,  
 Nome_Conquistas VARCHAR(50),  
 Descricao_Conquistas VARCHAR(200),  
 CONSTRAINT Pk_Conquistas PRIMARY KEY (Id_Conquistas)
); 

COMMENT ON TABLE Conquistas IS 'Catalogo de conquistas (achievements) que podem ser obtidas pelos usuarios.';
COMMENT ON COLUMN Conquistas.Id_Conquistas IS 'Identificador unico da conquista (chave primaria).';
COMMENT ON COLUMN Conquistas.Nome_Conquistas IS 'Nome da conquista.';
COMMENT ON COLUMN Conquistas.Descricao_Conquistas IS 'Descricao detalhada da conquista.';


CREATE TABLE Usuario_Tem_Conquistas (

 Id_Usuario NUMBER,
 Id_Conquistas NUMBER,
 CONSTRAINT Pk_Utc PRIMARY KEY (Id_Usuario, Id_Conquistas)  
);

COMMENT ON TABLE Usuario_Tem_Conquistas IS 'Tabela associativa entre usuarios e as conquistas que eles obtiveram.';
COMMENT ON COLUMN Usuario_Tem_Conquistas.Id_Usuario IS 'Referencia ao usuario que obteve a conquista.';
COMMENT ON COLUMN Usuario_Tem_Conquistas.Id_Conquistas IS 'Referencia a conquista obtida pelo usuario.';


CREATE TABLE Item 
( 
 Id_Item NUMBER,  
 Nome_Item VARCHAR(20) NOT NULL,  
 Descricao_Item VARCHAR(200),
 CONSTRAINT Pk_Item PRIMARY KEY (Id_Item)
); 

COMMENT ON TABLE Item IS 'Catalogo de itens cosmeticos/colecionaveis que os usuarios podem possuir.';
COMMENT ON COLUMN Item.Id_Item IS 'Identificador unico do item (chave primaria).';
COMMENT ON COLUMN Item.Nome_Item IS 'Nome do item.';
COMMENT ON COLUMN Item.Descricao_Item IS 'Descricao detalhada do item.';


CREATE TABLE Usuario_Tem_Item 
( 
 Id_Usuario NUMBER,  
 Id_Item NUMBER,  
 Quantidade_Uti NUMBER(2) NOT NULL,
 CONSTRAINT Pk_Uti PRIMARY KEY (Id_Usuario, Id_Item)
); 

COMMENT ON TABLE Usuario_Tem_Item IS 'Tabela associativa entre usuarios e os itens que possuem, com a quantidade de cada item.';
COMMENT ON COLUMN Usuario_Tem_Item.Id_Usuario IS 'Referencia ao usuario que possui o item.';
COMMENT ON COLUMN Usuario_Tem_Item.Id_Item IS 'Referencia ao item possuido pelo usuario.';
COMMENT ON COLUMN Usuario_Tem_Item.Quantidade_Uti IS 'Quantidade do item que o usuario possui.';


CREATE TABLE Comentarios 
( 
 Id_Comentarios NUMBER,
 Id_Usuario NUMBER,  
 Comentarios JSON,
 CONSTRAINT Pk_Comentarios PRIMARY KEY (Id_Comentarios,Id_Usuario)
); 

COMMENT ON TABLE Comentarios IS 'Armazena comentarios feitos pelos usuarios, com conteudo estruturado em JSON.';
COMMENT ON COLUMN Comentarios.Id_Comentarios IS 'Identificador do comentario (compoe a chave primaria).';
COMMENT ON COLUMN Comentarios.Id_Usuario IS 'Referencia ao usuario autor do comentario.';
COMMENT ON COLUMN Comentarios.Comentarios IS 'Conteudo do comentario em formato JSON (ex.: mensagem e tags).';


CREATE TABLE Amigo_de 
( 
 Id_Usuario_1 NUMBER,  
 Id_Usuario_2 NUMBER,
 CONSTRAINT Pk_Amigo_de PRIMARY KEY (Id_Usuario_1, Id_Usuario_2)
); 

COMMENT ON TABLE Amigo_de IS 'Tabela associativa que representa relacoes de amizade entre usuarios.';
COMMENT ON COLUMN Amigo_de.Id_Usuario_1 IS 'Referencia a um dos usuarios da relacao de amizade.';
COMMENT ON COLUMN Amigo_de.Id_Usuario_2 IS 'Referencia ao outro usuario da relacao de amizade.';


-- fks tabela usuario tem conquistas
ALTER TABLE Usuario_Tem_Conquistas ADD CONSTRAINT Fk_id_usuario_conquista FOREIGN KEY(Id_Usuario) REFERENCES Usuario(Id_Usuario);
ALTER TABLE Usuario_Tem_Conquistas ADD CONSTRAINT Fk_id_conquista_Usuario FOREIGN KEY(Id_Conquistas) REFERENCES Conquistas(Id_Conquistas);

-- fks tabela participante_da_partida
ALTER TABLE Participante_da_partida ADD CONSTRAINT Fk_Partida_Pdp FOREIGN KEY(Id_Partida) REFERENCES Partida (Id_Partida);
ALTER TABLE Participante_da_partida ADD CONSTRAINT Fk_Usuario_Pdp FOREIGN KEY(Id_Usuario) REFERENCES Usuario (Id_Usuario);

-- fks tabela estado_da_partida
ALTER TABLE Estado_da_Partida ADD CONSTRAINT Fk_Partida_Edp FOREIGN KEY(Id_Partida) REFERENCES Partida (Id_Partida);

-- fks tabela historicojogada
ALTER TABLE HistoricoJogada ADD CONSTRAINT Fk_Pdp_Hj FOREIGN KEY(Id_Pdp) REFERENCES Participante_da_partida (Id_Pdp);

-- fks tabela uusuario_tem_item
ALTER TABLE Usuario_Tem_Item ADD CONSTRAINT Fk_Usuario_Uti FOREIGN KEY(Id_Usuario) REFERENCES Usuario (Id_Usuario);
ALTER TABLE Usuario_Tem_Item ADD CONSTRAINT Fk_Item_Uti FOREIGN KEY(Id_Item) REFERENCES Item (Id_Item);

-- fks tabela amigo_de
ALTER TABLE Amigo_de ADD CONSTRAINT Fk_Usuario_1_Usuario_2 FOREIGN KEY(Id_Usuario_1) REFERENCES Usuario (Id_Usuario);
ALTER TABLE Amigo_de ADD CONSTRAINT Fk_Usuario_2_Usuario_1 FOREIGN KEY(Id_Usuario_2) REFERENCES Usuario (Id_Usuario);

-- fks tabela comentarios
ALTER TABLE Comentarios ADD CONSTRAINT Fk_Usuario_Comentario FOREIGN KEY(Id_Usuario) REFERENCES Usuario(Id_Usuario);

-- 1. Tabela Conquistas 
INSERT INTO Conquistas (Id_Conquistas, Nome_Conquistas, Descricao_Conquistas) VALUES
(1, 'Kanban das Winx', 'Organizou o projeto com a magia do clube das Winx.'),
(2, 'Atomos de Coca-Cola', 'Enya tomando atomos de coca cola para recuperar a energia.'),
(3, 'Multi-Assentos', 'Gian senta em todas as cadeiras do recinto simultaneamente.'),
(4, 'O Lendario', 'O lendario realiehgay entrou no servidor.'),
(5, 'Entrando no Modo', 'Calvo de tanto tomar +4 no Uno.'),
(6, 'Tempo de Ouro', 'Lembra de quando eu fazia eletrica e tinha cabelo.'),
(7, 'Yhann de Férias', 'Yhann banido do jogo e do kanban pela eternidade.'),
(8, 'Corporação de Bomba', 'Johnatan virou bombeiro e apagou o fogo do server.'),
(9, 'Voz do Eco', 'Gian falando caraaaa a cada 5 segundos.'),
(10, 'Zé Felipe', 'Ficou fofocando em vez de jogar a carta de Uno.');

-- 2. Tabela Item (Baseado nas piadas do Kanban)
INSERT INTO Item (Id_Item, Nome_Item, Descricao_Item) VALUES
(1, 'Front Inexistente', 'O lendario front end do Caio que ninguem nunca viu.'),
(2, 'Claudooatividade', 'Garante 200% de atividade pura na call.'),
(3, 'Martelo do Ban', 'Heitor banido por falar absurdos impublicaveis.'),
(4, 'Monoculo de Lorde', 'Abraham é um lorde e exige respeito no chat.'),
(5, 'Firewall Protect', 'Murilo da it protect bloqueou seu ataque.'),
(6, 'Hiperfoco', 'Pedro autista ativou o modo hiperfoco no Uno.'),
(7, 'Lata de Coca-Cola', 'Contem apenas atomos selecionados da bebida.'),
(8, 'Multicadeira 2000', 'Permite ao Gian ocupar tres lugares ao mesmo tempo.'),
(9, 'Alicate de Eletrica', 'Item relicario da epoca de ouro da eletrica.'),
(10, 'Asas de Winx', 'Acelera o quadro do Kanban em 50%.');

-- 3. Tabela Usuario
INSERT INTO Usuario (Id_Usuario, Nome_Usuario, Email_Usuario, Senha_Usuario, Data_Criacao_Usuario, Id_Conquistas) VALUES
(1, 'gian', 'gian@email.com', 'senha123', TO_DATE('2026-01-01', 'YYYY-MM-DD'), 3),
(2, 'loenardo', 'loenardo@email.com', 'senha123', TO_DATE('2026-01-02', 'YYYY-MM-DD'), 5),
(3, 'felipe', 'felipe@email.com', 'senha123', TO_DATE('2026-01-03', 'YYYY-MM-DD'), 10),
(4, 'realiehgay', 'realiehgay@email.com', 'senha123', TO_DATE('2026-01-04', 'YYYY-MM-DD'), 4),
(5, 'caio', 'caio@email.com', 'senha123', TO_DATE('2026-01-05', 'YYYY-MM-DD'), 1),
(6, 'yhann', 'yhann@email.com', 'senha123', TO_DATE('2026-01-06', 'YYYY-MM-DD'), 7),
(7, 'johnatan', 'johnatan@email.com', 'senha123', TO_DATE('2026-01-07', 'YYYY-MM-DD'), 8),
(8, 'claudio', 'claudio@email.com', 'senha123', TO_DATE('2026-01-08', 'YYYY-MM-DD'), 2),
(9, 'heitor', 'heitor@email.com', 'senha123', TO_DATE('2026-01-09', 'YYYY-MM-DD'), 9),
(10, 'abraham', 'abraham@email.com', 'senha123', TO_DATE('2026-01-10', 'YYYY-MM-DD'), 6);

-- 4. Tabela Partida (Uno Status: cor, carta do topo, sentido, se acabou)
INSERT INTO Partida (Id_Partida, Data_Inicio_Partida, Data_FIm_Partida, Status_Partida) VALUES
(1, TO_DATE('2026-02-01', 'YYYY-MM-DD'), TO_DATE('2026-02-01', 'YYYY-MM-DD'), '{"finalizada": true}'),
(2, TO_DATE('2026-02-02', 'YYYY-MM-DD'), TO_DATE('2026-02-02', 'YYYY-MM-DD'), '{"finalizada": true}'),
(3, TO_DATE('2026-02-03', 'YYYY-MM-DD'), TO_DATE('2026-02-03', 'YYYY-MM-DD'), '{"finalizada": true}'),
(4, TO_DATE('2026-02-04', 'YYYY-MM-DD'), TO_DATE('2026-02-04', 'YYYY-MM-DD'), '{"finalizada": true}'),
(5, TO_DATE('2026-02-05', 'YYYY-MM-DD'), TO_DATE('2026-02-05', 'YYYY-MM-DD'), '{"finalizada": true}'),
(6, TO_DATE('2026-02-06', 'YYYY-MM-DD'), NULL, '{"finalizada": false}'),
(7, TO_DATE('2026-02-07', 'YYYY-MM-DD'), NULL, '{"finalizada": false}'),
(8, TO_DATE('2026-02-08', 'YYYY-MM-DD'), NULL, '{"finalizada": false}'),
(9, TO_DATE('2026-02-09', 'YYYY-MM-DD'), NULL, '{"finalizada": false}'),
(10, TO_DATE('2026-02-10', 'YYYY-MM-DD'), NULL, '{"finalizada": false}');

-- 5. Tabela Participante_da_partida (Uno Status: numero de cartas na mao)
INSERT INTO Participante_da_partida (Id_Pdp, Id_Partida, Id_Usuario, Status_Pdp, Flag_Vencedor_Pdp) VALUES
(1, 1, 1, '{"numero_cartas": 0, "gritou_uno": true}', 1),
(2, 1, 2, '{"numero_cartas": 5, "gritou_uno": false}', 0),
(3, 2, 4, '{"numero_cartas": 0, "gritou_uno": true}', 1),
(4, 2, 3, '{"numero_cartas": 3, "gritou_uno": false}', 0),
(5, 3, 5, '{"numero_cartas": 0, "gritou_uno": true}', 1),
(6, 3, 6, '{"numero_cartas": 12, "gritou_uno": false}', 0),
(7, 4, 8, '{"numero_cartas": 0, "gritou_uno": true}', 1),
(8, 4, 7, '{"numero_cartas": 2, "gritou_uno": false}', 0),
(9, 5, 10, '{"numero_cartas": 0, "gritou_uno": true}', 1),
(10, 5, 9, '{"numero_cartas": 7, "gritou_uno": false}', 0);

-- 6. Tabela Estado_da_Partida
INSERT INTO Estado_da_Partida (Id_Edp, Id_Partida, Estado_Partida_Edp) VALUES
(1, 1, '{"status_etapa": "finalizada"}'),
(2, 2, '{"status_etapa": "finalizada"}'),
(3, 3, '{"status_etapa": "finalizada"}'),
(4, 4, '{"status_etapa": "finalizada"}'),
(5, 5, '{"status_etapa": "finalizada"}'),
(6, 6, '{"status_etapa": "em_andamento"}'),
(7, 7, '{"status_etapa": "em_andamento"}'),
(8, 8, '{"status_etapa": "em_andamento"}'),
(9, 9, '{"status_etapa": "em_andamento"}'),
(10, 10, '{"status_etapa": "em_andamento"}');

-- 7. Tabela HistoricoJogada
INSERT INTO HistoricoJogada (Id_Hj, Tipo_Acao_Hj, Carta_jogada_Hj, Data_hora_Hj, Turno_Hj, Id_Pdp) VALUES
(1, 'Jogar Carta', 'Inverter Vermelho', TO_TIMESTAMP('2026-02-01 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 1),
(2, 'Comprar', 'Nenhuma', TO_TIMESTAMP('2026-02-01 14:01:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 2),
(3, 'Jogar Carta', '7 Azul', TO_TIMESTAMP('2026-02-02 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 3),
(4, 'Jogar Carta', '+2 Verde', TO_TIMESTAMP('2026-02-03 16:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 5),
(5, 'Comprar', 'Nenhuma', TO_TIMESTAMP('2026-02-03 16:01:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 6),
(6, 'Jogar Carta', 'Bloqueio Amarelo', TO_TIMESTAMP('2026-02-04 17:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 7),
(7, 'Jogar Carta', '+4', TO_TIMESTAMP('2026-02-05 18:00:00', 'YYYY-MM-DD HH24:MI:SS'), 5, 9),
(8, 'Jogar Carta', '9 Azul', TO_TIMESTAMP('2026-02-06 19:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 1),
(9, 'Jogar Carta', 'Inverter Verde', TO_TIMESTAMP('2026-02-07 20:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 10),
(10, 'Jogar Carta', '0 Amarelo', TO_TIMESTAMP('2026-02-08 21:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 4);

-- 8. Tabela Usuario_Tem_Conquistas
INSERT INTO Usuario_Tem_Conquistas (Id_Usuario, Id_Conquistas) VALUES
(1, 3), -- Gian -> Multi-Assentos
(1, 9), -- Gian -> Voz do Eco
(3, 10), -- Felipe -> Zé Felipe
(4, 4), -- Realiehgay -> O Lendario
(5, 1), -- Caio -> Kanban das Winx
(6, 7), -- Yhann -> Yhann de Férias
(7, 8), -- Johnatan -> Corporação de Bomba
(8, 2), -- Claudio -> Atomos de Coca-Cola
(9, 9), -- Heitor -> Voz do Eco
(10, 6); -- Abraham -> Tempo de Ouro

-- 9. Tabela Usuario_Tem_Item
INSERT INTO Usuario_Tem_Item (Id_Usuario, Id_Item, Quantidade_Uti) VALUES
(1, 8, 3), -- Gian -> Multicadeira 2000
(5, 1, 1), -- Caio -> Front Inexistente
(8, 2, 1), -- Claudio -> Claudooatividade
(9, 3, 1), -- Heitor -> Martelo do Ban
(10, 4, 1), -- Abraham -> Monoculo de Lorde
(2, 7, 5), -- Leonardo -> Lata de Coca-Cola
(3, 9, 2), -- Felipe -> Alicate de Eletrica
(4, 10, 1), -- Realiehgay -> Asas de Winx
(6, 3, 2), -- Yhann -> Martelo do Ban
(7, 5, 1); -- Johnatan -> Firewall Protect

-- 10. Tabela Comentarios (Chave Primaria composta: Id_Comentarios, Id_Usuario)
INSERT INTO Comentarios (Id_Comentarios, Id_Usuario, Comentarios) VALUES
(1, 1, '{"msg": "Caraaaa, que partida foi essa!", "tags": ["gian", "uno"]}'),
(2, 4, '{"msg": "O lendario ganhou mais uma de voces.", "tags": ["vitoria"]}'),
(3, 5, '{"msg": "O front end sumiu mas o Uno tá em dia.", "tags": ["caio"]}'),
(4, 6, '{"msg": "Fui banido da partida injustamente.", "tags": ["yhann"]}'),
(5, 9, '{"msg": "Falei absurdos e falaria de novo.", "tags": ["heitor"]}'),
(6, 10, '{"msg": "Uma partida digna de lordes.", "tags": ["abraham"]}'),
(7, 8, '{"msg": "Atividade maxima nesse +4 que eu joguei.", "tags": ["claudio"]}'),
(8, 3, '{"msg": "Felipe fofocando no chat em vez de jogar.", "tags": ["felipe"]}'),
(9, 7, '{"msg": "Apaguei o fogo desse deck de Uno.", "tags": ["johnatan"]}'),
(10, 2, '{"msg": "Leonardo calvo de tanto estresse.", "tags": ["uno"]}');

-- 11. Tabela Amigo_de
INSERT INTO Amigo_de (Id_Usuario_1, Id_Usuario_2) VALUES
(1, 2), -- Gian e Leonardo
(1, 3), -- Gian e Felipe
(1, 4), -- Gian e Realiehgay
(5, 9), -- Caio e Heitor
(10, 4), -- Abraham e Realiehgay
(2, 5), -- Leonardo e Realiehgay
(8, 1), -- Claudio e Gian
(2, 3), -- Leonardo e Felipe
(4, 5), -- Realiehgay e Caio
(9, 6); -- Heitor e Yhann

-- Query 1 : Conquista de jogadores

SELECT 
    u.nome_usuario,
    u.data_criacao_usuario, 
    COUNT(utc.id_conquistas) AS qtd_conquistas
FROM Usuario_Tem_Conquistas utc
LEFT JOIN usuario u 
    ON utc.id_usuario = u.id_usuario
LEFT JOIN conquistas c 
    ON utc.id_conquistas = c.id_conquistas
WHERE 
    (u.nome_usuario LIKE '%reali%' or u.nome_usuario in ('leonardo','gian')) 
    AND u.data_criacao_usuario BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD') 
                                    AND TO_DATE('2029-12-31', 'YYYY-MM-DD') or u.data_criacao_usuario is null 
GROUP BY 
    u.nome_usuario,
    u.data_criacao_usuario
HAVING 
    COUNT(utc.id_conquistas) > 0
ORDER BY 
    qtd_conquistas DESC;

-- Query 2: itens
SELECT 
    u.nome_usuario,
    i.nome_item,
    SUM(uti.quantidade_uti) AS total_quantidade
FROM Usuario_Tem_Item uti
JOIN Usuario u 
    ON uti.id_usuario = u.id_usuario
JOIN Item i 
    ON uti.id_item = i.id_item
WHERE 
    i.nome_item IN ('Lata de Coca-Cola', 'Alicate de Eletrica', 'Martelo do Ban')
    AND (u.nome_usuario LIKE '%a%' OR u.data_criacao_usuario IS NULL)
    AND u.data_criacao_usuario BETWEEN TO_DATE('2020-01-01', 'YYYY-MM-DD') 
                                   AND TO_DATE('2030-12-31', 'YYYY-MM-DD')
GROUP BY 
    u.nome_usuario, 
    i.nome_item
ORDER BY 
    total_quantidade DESC;
-- Query 3: jogadas
SELECT
    u.nome_usuario,
    hj.carta_jogada_hj,
    COUNT(hj.id_hj) AS qtd_vezes_jogada
FROM HistoricoJogada hj
JOIN Participante_da_partida pdp 
    ON hj.id_pdp = pdp.id_pdp
JOIN Usuario u 
    ON pdp.id_usuario = u.id_usuario
WHERE 
    (hj.carta_jogada_hj LIKE '%Azul%' OR u.nome_usuario IN ('gian', 'leonardo', 'felipe'))
    AND (hj.data_hora_hj BETWEEN TO_DATE('2026-01-01', 'YYYY-MM-DD') 
                             AND TO_DATE('2026-12-31', 'YYYY-MM-DD') 
         OR u.data_criacao_usuario IS NULL)
GROUP BY 
    u.nome_usuario, 
    hj.carta_jogada_hj
ORDER BY 
    qtd_vezes_jogada DESC;
-- Query 4: partidas
SELECT
    p.id_partida,
    edp.estado_partida_edp,
    COUNT(p.id_partida) AS qtd_registros_estado
FROM Partida p
JOIN Estado_da_Partida edp 
    ON p.id_partida = edp.id_partida
WHERE 
    p.data_inicio_partida BETWEEN TO_DATE('2026-01-01', 'YYYY-MM-DD') 
                              AND TO_DATE('2026-12-31', 'YYYY-MM-DD')
    AND (edp.estado_partida_edp LIKE '%Finalizado%' OR p.data_fim_partida IS NULL)
    AND p.id_partida IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
GROUP BY 
    p.id_partida, 
    edp.estado_partida_edp
ORDER BY 
    p.id_partida;
-- Query 5: quantidade de participantes por partida em andamento

SELECT
    p.id_partida,
    p.data_inicio_partida,
    COUNT(pdp.id_pdp) AS qtd_participantes
FROM Partida p
LEFT JOIN Participante_da_partida pdp 
    ON p.id_partida = pdp.id_partida
LEFT JOIN Usuario u 
    ON pdp.id_usuario = u.id_usuario
WHERE 
    (p.data_fim_partida IS NULL OR u.nome_usuario LIKE '%a%')
    AND p.id_partida IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    AND p.data_inicio_partida BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD') 
                                  AND TO_DATE('2026-12-31', 'YYYY-MM-DD')
GROUP BY 
    p.id_partida, 
    p.data_inicio_partida
ORDER BY 
    qtd_participantes DESC;