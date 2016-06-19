#!/bin/bash
set -euf -o pipefail

SQLDIR=./sql

POPULATE=(
  "locais.sql"
  "delegacoes.sql"
  "esportes.sql"
  "atletas.sql"
  "modalidades_eq.sql"
  "modalidades_ind.sql"
  "times.sql"
  "eventos_ind.sql"
  "eventos_eq.sql"
  "atletas_participam.sql"
  "compoem_times.sql"
  "times_participam.sql"
)

SCHEMA=${1:-public}

echo "-- Apagando o schema caso exista..."
printf "drop schema if exists \"%s\" cascade;\n" $SCHEMA
printf "create schema \"%s\";\n\n" $SCHEMA

echo "-- Definindo o schema atual..."
printf "SET search_path TO %s;\n\n" $SCHEMA

echo "-- Ajusta o estilo padrão das datas..."
echo -ne "set datestyle to ymd;\n\n"

echo "-- Criando as tabelas..."
cat $SQLDIR/create.sql

echo "-- Populando as tabelas..."
for arq in ${POPULATE[@]}
do
    printf -- "\n---------- BEGIN %s ----------\n" "$arq"
    cat "$SQLDIR/populate/$arq"
    printf -- "----------  END  %s ----------\n" "$arq"
done

printf "AVISO: O script gerado vai apagar COMPLETAMENTE (caso exista) o schema '%s'!\n" $SCHEMA 1>&2
