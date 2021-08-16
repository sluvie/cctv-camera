CREATE EXTENSION pgcrypto;


-- USER

CREATE TABLE public.t_user
(
    userid  uuid not null default gen_random_uuid(),
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
	

CREATE TABLE public.t_user_session
(
    	sessionid uuid NOT NULL DEFAULT gen_random_uuid(),
		userid uuid NOT NULL,
    	username character varying NOT NULL,
	    created timestamp NOT NULL DEFAULT now(),
		createby character varying,
    	updated timestamp,
    	updateby character varying,
    	PRIMARY KEY (sessionid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_user_session
    OWNER to camera;

COMMENT ON TABLE public.t_user_session
    IS 'list of user session';


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


-- company name
ALTER TABLE public.t_camera
ADD COLUMN companyname character varying NOT NULL DEFAULT '';

-- place name
ALTER TABLE public.t_camera
ADD COLUMN placename character varying NOT NULL DEFAULT '';

-- position order
ALTER TABLE public.t_camera
ADD COLUMN positionorder integer NOT NULL DEFAULT 1;

-- effective date
ALTER TABLE public.t_camera
ADD COLUMN startdate timestamp NOT NULL DEFAULT now();

ALTER TABLE public.t_camera
ADD COLUMN enddate timestamp NOT NULL DEFAULT now();

-- CAMERA POSITION

CREATE TABLE public.t_camera_position
(
    camerapositionid uuid NOT NULL DEFAULT gen_random_uuid(),
    positionnumber integer NOT NULL DEFAULT 0,
    positionname  character varying NOT NULL DEFAULT '',
    cameraid uuid NOT NULL,
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    PRIMARY KEY (camerapositionid)
    --CONSTRAINT fk_camera_position
    --    FOREIGN KEY(cameraid)
    --        REFERENCES t_camera(cameraid)
)

TABLESPACE pg_default;

ALTER TABLE public.t_camera_position
    OWNER to camera;

COMMENT ON TABLE public.t_camera_position
    IS 'list of camera position';




-- SETTING

CREATE TABLE public.t_setting
(
    settingid uuid NOT NULL DEFAULT gen_random_uuid(),
    keytag1 character varying NOT NULL,
    keytag2 character varying NOT NULL,
    tag1 character varying NOT NULL DEFAULT '',
    tag2 character varying NOT NULL DEFAULT '',
    tag3 character varying NOT NULL DEFAULT '',
    tag4 character varying NOT NULL DEFAULT '',
    tag5 character varying NOT NULL DEFAULT '',
    created timestamp NOT NULL DEFAULT now(),
    createby character varying,
    PRIMARY KEY (settingid)
)

TABLESPACE pg_default;

ALTER TABLE public.setting
    OWNER to camera;

COMMENT ON TABLE public.t_setting
    IS 'setting';






-- NOT USED


-- CAMERA POSITION PICTURE

CREATE TABLE public.t_camera_snapshot
(
    camerasnapshotid uuid NOT NULL DEFAULT gen_random_uuid(),
    snapshotfilename character varying NOT NULL,
    snapshottype integer NOT NULL DEFAULT 0, -- 0: IMAGE, 1: VIDEO
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
