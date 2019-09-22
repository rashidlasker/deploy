create user IF NOT EXISTS 'www'@'%' identified with mysql_native_password by '$3cureUS';
create database IF NOT EXISTS deploy character set utf8;
grant all on deploy.* to 'www'@'%';