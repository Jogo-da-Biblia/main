--
-- Dump tables with csv
--

COPY biblia_testamento FROM '/initial_data/biblia_testamento.csv' WITH (FORMAT csv);
COPY biblia_versao FROM '/initial_data/biblia_versao.csv' WITH (FORMAT csv);
COPY biblia_livro FROM '/initial_data/biblia_livro.csv' WITH (FORMAT csv);
COPY biblia_versiculo FROM '/initial_data/biblia_versiculo.csv' WITH (FORMAT csv);
COPY biblia_livrocapitulonumeroversiculos FROM '/initial_data/biblia_livro_capitulo_numero_versiculos.csv' WITH (FORMAT csv);