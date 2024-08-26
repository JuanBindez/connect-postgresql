#!/bin/bash

# Parar o serviço PostgreSQL
echo "Parando o serviço PostgreSQL..."
sudo systemctl stop postgresql

# Remover o PostgreSQL e pacotes relacionados
echo "Removendo pacotes PostgreSQL..."
sudo apt-get --purge remove postgresql\* -y

# Remover dependências não utilizadas
echo "Removendo dependências não utilizadas..."
sudo apt-get autoremove -y

# Remover arquivos de configuração restantes
echo "Removendo arquivos de configuração..."
sudo rm -rf /etc/postgresql/
sudo rm -rf /etc/postgresql-common/
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /var/log/postgresql/

# Remover usuário e grupo PostgreSQL
echo "Removendo usuário e grupo PostgreSQL..."
sudo deluser postgres
sudo delgroup postgres

# Atualizar a lista de pacotes
echo "Atualizando a lista de pacotes..."
sudo apt-get update

echo "PostgreSQL removido completamente do sistema."