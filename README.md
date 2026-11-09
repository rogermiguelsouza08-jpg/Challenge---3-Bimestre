# Portal Web de Helpdesk

## Estrutura (dividida por membro)

| Arquivo | Responsável | O que faz |
|---|---|---|
| `schema.sql` | Membro 1 (Banco) | Script SQL que cria a tabela `chamados` |
| `criar_banco.py` | Membro 1 (Banco) | Executa o `schema.sql` e gera o `helpdesk.db` |
| `banco.py` | **Ponte** | Funções `inserir_chamado`, `listar_chamados`, `atualizar_status`, `deletar_chamado` — é o que liga o banco à tela |
| `interface.py` | Membro 2 (Interface) | Tela em Streamlit (formulário + tabela), consome só as funções de `banco.py` |

## Como rodar

```bash
pip install -r requirements.txt

# 1. Criar o banco (rodar uma vez)
python criar_banco.py

# 2. Subir a interface
streamlit run interface.py
```

## Como funciona o CRUD

- **Create**: formulário no topo. Bloqueia envio se Título ou Descrição estiverem vazios. Status sempre nasce como "Aberto".
- **Read**: a tabela (`st.data_editor`) é carregada com `listar_chamados()` a cada execução.
- **Update**: mude o valor da coluna "Status" direto na célula da tabela — a alteração é aplicada assim que você sai da célula (sem precisar de botão).
- **Delete**: clique no ícone de lixeira da linha, dentro do `st.data_editor`.

O `st.data_editor` guarda em `st.session_state["editor_chamados"]` um dicionário com `edited_rows` e `deleted_rows`. O `interface.py` percorre só essas chaves alteradas e chama `atualizar_status`/`deletar_chamado` — por isso é "silencioso e eficiente": não reescreve linhas que não mudaram.
