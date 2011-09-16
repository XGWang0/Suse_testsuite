--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'Standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: aliases; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aliases (
    id integer NOT NULL,
    alias character varying(255),
    forward_address character varying(255),
    paid character(1) DEFAULT 'N'::bpchar
);


ALTER TABLE public.aliases OWNER TO postgres;

--
-- Data for Name: aliases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY aliases (id, alias, forward_address, paid) FROM stdin;
2	testmail01_alias2	testmail01	N
1	testmail01_alias	testmail01	Y
\.


--
-- Name: aliases_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aliases
    ADD CONSTRAINT aliases_id_key UNIQUE (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

