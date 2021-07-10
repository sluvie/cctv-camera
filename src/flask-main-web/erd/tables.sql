CREATE EXTENSION pgcrypto;


-- USER

CREATE TABLE public.t_user
(
    userid uuid NOT NULL DEFAULT gen_random_uuid(),
    username character varying NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    isadmin integer NOT NULL DEFAULT 0,
    PRIMARY KEY (userid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_user
    OWNER to camera;

COMMENT ON TABLE public.t_user
    IS 'list of user that can be access to the main website';


-- CAMERA


CREATE TABLE public.t_camera
(
    cameraid uuid NOT NULL DEFAULT gen_random_uuid(),
    ip character varying NOT NULL,
    webport character varying NOT NULL,
    rtspport character varying NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    dockerid character varying NOT NULL,
    dockername character varying NOT NULL,
    dockerport character varying NOT NULL,
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    updated timestamp,
    updateby character varying,
    PRIMARY KEY (cameraid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_camera
    OWNER to camera;

COMMENT ON TABLE public.t_camera
    IS 'list of registered camera';