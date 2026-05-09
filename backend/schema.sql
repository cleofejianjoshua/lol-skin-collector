


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


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";





SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL
);


ALTER TABLE "public"."alembic_version" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."rarities" (
    "id" integer NOT NULL,
    "rarity_name" character varying(50) NOT NULL,
    "item_cost" integer NOT NULL,
    "disenchant_value" integer NOT NULL
);


ALTER TABLE "public"."rarities" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."rarities_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."rarities_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."rarities_id_seq" OWNED BY "public"."rarities"."id";



CREATE TABLE IF NOT EXISTS "public"."skins" (
    "id" integer NOT NULL,
    "skin_name" character varying(120) NOT NULL,
    "champion" character varying(80) NOT NULL,
    "rarity_id" integer NOT NULL,
    "image_path" character varying(255) NOT NULL
);


ALTER TABLE "public"."skins" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."skins_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."skins_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."skins_id_seq" OWNED BY "public"."skins"."id";



CREATE TABLE IF NOT EXISTS "public"."user_collection" (
    "id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "skin_id" integer NOT NULL,
    "obtained_at" timestamp without time zone,
    "duplicate_count" integer NOT NULL
);


ALTER TABLE "public"."user_collection" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."user_collection_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."user_collection_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."user_collection_id_seq" OWNED BY "public"."user_collection"."id";



CREATE TABLE IF NOT EXISTS "public"."users" (
    "id" integer NOT NULL,
    "username" character varying(80) NOT NULL,
    "password" character varying(255) NOT NULL,
    "nickname" character varying(20),
    "email" character varying(255),
    "currency" integer
);


ALTER TABLE "public"."users" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."users_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."users_id_seq" OWNED BY "public"."users"."id";



ALTER TABLE ONLY "public"."rarities" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."rarities_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."skins" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."skins_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."user_collection" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."user_collection_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."users" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."users_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."alembic_version"
    ADD CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num");



ALTER TABLE ONLY "public"."rarities"
    ADD CONSTRAINT "rarities_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."rarities"
    ADD CONSTRAINT "rarities_rarity_name_key" UNIQUE ("rarity_name");



ALTER TABLE ONLY "public"."skins"
    ADD CONSTRAINT "skins_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_collection"
    ADD CONSTRAINT "uq_user_skin" UNIQUE ("user_id", "skin_id");



ALTER TABLE ONLY "public"."user_collection"
    ADD CONSTRAINT "user_collection_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_username_key" UNIQUE ("username");



ALTER TABLE ONLY "public"."skins"
    ADD CONSTRAINT "skins_rarity_id_fkey" FOREIGN KEY ("rarity_id") REFERENCES "public"."rarities"("id");



ALTER TABLE ONLY "public"."user_collection"
    ADD CONSTRAINT "user_collection_skin_id_fkey" FOREIGN KEY ("skin_id") REFERENCES "public"."skins"("id");



ALTER TABLE ONLY "public"."user_collection"
    ADD CONSTRAINT "user_collection_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");





ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";





































































































































































GRANT ALL ON TABLE "public"."alembic_version" TO "anon";
GRANT ALL ON TABLE "public"."alembic_version" TO "authenticated";
GRANT ALL ON TABLE "public"."alembic_version" TO "service_role";



GRANT ALL ON TABLE "public"."rarities" TO "anon";
GRANT ALL ON TABLE "public"."rarities" TO "authenticated";
GRANT ALL ON TABLE "public"."rarities" TO "service_role";



GRANT ALL ON SEQUENCE "public"."rarities_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."rarities_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."rarities_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."skins" TO "anon";
GRANT ALL ON TABLE "public"."skins" TO "authenticated";
GRANT ALL ON TABLE "public"."skins" TO "service_role";



GRANT ALL ON SEQUENCE "public"."skins_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."skins_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."skins_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."user_collection" TO "anon";
GRANT ALL ON TABLE "public"."user_collection" TO "authenticated";
GRANT ALL ON TABLE "public"."user_collection" TO "service_role";



GRANT ALL ON SEQUENCE "public"."user_collection_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."user_collection_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."user_collection_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."users" TO "anon";
GRANT ALL ON TABLE "public"."users" TO "authenticated";
GRANT ALL ON TABLE "public"."users" TO "service_role";



GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";































