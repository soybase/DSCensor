--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dscensor; Type: SCHEMA; Schema: -; Owner: ctc
--

CREATE SCHEMA dscensor;


ALTER SCHEMA dscensor OWNER TO ctc;

SET search_path = dscensor, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: annotations; Type: TABLE; Schema: dscensor; Owner: ctc
--

CREATE TABLE annotations (
    annotation_id integer NOT NULL,
    annotation_name text NOT NULL,
    annotation_build character varying(10),
    organism_id integer,
    genome_id integer,
    annotation_home text,
    format character varying(10),
    annotation_counts text NOT NULL
);


ALTER TABLE annotations OWNER TO ctc;

--
-- Name: annotations_annotation_id_seq; Type: SEQUENCE; Schema: dscensor; Owner: ctc
--

CREATE SEQUENCE annotations_annotation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE annotations_annotation_id_seq OWNER TO ctc;

--
-- Name: annotations_annotation_id_seq; Type: SEQUENCE OWNED BY; Schema: dscensor; Owner: ctc
--

ALTER SEQUENCE annotations_annotation_id_seq OWNED BY annotations.annotation_id;


--
-- Name: genomes; Type: TABLE; Schema: dscensor; Owner: ctc
--

CREATE TABLE genomes (
    genome_id integer NOT NULL,
    genome_name text NOT NULL,
    organism_id integer,
    genome_build character varying(10),
    genome_home text,
    genome_counts text NOT NULL
);


ALTER TABLE genomes OWNER TO ctc;

--
-- Name: genomes_genome_id_seq; Type: SEQUENCE; Schema: dscensor; Owner: ctc
--

CREATE SEQUENCE genomes_genome_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genomes_genome_id_seq OWNER TO ctc;

--
-- Name: genomes_genome_id_seq; Type: SEQUENCE OWNED BY; Schema: dscensor; Owner: ctc
--

ALTER SEQUENCE genomes_genome_id_seq OWNED BY genomes.genome_id;


--
-- Name: organisms; Type: TABLE; Schema: dscensor; Owner: ctc
--

CREATE TABLE organisms (
    organism_id integer NOT NULL,
    genus character varying(64),
    species character varying(64),
    abbreviation character varying(64),
    infraspecies character varying(32),
    common_name text
);


ALTER TABLE organisms OWNER TO ctc;

--
-- Name: organisms_organism_id_seq; Type: SEQUENCE; Schema: dscensor; Owner: ctc
--

CREATE SEQUENCE organisms_organism_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE organisms_organism_id_seq OWNER TO ctc;

--
-- Name: organisms_organism_id_seq; Type: SEQUENCE OWNED BY; Schema: dscensor; Owner: ctc
--

ALTER SEQUENCE organisms_organism_id_seq OWNED BY organisms.organism_id;


--
-- Name: annotations annotation_id; Type: DEFAULT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY annotations ALTER COLUMN annotation_id SET DEFAULT nextval('annotations_annotation_id_seq'::regclass);


--
-- Name: genomes genome_id; Type: DEFAULT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY genomes ALTER COLUMN genome_id SET DEFAULT nextval('genomes_genome_id_seq'::regclass);


--
-- Name: organisms organism_id; Type: DEFAULT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY organisms ALTER COLUMN organism_id SET DEFAULT nextval('organisms_organism_id_seq'::regclass);


--
-- Name: annotations annotations_pkey; Type: CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_pkey PRIMARY KEY (annotation_id);


--
-- Name: genomes genomes_pkey; Type: CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY genomes
    ADD CONSTRAINT genomes_pkey PRIMARY KEY (genome_id);


--
-- Name: organisms organisms_pkey; Type: CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY organisms
    ADD CONSTRAINT organisms_pkey PRIMARY KEY (organism_id);


--
-- Name: annotations annotations_genome_id_fkey; Type: FK CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_genome_id_fkey FOREIGN KEY (genome_id) REFERENCES genomes(genome_id);


--
-- Name: annotations annotations_organism_id_fkey; Type: FK CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_organism_id_fkey FOREIGN KEY (organism_id) REFERENCES organisms(organism_id);


--
-- Name: genomes genomes_organism_id_fkey; Type: FK CONSTRAINT; Schema: dscensor; Owner: ctc
--

ALTER TABLE ONLY genomes
    ADD CONSTRAINT genomes_organism_id_fkey FOREIGN KEY (organism_id) REFERENCES organisms(organism_id);


--
-- PostgreSQL database dump complete
--

