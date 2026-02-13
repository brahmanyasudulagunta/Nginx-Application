--
-- PostgreSQL database dump
--

\restrict PaEmSPVxln01hYsp4yLzH3lPGhzCrGA2xkstC2Pgflm33iDS92PtlLsnL1hG3nT

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: backup_test; Type: TABLE; Schema: public; Owner: krishna
--

CREATE TABLE public.backup_test (
    id integer
);


ALTER TABLE public.backup_test OWNER TO krishna;

--
-- Name: test; Type: TABLE; Schema: public; Owner: krishna
--

CREATE TABLE public.test (
    id integer
);


ALTER TABLE public.test OWNER TO krishna;

--
-- Name: visits; Type: TABLE; Schema: public; Owner: krishna
--

CREATE TABLE public.visits (
    count integer
);


ALTER TABLE public.visits OWNER TO krishna;

--
-- Data for Name: backup_test; Type: TABLE DATA; Schema: public; Owner: krishna
--

COPY public.backup_test (id) FROM stdin;
1
1
1
1
1
1
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: krishna
--

COPY public.test (id) FROM stdin;
1
1
1
\.


--
-- Data for Name: visits; Type: TABLE DATA; Schema: public; Owner: krishna
--

COPY public.visits (count) FROM stdin;
3
\.


--
-- PostgreSQL database dump complete
--

\unrestrict PaEmSPVxln01hYsp4yLzH3lPGhzCrGA2xkstC2Pgflm33iDS92PtlLsnL1hG3nT

