create table delegacao (
    -- Código do país como definido no padrão iso-3166-1
    sigla char(3) primary key,
    nome varchar(40) not null,
    linguas text not null,
    n_participantes smallint default 0 not null,
    ouro smallint default 0 not null,
    prata smallint default 0 not null,
    bronze smallint default 0 not null
);

create table esporte (
    codigo char(3) primary key check (codigo ~* '^[a-z]{3}$'),
    nome varchar(15) unique not null,
    trivia text
);

create table atleta (
    registro_olimp char(10) primary key,
    passaporte char(10) not null,
    nome varchar(50) not null,
    data_nasc date not null check (age('2016-08-05', data_nasc) >= interval '16 years'),
    peso numeric(6, 3) not null,
    altura numeric(4, 3) not null,
    genero char(1) not null check (upper(genero) in ('M', 'F')),
    inabilidades text,
    delegacao char(3) not null references delegacao on delete cascade on update cascade,
    esporte char(3) not null references esporte on delete cascade on update cascade
);

create table local (
    id smallserial primary key,
    nome_oficial varchar(50) unique not null,
    apelido varchar(30),
    capacidade integer not null,
    estado char(2) not null,
    cidade varchar(30) not null,
    rua varchar(40) not null,
    numero integer,
    referencia text
);

create table modalidade_ind (
    codigo smallserial primary key,
    nome_usual varchar(30) not null,
    descricao text not null,
    atletas_por_evento smallint not null,
    esporte char(3) not null references esporte on delete cascade on update cascade
);

create table modalidade_eq (
    codigo smallserial primary key,
    nome_usual varchar(30) not null,
    descricao text not null,
    atletas_por_equipe smallint not null,
    equipes_por_evento smallint not null,
    esporte char(3) not null references esporte on delete cascade on update cascade
);

create table "time" (
    id smallserial primary key,
    delegacao char(3) references delegacao,
    modalidade smallint not null references modalidade_eq on delete cascade on update cascade,
    genero char(1) not null check (upper(genero) in ('M', 'F')),
    unique (delegacao, modalidade, genero)
);

create table evento_ind (
    id smallserial primary key,
    local smallint not null references local on delete cascade on update cascade,
    data_hora timestamp not null,
    duracao interval not null,
    fase smallint not null,
    genero char(1) not null check (upper(genero) in ('M', 'F')),
    modalidade smallint not null references modalidade_ind on delete cascade on update cascade,
    unique (local, data_hora)
);

create table evento_eq (
    id smallserial primary key,
    local smallint not null references local on delete cascade on update cascade,
    data_hora timestamp not null,
    duracao interval not null,
    fase smallint not null,
    genero char(1) not null check (upper(genero) in ('M', 'F')),
    modalidade smallint not null references modalidade_eq on delete cascade on update cascade,
    unique (local, data_hora)
);

create table atleta_participa (
    evento smallint references evento_ind on delete cascade on update cascade,
    atleta char(10) references atleta on delete cascade on update cascade,
    classificacao smallint,
    primary key (evento, atleta)
);

create table time_participa (
    evento smallint references evento_eq on delete cascade on update cascade,
    "time" smallint references "time" on delete cascade on update cascade,
    classificacao smallint,
    primary key (evento, "time")
);

create table compoe_time (
    atleta char(10) references atleta on delete cascade on update cascade,
    "time" smallint references "time" on delete cascade on update cascade,
    posicao varchar(15),
    primary key (atleta, "time")
);
