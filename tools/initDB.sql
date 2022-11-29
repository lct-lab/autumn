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
COMMENT ON COLUMN "Users"."id" IS '�û�ID';
COMMENT ON COLUMN "Users"."create_time" IS '�û�����ʱ��';
COMMENT ON COLUMN "Users"."insert_time" IS '���ʱ��';
COMMENT ON COLUMN "Users"."update_time" IS '����ʱ��';
COMMENT ON COLUMN "Users"."delete_time" IS '�߼�ɾ��ʱ��';
COMMENT ON COLUMN "Users"."is_delete" IS '�Ƿ��߼�ɾ��';
COMMENT ON COLUMN "Users"."name" IS '�û�����';
COMMENT ON COLUMN "Users"."desc" IS '�û���Ϣ����';
COMMENT ON COLUMN "Users"."auth_group" IS '�û�Ȩ�����ͣ������������Ա����ͨ����Ա�����ݷ���Ա��';

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
COMMENT ON COLUMN "SysLog"."id" IS 'ϵͳ��־ID';
COMMENT ON COLUMN "SysLog"."create_time" IS 'ϵͳ�¼�����ʱ��';
COMMENT ON COLUMN "SysLog"."insert_time" IS '���ʱ��';
COMMENT ON COLUMN "SysLog"."name" IS '��־����';
COMMENT ON COLUMN "SysLog"."desc" IS '��־����';
COMMENT ON COLUMN "SysLog"."content" IS '��־��ϸ����';
COMMENT ON COLUMN "SysLog"."user" IS '�����û�ID';
COMMENT ON COLUMN "SysLog"."sub_sys" IS '��������ϵͳID';
COMMENT ON COLUMN "SysLog"."log_type" IS 'ϵͳ��־����';
COMMENT ON COLUMN "SysLog"."is_delete" IS '�Ƿ��߼�ɾ��';
COMMENT ON COLUMN "SysLog"."delete_time" IS 'ɾ��ʱ��';
COMMENT ON COLUMN "SysLog"."update_time" IS '����ʱ��';


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
COMMENT ON COLUMN "SubSystems"."id" IS '��ϵͳ��ϢID';
COMMENT ON COLUMN "SubSystems"."insert_time" IS '���ʱ��';
COMMENT ON COLUMN "SubSystems"."update_time" IS '����ʱ��';
COMMENT ON COLUMN "SubSystems"."delete_time" IS 'ɾ��ʱ��';
COMMENT ON COLUMN "SubSystems"."is_delete" IS '�Ƿ��߼�ɾ��';
COMMENT ON COLUMN "SubSystems"."name" IS '��ϵͳ����';
COMMENT ON COLUMN "SubSystems"."desc" IS '��ϵͳ����';
