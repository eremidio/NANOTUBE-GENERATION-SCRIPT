#!/bin/bash

#Removendo arquivos que não serão mais necessários
rm -f POSCAR_supercell
rm -f scale.txt


#Renomenando o arquivo final gerado com o nome POSCAR_nanostructure
read -p "Renomear arquivo POSCAR_nanostructure como: " filename
mv POSCAR_nanostructure $filename


