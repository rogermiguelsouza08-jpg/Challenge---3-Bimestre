-- ============================================================
-- Portal Web de Helpdesk — Script de criação do banco (Membro 1)
-- ============================================================
-- Cria a tabela "chamados", que guarda todos os chamados abertos
-- pelos colaboradores.

CREATE TABLE IF NOT EXISTS chamados (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT    NOT NULL,
    descricao   TEXT    NOT NULL,
    prioridade  TEXT    NOT NULL CHECK (prioridade IN ('Baixa', 'Média', 'Alta')),
    status      TEXT    NOT NULL DEFAULT 'Aberto'
                        CHECK (status IN ('Aberto', 'Em Andamento', 'Resolvido'))
);
