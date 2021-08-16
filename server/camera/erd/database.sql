create user camera with password 'camera';
alter role camera createdb;
create database cameradb with owner=camera;
grant all privileges on database cameradb to camera;

psql postgres -U camera
\c cameradb camera