
CREATE DATABASE IF NOT EXISTS saep_db;
USE saep_db;


CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL 
);


CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100)
);


CREATE TABLE animal (
    id_animal INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    responsavel VARCHAR(50),
    observacao VARCHAR(50),
    data_nascimento DATE,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);


CREATE TABLE agendamento (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    data_agendamento DATETIME NOT NULL,
    motivo_servico VARCHAR(255),
    id_animal INT NOT NULL,
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal)
);




INSERT INTO usuario (nome, email, senha) VALUES
('Heloísa', 'heloisa@email.com', '$2b$12$f.fVhbVLJfIH.Mqmrh86COwcK.M7VXh8HrV5GlGOmJHe1ZwSdWnsu');
('Caetano', 'caetano@email.com', '$2b$12$KKTdrAEUZWNSauCrF.muxePfI7yG.U.eQCXAo.rVLz2L1JYOWJbvO'),
('Daniel', 'daniel@email.com', '$2b$12$zDf2PxMi5p8G7zWB1yrM5u/to9a3c3Oydqj35oMPFZ/ll/QWg4gQm');

INSERT INTO cliente (nome, cpf, telefone, email) VALUES
('Flávio Bolsonaro', 'MTIzNDU2Nzg5MTA=', '47123456789', 'flavio@email.com'),
('Renan Santos', 'MTIzNDU2Nzg5MTE=', '48123456789', 'renan@email.com'),
('Lucas Pereira', 'MTIzNDU2Nzg5MTI=', '49123456789', 'lucas@email.com');

INSERT INTO animal (nome, responsavel, observacao, data_nascimento, id_cliente) VALUES
('Thor', 'Dono', 'Porte grande, pelo curto', '2019-05-22', 1),
('Mel', 'Cuidador', 'Pelo longo, tosa na tesoura', '2022-08-13', 2),
('Bidu', 'Dono', 'Tem medo de secador', '2021-12-30', 3);


INSERT INTO agendamento (data_agendamento, motivo_servico, id_animal) VALUES
('2026-10-20 14:00:00', 'Banho e Tosa Higiênica', 1),
('2026-10-21 10:30:00', 'Tosa na Tesoura', 2),
('2026-10-22 16:00:00', 'Banho Simples', 3);

