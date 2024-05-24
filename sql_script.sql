CREATE TABLE "User" (id integer primary key, name varchar);

ALTER TABLE "User" REPLICA IDENTITY FULL;

INSERT INTO "User" VALUES (1,'phong');

CREATE TABLE scd2_user (
    surrogate_key SERIAL PRIMARY KEY,
    id INT NOT NULL,
    name VARCHAR(255),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    current_flag BOOLEAN NOT NULL
);



