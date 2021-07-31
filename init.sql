-- init test
create table bookmarks
(
    id              serial not null primary key,
    user_id       integer        not null,
    title           varchar(50) not null,
    url             varchar(1000) not null,
    created_at timestamp without time zone default (now() at time zone 'utc'),
    updated_at timestamp without time zone default (now() at time zone 'utc')
);

CREATE TYPE status AS ENUM('active', 'deleted', 'blocked');
CREATE TYPE sns_type AS ENUM('facebook', 'google', 'kakao');

create table users
(
    id              serial not null primary key,
    status          status default 'active' not null,
    email           varchar(255)                                                    not null,
    name            varchar(255)                                                    not null,
    profile_img     varchar(1000)                                                   null,
    sns_type        sns_type                           not null,
    created_at timestamp without time zone default (now() at time zone 'utc'),
    updated_at timestamp without time zone default (now() at time zone 'utc')
);