CREATE TABLE "Users" (
                         "id" uuid NOT NULL,
                         "create_time" timestamp NOT NULL DEFAULT current_timestamp,
                         "insert_time" timestamp NOT NULL DEFAULT current_timestamp,
                         "update_time" timestamp NOT NULL DEFAULT current_timestamp,
                         "delete_time" timestamp DEFAULT '1970-01-01',
                         "is_delete" bool NOT NULL DEFAULT false,
                         "name" varchar NOT NULL DEFAULT '',
                         "passwd" varchar(255) NOT NULL,
                         "desc" text DEFAULT '',
                         "auth_group" varchar NOT NULL,
                         PRIMARY KEY ("id") ,
                         CONSTRAINT "username" UNIQUE ("delete_time", "name")
)
    WITHOUT OIDS;
COMMENT ON COLUMN "Users"."id" IS '用户ID';
COMMENT ON COLUMN "Users"."create_time" IS '用户创建时间';
COMMENT ON COLUMN "Users"."insert_time" IS '入库时间';
COMMENT ON COLUMN "Users"."update_time" IS '更新时间';
COMMENT ON COLUMN "Users"."delete_time" IS '逻辑删除时间';
COMMENT ON COLUMN "Users"."is_delete" IS '是否逻辑删除';
COMMENT ON COLUMN "Users"."name" IS '用户名称';
COMMENT ON COLUMN "Users"."desc" IS '用户信息描述';
COMMENT ON COLUMN "Users"."auth_group" IS '用户权限类型（必填，超级管理员、普通操作员、数据分析员）';

CREATE TABLE "SysLog" (
                          "id" uuid NOT NULL,
                          "create_time" timestamp NOT NULL DEFAULT current_timestamp,
                          "insert_time" timestamp NOT NULL DEFAULT current_timestamp,
                          "name" varchar DEFAULT '',
                          "desc" text DEFAULT '',
                          "content" json,
                          "user" uuid,
                          "sub_sys" uuid,
                          "log_type" varchar,
                          "is_delete" bool DEFAULT false,
                          "delete_time" timestamp DEFAULT '1970-01-01',
                          "update_time" timestamp DEFAULT current_timestamp,
                          PRIMARY KEY ("id")
)
    WITHOUT OIDS;
COMMENT ON COLUMN "SysLog"."id" IS '系统日志ID';
COMMENT ON COLUMN "SysLog"."create_time" IS '系统事件发生时间';
COMMENT ON COLUMN "SysLog"."insert_time" IS '入库时间';
COMMENT ON COLUMN "SysLog"."name" IS '日志名称';
COMMENT ON COLUMN "SysLog"."desc" IS '日志描述';
COMMENT ON COLUMN "SysLog"."content" IS '日志详细内容';
COMMENT ON COLUMN "SysLog"."user" IS '关联用户ID';
COMMENT ON COLUMN "SysLog"."sub_sys" IS '关联的子系统ID';
COMMENT ON COLUMN "SysLog"."log_type" IS '系统日志类型';
COMMENT ON COLUMN "SysLog"."is_delete" IS '是否逻辑删除';
COMMENT ON COLUMN "SysLog"."delete_time" IS '删除时间';
COMMENT ON COLUMN "SysLog"."update_time" IS '更新时间';


CREATE TABLE "SubSystems" (
                              "id" uuid NOT NULL,
                              "insert_time" timestamp NOT NULL DEFAULT current_timestamp,
                              "update_time" timestamp NOT NULL DEFAULT current_timestamp,
                              "delete_time" timestamp DEFAULT '1970-01-01',
                              "is_delete" bool NOT NULL DEFAULT false,
                              "name" varchar COLLATE "default" DEFAULT '',
                              "desc" text DEFAULT '',
                              PRIMARY KEY ("id") ,
                              CONSTRAINT "subSysname" UNIQUE ("delete_time", "name")
)
    WITHOUT OIDS;
COMMENT ON COLUMN "SubSystems"."id" IS '子系统信息ID';
COMMENT ON COLUMN "SubSystems"."insert_time" IS '入库时间';
COMMENT ON COLUMN "SubSystems"."update_time" IS '更新时间';
COMMENT ON COLUMN "SubSystems"."delete_time" IS '删除时间';
COMMENT ON COLUMN "SubSystems"."is_delete" IS '是否逻辑删除';
COMMENT ON COLUMN "SubSystems"."name" IS '子系统名称';
COMMENT ON COLUMN "SubSystems"."desc" IS '子系统描述';
