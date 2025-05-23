# Jcff - Gerador de Estrutura de Arquivos em JSON

## Descrição

O **Jcff** é uma ferramenta desenvolvida para escanear diretórios do seu computador e gerar um arquivo JSON contendo a estrutura de arquivos e pastas, com opções de filtragem por extensões e padrões a serem ignorados. O programa pode ser utilizado tanto via linha de comando (CLI) quanto por interface gráfica (GUI), facilitando o uso para diferentes perfis de usuários.

## Funcionalidades

- **Escaneamento de Diretórios:** Varre recursivamente uma pasta base, listando arquivos e subpastas.
- **Filtragem por Extensão:** Permite definir quais extensões de arquivos devem ser incluídas no resultado.
- **Ignorar Padrões:** Possibilidade de ignorar arquivos ou pastas por nome ou padrão (com suporte a curingas, ex: `*.log`, `temp*`).
- **Configuração Personalizável:** Salve e reutilize configurações de caminho, extensões e padrões ignorados.
- **Interface CLI e GUI:** Use pelo terminal ou por uma interface gráfica amigável.
- **Exportação em JSON:** Gera um arquivo JSON estruturado com as informações coletadas.

## Estrutura do Projeto

- `src/cli/controller.py`: Controla o fluxo principal do programa, decide entre CLI, GUI ou menu interativo.
- `src/interface/menu.py`: Menu interativo no terminal para executar as principais funções.
- `src/interface/actions/`: Ações específicas para execução com configuração salva, personalizada ou exibição de configurações.
- `src/config/settings_reader.py`: Leitura das configurações salvas.
- `src/config/gui/configuration.py`: Tela de configuração gráfica.
- `src/scanner/file_scanner.py`: Função principal de varredura de diretórios.
- `src/scanner/filters.py`: Funções auxiliares para filtragem de arquivos e padrões.
- `src/exporter/json_formatter.py`: Formata a estrutura para exportação em JSON.
- `src/utils/`: Utilitários diversos (erros, logs, contexto, etc).

## Como Executar

### 1. Pré-requisitos
- Python 3.10 ou superior
- Instale as dependências necessárias (PySide6, etc):

```bash
pip install -r requirements.txt
```

### 2. Executando via Terminal (CLI)

No terminal, navegue até a pasta do projeto e execute:

```bash
python src/main.py
```

Você verá o menu interativo com as opções:
- Executar com configuração salva
- Executar com valores personalizados
- Ver configuração salva
- Configurar
- Sair

Ou, para executar diretamente com argumentos:

```bash
python src/main.py --path "CAMINHO/DA/PASTA" --output "saida.json" --ext .pdf .txt --ignore *.log temp*
```

### 3. Executando a Interface Gráfica (GUI)

Se o programa for empacotado como executável (`main.exe`), basta dar duplo clique no arquivo ou executar pelo terminal:

```bash
./build/main/main.exe
```

A interface gráfica será aberta, permitindo configurar e gerar o JSON de forma visual.

## Observações

- O arquivo de configuração padrão é salvo em `config/settings.conf`.
- Os logs de execução ficam na pasta `logs/`.
- O JSON gerado terá a estrutura de diretórios e arquivos conforme os filtros definidos.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. Para contribuir, siga os passos:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`.
3. Faça suas alterações e commit: `git commit -m '<feat, update, fix> Adicionando nova feature'`.
4. Envie para o repositório remoto: `git push origin minha-feature`.
5. Siga o workflow do projeto.
6. Abra um Pull Request.

## Licença

Este projeto está sob a licença [GNU](./LICENSE).

---

Dúvidas ou sugestões? Abra uma issue ou entre em contato com o desenvolvedor.
