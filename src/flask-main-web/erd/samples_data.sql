insert into t_user(userid, username, password, name, isadmin) values(default, 'user1', 't5kskadg', 'User 1', 1);
insert into t_user(userid, username, password, name, isadmin) values(default, 'user2', 't5kskadg', 'User 2', 0);


-- prepare 20 camera list (can't add from management apps, only edit)
insert into t_camera(cameraid, ip, webport, rtspport, username, password, onoff, dockerid, dockername, dockerport, companyname, placename, positionorder, startdate, enddate)
values(default, '', '', '', '', '', 0, 'deb2908f35b17db03966f668ae446aa3fb0198ee112bc73981341fb356e5685e', 'camera-01', '4001', '', '', 1, now(), now());
insert into t_camera(cameraid, ip, webport, rtspport, username, password, onoff, dockerid, dockername, dockerport, companyname, placename, positionorder, startdate, enddate)
values(default, '', '', '', '', '', 0, 'b52e8e591f79916509c03ecfa4e26ddd445675cae8e8c28bf0d893b745e404ef', 'camera-02', '4002', '', '', 2, now(), now());


-- prepare the url base on database
insert into t_setting(settingid, keytag1, keytag2, tag1) values(default, 'SERVER', 'BASEURL', '192.168.1.101');
-- live

insert into t_setting(settingid, keytag1, keytag2, tag1) values(default, 'SERVER', 'BASEURL', '153.126.161.130');


-- NOT USED

-- setting
-- port docker
insert into t_setting(settingid, keytag1, keytag2, tag1, tag2) values(default, 'DOCKER', 'PORT', '4001', '4100');
	

-- list docker
insert into t_setting(settingid, keytag1, keytag2, tag1, tag2) values(default, 'DOCKER', 'SERVER_CAMERA', 'camera-01', '4101');
insert into t_setting(settingid, keytag1, keytag2, tag1, tag2) values(default, 'DOCKER', 'SERVER_CAMERA', 'camera-02', '4102');