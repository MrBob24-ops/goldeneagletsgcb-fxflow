-- ==========================================
-- FXFlow Initial Database Schema Backup
-- Exact match of the original table provided
-- ==========================================

CREATE TABLE public.transfer_requests (
  tf text NOT NULL,
  customer_kind text NULL,
  customer_id text NULL,
  customer_name text NULL,
  transfer_group text NULL,
  purpose_type text NULL,
  purpose text NULL,
  source_account text NULL,
  source_currency text NULL,
  tx_currency text NULL,
  amount numeric(18, 2) NULL,
  rate text NULL,
  debit text NULL,
  branch text NULL,
  ben_name text NULL,
  ben_country text NULL,
  ben_bank text NULL,
  ben_swift text NULL,
  ben_account_masked text NULL,
  stage integer NULL,
  status text NULL,
  ps_status text NULL,
  ps_submitted boolean NULL DEFAULT false,
  is_demo boolean NULL DEFAULT false,
  submitted_at text NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  rev integer NOT NULL DEFAULT 1,
  data jsonb NOT NULL,
  CONSTRAINT transfer_requests_pkey PRIMARY KEY (tf),
  CONSTRAINT transfer_requests_tf_check CHECK ((tf ~ '^TF[0-9]{10}$'::text))
) TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS ix_req_status ON public.transfer_requests USING btree (status) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS ix_req_customer ON public.transfer_requests USING btree (customer_id) TABLESPACE pg_default;
