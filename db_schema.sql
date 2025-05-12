-- Таблица типов партнеров
CREATE TABLE partner_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Таблица партнеров
CREATE TABLE partner (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type_id INTEGER NOT NULL REFERENCES partner_type(id),
    rating INTEGER NOT NULL,
    address VARCHAR(255),
    director_name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(100)
);

-- Таблица продукции
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    param1 NUMERIC NOT NULL,
    param2 NUMERIC NOT NULL
);

-- Таблица материалов
CREATE TABLE material (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица истории реализации продукции
CREATE TABLE sales_history (
    id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner(id),
    product_id INTEGER NOT NULL REFERENCES product(id),
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL
);

-- (Опционально) Таблица для коэффициентов и процента брака по продукции и материалу
CREATE TABLE product_material (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    material_id INTEGER NOT NULL REFERENCES material(id),
    product_coefficient NUMERIC NOT NULL,
    defect_percent NUMERIC NOT NULL
); 