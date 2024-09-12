CREATE TABLE IF NOT EXISTS table1 (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);

INSERT INTO public.table1 (id, description) VALUES (1, 'Sample Name');