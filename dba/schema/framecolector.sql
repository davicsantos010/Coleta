-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.0.4
-- PostgreSQL version: 10.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: ticweb | type: DATABASE --
-- DROP DATABASE IF EXISTS ticweb;
ALTER DATABASE framecolector SET datestyle TO "ISO, DMY";
-- ddl-end --


-- object: opendata | type: SCHEMA --
-- DROP SCHEMA IF EXISTS opendata CASCADE;
CREATE SCHEMA opendata;
-- ddl-end --
ALTER SCHEMA opendata OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,opendata;
-- ddl-end --

-- object: opendata.sites | type: TABLE --
-- DROP TABLE IF EXISTS opendata.sites CASCADE;
CREATE TABLE opendata.sites (
	site_id serial NOT NULL,
	url varchar(2048) NOT NULL,
	created_at date NOT NULL DEFAULT CURRENT_DATE,
	status integer NOT NULL DEFAULT 0,  -- Coluna status adicionada aqui
	CONSTRAINT sites_pk PRIMARY KEY (site_id)
);
-- ddl-end --
ALTER TABLE opendata.sites OWNER TO postgres;
-- ddl-end --

-- object: opendata.pages | type: TABLE --
-- DROP TABLE IF EXISTS opendata.pages CASCADE;
CREATE TABLE opendata.pages (
	page_id serial NOT NULL,
  site_id integer NOT NULL,
	url varchar(2048) NOT NULL,
	created_at date NOT NULL DEFAULT CURRENT_DATE,
  FOREIGN KEY (site_id) REFERENCES sites(site_id) ON DELETE CASCADE,
  CONSTRAINT pages_pk PRIMARY KEY (page_id)
);
-- ddl-end --
ALTER TABLE opendata.pages OWNER TO postgres;
-- ddl-end --
