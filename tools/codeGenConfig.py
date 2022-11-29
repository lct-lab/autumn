genConfig = {
    "thrift":{
        "enable":True,
        "namespace":"Radar.Buisiness",
        "service_name":"BasicDataAccess",
        "save_path":"../src/thrift",
        "cmd_path":"thrift.exe"
    },
    "dao":{
        "enable":True,
        "save_path":"../src/dao"
    },
    "service":{
        "enable":True,

        "save_path":"../src/service"
    },
    "controller":{
        "enable":True,
        "save_path":"../src/controller",
        "serverEventHandler": True,
        "processorEventHandler": True,
        "controller_name":"BasicDataAccess"
    },
    "application":{
        "enable":True,
        "save_path":"../src/",
        "application_name":"BasicDataAccess",
        "mode":"threadPool"
    },
    "general":{
        "updateBatch":8 # 数据库更新时提交一次sql时的数据量上限
    }
}

dataInfo = {
    "SysLog":{#表名
        "table_name":"系统日志", #中文表名
        "access_type":[
            {"name":"info_list", "asService":True}, #查询数据列表，排序、分页,asservice 是否作为服务
            {"name":"info_detail", "asService":True}, # 根据id 查询数据详情
            {"name":"insert", "asService":True}, # 批量插入操作
            {"name":"update", "asService":True}, # 批量更新
            {"name":"delete", "asService":True}, # 数据删除操作，与列表查询采用相同输入参数
        ],
        "fields":
            [
                {
                    "name":"id",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件, range 表示范围， eq 表示等号查询
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":"", # 外键链接的字段名
                    "return_link":True, #是否返回外键关联后的数据
                },
                {
                    "name":"create_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"insert_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"update_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"delete_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"is_delete",#字段名称
                    "type":"bool",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"name",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"desc",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"content",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"user",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":"Users", # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":"name", # 外键链接的字段名
                    "return_link":True, #是否返回外键关联后的数据
                },
                {
                    "name":"sub_sys",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":"SubSystems", # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":"name", # 外键链接的字段名
                    "return_link":True, #是否返回外键关联后的数据
                },
                {
                    "name":"log_type",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                }
            ]
    },
    "Users":{#表名
        "table_name":"用户信息", #中文表名
        "access_type":[
            {"name":"info_list", "asService":True}, #查询数据列表，排序、分页,asservice 是否作为服务
            {"name":"info_detail", "asService":True}, # 根据id 查询数据详情
            {"name":"insert", "asService":True}, # 批量插入操作
            {"name":"update", "asService":True}, # 批量更新
            {"name":"delete", "asService":True}, # 数据删除操作，与列表查询采用相同输入参数
        ],
        "fields":
            [
                {
                    "name":"id",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件, range 表示范围， eq 表示等号查询
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":"", # 外键链接的字段名
                    "return_link":True, #是否返回外键关联后的数据
                },
                {
                    "name":"create_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"insert_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"update_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"delete_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"is_delete",#字段名称
                    "type":"bool",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"name",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"desc",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"passwd",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"auth_group",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                }
            ]
    },
    "SubSystems":{#表名
        "table_name":"子系统信息", #中文表名
        "access_type":[
            {"name":"info_list", "asService":True}, #查询数据列表，排序、分页,asservice 是否作为服务
            {"name":"info_detail", "asService":True}, # 根据id 查询数据详情
            {"name":"insert", "asService":True}, # 批量插入操作
            {"name":"update", "asService":True}, # 批量更新
            {"name":"delete", "asService":True}, # 数据删除操作，与列表查询采用相同输入参数
        ],
        "fields":
            [
                {
                    "name":"id",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件, range 表示范围， eq 表示等号查询
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":"", # 外键链接的字段名
                    "return_link":True, #是否返回外键关联后的数据
                },
                {
                    "name":"insert_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"update_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":"range",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"delete_time",#字段名称
                    "type":"timestamp",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"is_delete",#字段名称
                    "type":"bool",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":False, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":False, # 字段是否作为返回
                    "detail_return":False, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"name",#字段名称
                    "type":"text",#字段类型
                    "condition_type":"equal",# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":True, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                },
                {
                    "name":"desc",#字段名称
                    "type":"text",#字段类型
                    "condition_type":None,# 字段作为查询或删除时条件时的类型，None表示不作为条件
                    "in_up_param":True, # 是否作为插入和更新的输入
                    "order":False, #是否用于排序
                    "list_return":True, # 字段是否作为返回
                    "detail_return":True, # 字段是否作为返回
                    "link_table":None, # 字段是否为外键，是的话为外键链接的表名，否的话为None
                    "link_field":None, # 外键链接的字段名
                    "return_link":False, #是否返回外键关联后的数据
                }
            ]
    }
}