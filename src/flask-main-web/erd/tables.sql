CREATE EXTENSION pgcrypto;


-- USER

CREATE TABLE public.t_user
(
    userid uuid NOT NULL DEFAULT gen_random_uuid(),
    username character varying NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    isadmin integer NOT NULL DEFAULT 0,
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    updated timestamp,
    updateby character varying,
    deleteflag integer NOT NULL DEFAULT 0,
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
    onoff integer NOT NULL DEFAULT 0,
    dockerid character varying NOT NULL DEFAULT '',
    dockername character varying NOT NULL DEFAULT '',
    dockerport character varying NOT NULL DEFAULT '',
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


-- CAMERA POSITION

CREATE TABLE public.t_camera_position
(
    camerapositionid uuid NOT NULL DEFAULT gen_random_uuid(),
    positionnumber integer NOT NULL DEFAULT 0,
    positionname  character varying NOT NULL DEFAULT '',
    cameraid uuid NOT NULL,
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    PRIMARY KEY (camerapositionid),
    CONSTRAINT fk_camera_position
        FOREIGN KEY(cameraid)
            REFERENCES t_camera(cameraid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_camera_position
    OWNER to camera;

COMMENT ON TABLE public.t_camera_position
    IS 'list of camera position';


-- CAMERA POSITION PICTURE

CREATE TABLE public.t_camera_snapshot
(
    camerasnapshotid uuid NOT NULL DEFAULT gen_random_uuid(),
    camerabase64 character varying NOT NULL,
    cameraid uuid NOT NULL,
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    PRIMARY KEY (camerasnapshotid),
    CONSTRAINT fk_camera_snapshot
        FOREIGN KEY(cameraid)
            REFERENCES t_camera(cameraid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_camera_snapshot
    OWNER to camera;

COMMENT ON TABLE public.t_camera_snapshot
    IS 'list of camera snapshot';