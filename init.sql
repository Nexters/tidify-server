-- init test
create table bookmarks
(
    id              serial not null primary key,
    member_id       integer        not null,
    title           varchar(50) not null,
    url             varchar(1000) not null,
    created_at timestamp without time zone default (now() at time zone 'utc'),
    updated_at timestamp without time zone default (now() at time zone 'utc')
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);