#-*-coding:utf-8-*-
import os

from codeGenConfig import dataInfo, genConfig

tab = '    '
n = '\n'


def genDaoCodeInfoList(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct get{tableName}InfoListRet{{
        int retCode;
        std::string retDesc;
        int dataTotal;
        std::vector<Entity> data;
    }};
    // {operateInfo["table_name"]}列表查询
    void get{tableName}InfoList(
        get{tableName}InfoListRet & ret,
$inputParams$
        OrderFields orderField=OrderFields::insert_time, 
        OrderType orderType=OrderType::DESC,
        int limit=200,
        int offset=0
    ){{
        try {{
            log_info("dao get{tableName}InfoList start");
            if(orderType == OrderType::STAY){{
                ret.retCode = -1;
                ret.retDesc = "orderType cannot equals to OrderType::STAY in get{tableName}InfoList method";
            }}
$transID$
            std::string conditionSqls;
$SQLCondition$

            std::string sql = str(format("select $selectField$ from public.\\"{tableName}\\" \\n"
                                         "where  is_delete=false %1%order by %2% %3% limit %4% offset %5%")
                                  % conditionSqls
                                  % OrderFieldsMap[orderField]
                                  % OrderTypeMap[orderType]
                                  % limit
                                  % offset);
            nanodbc::statement statement(*dbConn);
            log_info("Dao get{tableName}InfoList excuting sql:\\n" + sql);
            prepare(statement, sql);
            int i = 0;
$SQLBind$
            nanodbc::result sqlResult = statement.execute(1, dbPool->sqlTimeout);
            while (sqlResult.next()) {{
                Entity dataItem;
$dataItem$
                transform(dataItem.id.begin(),dataItem.id.end(), dataItem.id.begin(), ::tolower);
                ret.data.push_back(dataItem);
            }}
            ret.retCode = 0;
            ret.retDesc = "success";
            ret.dataTotal = ret.data.size();
        }} catch (std::exception &e) {{
            log_error("Error in Dao get{tableName}InfoList");
            log_error(e.what());
            dbConn = dbPool->getConnection();
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("dao get{tableName}InfoList finish");
    }}
    '''
    inputInfos = []
    outputInfos = []
    inputContainID = False
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['condition_type'] is not None:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            if fieldInfo['name'] == 'id':
                inputContainID = True
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            if fieldInfo['condition_type'] in ["range", 'equal']:
                fieldItem['type'] = f'const std::vector<{trans2CppType(fieldInfo["type"])}> &'
                fieldItem['note'] = "指定范围的开始和结束" if fieldInfo['condition_type'] == "range" else "取值在此列表中"
            else:
                fieldItem['type'] = trans2CppType(fieldInfo['type'])
                fieldItem['note'] = "取值与此输入相等"
            inputInfos.append(fieldItem)
        if fieldInfo['list_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo['type'])
            outputInfos.append(fieldItem)
    inputParam = n.join([tab * 2 + f'{fieldItem["type"]} {fieldItem["name"]},// {fieldItem["note"]}' \
                         for fieldItem in inputInfos]);
    funcCode = funcTemplate.replace("$inputParams$", inputParam)

    transID = tab * 3 + 'toUpperCase(id);' if inputContainID else ''
    funcCode = funcCode.replace("$transID$", transID)

    selectField = ','.join([f'\\"{e["name"]}\\"' \
                            for i, e in enumerate(outputInfos)])
    funcCode = funcCode.replace("$selectField$", selectField)

    SQLCondition = n.join([f'''
            if({e['name']}.size() != 2)
                throw std::exception("range input parameter {e['name']} should be have size of 2");
    '''
                           for e in inputInfos if e['condition_type'] == 'range'])
    SQLCondition += n.join([
        tab * 3 + f'conditionSqls += sql_condition_gen<{e["rawType"]}>("{e["condition_type"]}", {e["name"]}, "{e["name"]}");' \
        for e in inputInfos])
    funcCode = funcCode.replace("$SQLCondition$", SQLCondition)

    SQLBind = ''
    for inputItem in inputInfos:
        if inputItem["rawType"] == "std::string":
            bindExp = f'statement.bind(i++, {inputItem["name"]}[j].c_str());'
        else:
            bindExp = f'statement.bind(i++, &{inputItem["name"]}[j]);'
        SQLBind += f'''
            for (int j = 0; j < {inputItem["name"]}.size(); j++) {{
                {bindExp}
            }}
        '''
    funcCode = funcCode.replace("$SQLBind$", SQLBind)

    dataItem = n.join([tab * 4 + f'dataItem.{e["name"]} = sqlResult.get<{e["rawType"]}>({i});' \
                       for i, e in enumerate(outputInfos)])
    funcCode = funcCode.replace("$dataItem$", dataItem)
    return funcCode


def genServiceCodeInfoList(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct get{tableName}InfoListRet{{
        int retCode;
        std::string retDesc;
        int dataTotal;
        std::vector<Entity> data;
    }};
    // {operateInfo["table_name"]}列表查询服务
    void get{tableName}InfoList(
        get{tableName}InfoListRet & ret,
$inputParams$
        OrderFields orderField=OrderFields::insert_time, 
        OrderType orderType=OrderType::DESC,
        int limit=200,
        int offset=0
    ){{
        try {{
            log_info("service get{tableName}InfoList start");
            {tableName}Dao daoObj;
            {tableName}Dao::get{tableName}InfoListRet daoRet;
            daoObj.get{tableName}InfoList(daoRet, $passParams$,
                                        static_cast<{tableName}Dao::OrderFields>(orderField),
                                        static_cast<{tableName}Dao::OrderType>(orderType),limit,offset);
            ret.retCode = daoRet.retCode;
            ret.retDesc = daoRet.retDesc;
$linkInit$
            if(daoRet.retCode == 0){{
                for(auto dataItem: daoRet.data){{
                    Entity e;
$retAssign$
$linkFillID$
                    ret.data.push_back(e);
                }}
$linkRet$
                for(int i = 0; i< ret.data.size(); i++){{
$linkTable$
                }}
                ret.dataTotal = ret.data.size();
            }}
        }} catch (std::exception &e) {{
            log_error("Error in service get{tableName}InfoList");
            log_error(e.what());
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("service get{tableName}InfoList finish");
    }}
    '''
    inputInfos = []
    outputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['condition_type'] is not None:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            if fieldInfo['condition_type'] in ["range", 'equal']:
                fieldItem['type'] = f'const std::vector<{trans2CppType(fieldInfo["type"])}> &'
                fieldItem['note'] = "指定范围的开始和结束" if fieldInfo['condition_type'] == "range" else "取值在此列表中"
            else:
                fieldItem['type'] = trans2CppType(fieldInfo['type'])
                fieldItem['note'] = "取值与此输入相等"
            inputInfos.append(fieldItem)
        if fieldInfo['list_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['link_table'] = fieldInfo['link_table']
            fieldItem['link_field'] = fieldInfo['link_field']
            fieldItem['rawType'] = trans2CppType(fieldInfo['type'])
            outputInfos.append(fieldItem)

    inputParam = n.join([tab * 2 + f'{fieldItem["type"]} {fieldItem["name"]},// {fieldItem["note"]}' \
                         for fieldItem in inputInfos]);
    funcCode = funcTemplate.replace("$inputParams$", inputParam)

    passParams = ','.join([fieldItem["name"] for fieldItem in inputInfos]);
    funcCode = funcCode.replace("$passParams$", passParams)

    retAssign = n.join([tab * 5 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                        for i, e in enumerate(outputInfos)])
    funcCode = funcCode.replace("$retAssign$", retAssign)

    linkInit = n.join([tab*4 + f'''std::vector<std::string> {e['name']}_id;'''
                       for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkInit$", linkInit)

    linkFillID = n.join([tab*5 + f'''{e['name']}_id.push_back(e.{e['name']});'''
                         for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkFillID$", linkFillID)

    linkRet = n.join([tab*5 + f'''
                {e['link_table']}Dao dao{e['link_table']};
                {e['link_table']}Dao::get{e['link_table']}InfoDetailRet ret{e['link_table']}Dao;
                dao{e['link_table']}.get{e['link_table']}InfoDetail(ret{e['link_table']}Dao, {e['name']}_id);'''
                      for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkRet$", linkRet)

    linkTable = n.join([f'''
                    std::string cur_{e['name']}_id = ret.data[i].{e['name']};
                    if(ret{e['link_table']}Dao.retCode == 0) {{
                        std::vector<{e['link_table']}Dao::Entity>::iterator it =
                                find_if(ret{e['link_table']}Dao.data.begin(), ret{e['link_table']}Dao.data.end(),
                                        [cur_{e['name']}_id]({e['link_table']}Dao::Entity another) {{
                                        return another.id == cur_{e['name']}_id;}});
                        if(it != ret{e['link_table']}Dao.data.end()){{
                            ret.data[i].{e['name']}_name = it->name;
                        }}
                    }}'''
                        for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkTable$", linkTable)
    return funcCode


def genControllerCodeInfoList(tableName, operateInfo, genConfig):
    serviceTemplate = f'''
    // {operateInfo["table_name"]}列表查询
    void get{tableName}InfoList(
        {tableName}InfoListRet &_return, //返回内容
$inputParams$,
        const {tableName}OrderFields::type orderField,
        const OrderType::type orderType,
        const int32_t limitSize,
        const int32_t offset
    ){{
        try{{
            log_info("handler get{tableName}InfoList process start");
            {tableName}Service serviceObj;
            {tableName}Service::get{tableName}InfoListRet ret;
            serviceObj.get{tableName}InfoList(ret,$passParams$,
                                              static_cast<{tableName}Service::OrderFields>(orderField),
                                              static_cast<{tableName}Service::OrderType>(orderType),
                                              limitSize,offset);
            _return.retCode = ret.retCode;
            _return.retDesc = ret.retDesc;
            if(ret.retCode == 0){{
                for(auto dataItem: ret.data){{
                    {tableName}Entity e;
$retAssign$
$linkAssign$
                    _return.data.push_back(e);
                }}
                _return.dataTotal = _return.data.size();
            }}
        }}catch(std::exception & e){{
            log_error("ERROR in handler get{tableName}InfoList process:");
            log_error(e.what());
            _return.retCode = -2;
            _return.retDesc = e.what();
        }}
        log_info("handler get{tableName}InfoList process finish");
    }}
    '''
    inputParams = []
    outputInfos = []
    inputInfos = []
    for fieldInfo in operateInfo["fields"]:
        if fieldInfo['condition_type'] is not None:
            cfgType = fieldInfo['type']
            tType = trans2CppType(cfgType)
            note = ''
            assert  fieldInfo['condition_type'] in ['equal', 'range'], 'unsupported condition_type'
            if fieldInfo['condition_type'] in ['equal', 'range']:
                tType = f'const std::vector<{tType}> &';
                note = '// 传空列表示不对此条件做限制'
            inputParams.append(tab * 2 + f'{tType} {fieldInfo["name"]}, {note} ')
            fieldItem = {}
            fieldItem["name"] = fieldInfo["name"]
            inputInfos.append(fieldItem)
        if fieldInfo['list_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem["link_table"] = fieldInfo["link_table"]
            fieldItem["link_field"] = fieldInfo["link_field"]
            outputInfos.append(fieldItem)

    code = serviceTemplate.replace("$inputParams$", ',\n'.join(inputParams))

    passParams = ','.join([fieldItem["name"] for fieldItem in inputInfos]);
    code = code.replace("$passParams$", passParams)

    retAssign = n.join([tab * 5 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                        for i, e in enumerate(outputInfos)])
    code = code.replace("$retAssign$", retAssign)

    linkAssign = n.join([tab * 5 + f'e.{e["name"]}_{e["link_field"]} = dataItem.{e["name"]}_{e["link_field"]};' \
                         for i, e in enumerate(outputInfos) if e['link_table'] is not None])
    code = code.replace("$linkAssign$", linkAssign)
    return code


def trans2thriftType(cfgType):
    if cfgType in ['text', 'timestamp']:
        tType = 'string'
    elif cfgType == 'bool':
        tType = 'i32'
    elif cfgType == 'int8':
        tType = 'i64'
    else:
        assert False, 'Unsupported data type:' + cfgType
    return tType


def trans2CppType(cfgType):
    if cfgType in ['text', 'timestamp']:
        tType = 'std::string'
    elif cfgType == 'bool':
        tType = 'int'
    elif cfgType == 'int8':
        tType = 'int64_t'
    else:
        assert False, 'Unsupported data type:' + cfgType
    return tType


def genThriftCodeInfoList(tableName, operateInfo, genConfig):
    retType = f'''
    struct {tableName}InfoListRet{{
        1:i32 retCode,# 返回码，0正常，-2未知异常
        2:string retDesc,#返回描述
        3:i32 dataTotal, #数据总量
        4:list<{tableName}Entity> data #数据内容列表
    }}
    
    '''
    serviceTemplate = f'''
        # {operateInfo["table_name"]}列表查询
        {tableName}InfoListRet get{tableName}InfoList(
$inputParams$
        )
    '''

    inputParams = []
    idx = 1
    for fieldInfo in operateInfo["fields"]:
        if fieldInfo['condition_type'] is None:
            continue
        cfgType = fieldInfo['type']
        tType = trans2thriftType(cfgType)
        note = ''
        assert  fieldInfo['condition_type'] in ['equal', 'range'], 'unsupported condition_type'
        if fieldInfo['condition_type'] in ['equal', 'range']:
            tType = f'list<{tType}>';
            note = '# 传空列表示不对此条件做限制'
        inputParams.append(tab * 3 + f'{idx}:{tType} {fieldInfo["name"]} {note} ')
        idx += 1
    inputParams.append(tab * 3 + f'{idx + 0}:{tableName}OrderFields orderField #')
    inputParams.append(tab * 3 + f'{idx + 1}:OrderType orderType #')
    inputParams.append(tab * 3 + f'{idx + 2}:i32 limitSize #0~maxint,-1 返回所有')
    inputParams.append(tab * 3 + f'{idx + 3}:i32 offset #0~maxint')
    service = serviceTemplate.replace("$inputParams$", '\n'.join(inputParams))
    return retType, service


def genDaoCodeInfoDetail(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct get{tableName}InfoDetailRet{{
        int retCode;
        std::string retDesc;
        int dataTotal;
        std::vector<Entity> data;
    }};
    // {operateInfo["table_name"]}数据详情查询
    void get{tableName}InfoDetail(
        get{tableName}InfoDetailRet & ret,
        std::vector<std::string> ids,
        OrderFields orderField = OrderFields::insert_time, 
        OrderType orderType = OrderType::STAY
    ){{
        try {{
            log_info("Dao get{tableName}InfoDetail start");
            toUpperCase(ids);
            if(ids.size()==0){{
                ret.retCode = -1;
                ret.retDesc = "There should be at least one 'id' at parameter ids";
                ret.dataTotal = 0;
                log_info("get{tableName}InfoDetail finish");
                return;
            }}
            std::string conditionSqls;
            conditionSqls += sql_condition_gen<std::string>("equal",ids, "id");
            std::string sql = str(format("select $selectField$ from public.\\"{tableName}\\" \\n"
                                         "where  is_delete=false %1%order by %2% %3% ")
                                  % conditionSqls
                                  % OrderFieldsMap[orderField]
                                  % OrderTypeMap[orderType]);
            nanodbc::statement statement(*dbConn);
            log_info("Dao get{tableName}InfoDetail excuting sql:\\n" + sql);
            prepare(statement, sql);
            int i = 0;
            for (int j = 0; j < ids.size(); j++) {{
                statement.bind(i++, ids[j].c_str());
            }}
            nanodbc::result sqlResult = statement.execute(1, dbPool->sqlTimeout);
            map<std::string, Entity> resultMap;
            while (sqlResult.next()) {{
                Entity dataItem;
$dataItem$
                if(orderType == OrderType::STAY) {{
                    resultMap[dataItem.id] = dataItem;
                }}else{{
                    ret.data.push_back(dataItem);
                }}
            }}
            if(orderType == OrderType::STAY) {{
                for (auto id: ids) {{
                    if(resultMap.find(id) == resultMap.end())
                        continue;
                    ret.data.push_back(resultMap[id]);
                }}
            }}
            ret.retCode = 0;
            ret.retDesc = "success";
            ret.dataTotal = ret.data.size();
        }} catch (std::exception &e) {{
            log_error("Error in Dao get{tableName}InfoDetail");
            log_error(e.what());
            dbConn = dbPool->getConnection();
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("Dao get{tableName}InfoDetail finish");
    }}
    '''
    inputInfos = []
    outputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['condition_type'] is not None:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            if fieldInfo['condition_type'] in ["range", 'equal']:
                fieldItem['type'] = f'const std::vector<{trans2CppType(fieldInfo["type"])}> &'
                fieldItem['note'] = "指定范围的开始和结束" if fieldInfo['condition_type'] == "range" else "取值在此列表中"
            else:
                fieldItem['type'] = trans2CppType(fieldInfo['type'])
                fieldItem['note'] = "取值与此输入相等"
            inputInfos.append(fieldItem)
        if fieldInfo['detail_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo['type'])
            outputInfos.append(fieldItem)

    selectField = ','.join([f'\\"{e["name"]}\\"' \
                            for i, e in enumerate(outputInfos)])
    funcCode = funcTemplate.replace("$selectField$", selectField)

    dataItem = n.join([tab * 4 + f'dataItem.{e["name"]} = sqlResult.get<{e["rawType"]}>({i});' \
                       for i, e in enumerate(outputInfos)])
    funcCode = funcCode.replace("$dataItem$", dataItem)
    return funcCode


def genServiceCodeInfoDetail(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct get{tableName}InfoDetailRet{{
        int retCode;
        std::string retDesc;
        int dataTotal;
        std::vector<Entity> data;
    }};
    // {operateInfo["table_name"]}详情查询服务
    void get{tableName}InfoDetail(
        get{tableName}InfoDetailRet & ret,
        std::vector<std::string> ids,
        OrderFields orderField = OrderFields::insert_time, 
        OrderType orderType = OrderType::STAY
    ){{
        try {{
            log_info("service get{tableName}InfoDetail start");
            {tableName}Dao daoObj;
            {tableName}Dao::get{tableName}InfoDetailRet daoRet;
            daoObj.get{tableName}InfoDetail(daoRet, ids,
                                            static_cast<{tableName}Dao::OrderFields>(orderField),
                                            static_cast<{tableName}Dao::OrderType>(orderType));
            ret.retCode = daoRet.retCode;
            ret.retDesc = daoRet.retDesc;
$linkInit$
            if(daoRet.retCode == 0){{
                for(auto dataItem: daoRet.data){{
                    Entity e;
$retAssign$
$linkFillID$
                    ret.data.push_back(e);
                }}
$linkRet$
                for(int i = 0; i< ret.data.size(); i++){{
$linkTable$
                }}

                ret.dataTotal = ret.data.size();
            }}
        }} catch (std::exception &e) {{
            log_error("Error in service get{tableName}InfoDetail");
            log_error(e.what());
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("service get{tableName}InfoDetail finish");
    }}
    '''
    outputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['detail_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['link_table'] = fieldInfo['link_table']
            fieldItem['link_field'] = fieldInfo['link_field']
            fieldItem['rawType'] = trans2CppType(fieldInfo['type'])
            outputInfos.append(fieldItem)

    retAssign = n.join([tab * 5 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                        for i, e in enumerate(outputInfos)])
    funcCode = funcTemplate.replace("$retAssign$", retAssign)

    linkInit = n.join([tab*3 + f'''std::vector<std::string> {e['name']}_id;'''
                       for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkInit$", linkInit)

    linkFillID = n.join([tab*5 + f'''{e['name']}_id.push_back(e.{e['name']});'''
                         for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkFillID$", linkFillID)

    linkRet = n.join([tab*5 + f'''
                {e['link_table']}Dao dao{e['link_table']};
                {e['link_table']}Dao::get{e['link_table']}InfoDetailRet ret{e['link_table']}Dao;
                dao{e['link_table']}.get{e['link_table']}InfoDetail(ret{e['link_table']}Dao, {e['name']}_id);'''
                      for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkRet$", linkRet)

    linkTable = n.join([f'''
                    std::string cur_{e['name']}_id = ret.data[i].{e['name']};
                    if(ret{e['link_table']}Dao.retCode == 0) {{
                        std::vector<{e['link_table']}Dao::Entity>::iterator it =
                                find_if(ret{e['link_table']}Dao.data.begin(), ret{e['link_table']}Dao.data.end(),
                                        [cur_{e['name']}_id]({e['link_table']}Dao::Entity another) {{
                                        return another.id == cur_{e['name']}_id;}});
                        if(it != ret{e['link_table']}Dao.data.end()){{
                            ret.data[i].{e['name']}_name = it->name;
                        }}
                    }}'''
                        for e in outputInfos if e['link_table'] is not None])
    funcCode = funcCode.replace("$linkTable$", linkTable)

    return funcCode


def genControllerCodeInfoDetail(tableName, operateInfo, genConfig):
    serviceTemplate = f'''
    // {operateInfo["table_name"]}列表查询
    void get{tableName}InfoDetail(
        {tableName}InfoDetailRet &_return, //返回内容
        const std::vector<std::string> & ids,
        const {tableName}OrderFields::type orderField,
        const OrderType::type orderType
    ){{
        try{{
            log_info("handler get{tableName}InfoDetail process start");
            {tableName}Service serviceObj;
            {tableName}Service::get{tableName}InfoDetailRet ret;
            serviceObj.get{tableName}InfoDetail(ret,ids,
                                              static_cast<{tableName}Service::OrderFields>(orderField),
                                              static_cast<{tableName}Service::OrderType>(orderType));
            _return.retCode = ret.retCode;
            _return.retDesc = ret.retDesc;
            if(ret.retCode == 0){{
                for(auto dataItem: ret.data){{
                    {tableName}Entity e;
$retAssign$
$linkAssign$
                    _return.data.push_back(e);
                }}
                _return.dataTotal = _return.data.size();
            }}
        }}catch(std::exception & e){{
            log_error("ERROR in handler get{tableName}InfoDetail process:");
            log_error(e.what());
            _return.retCode = -2;
            _return.retDesc = e.what();
        }}
        log_info("handler get{tableName}InfoDetail process finish");
    }}
    '''
    inputParams = []
    outputInfos = []
    inputInfos = []
    for fieldInfo in operateInfo["fields"]:
        if fieldInfo['condition_type'] is not None:
            cfgType = fieldInfo['type']
            tType = trans2CppType(cfgType)
            note = ''
            assert  fieldInfo['condition_type'] in ['equal', 'range'], 'unsupported condition_type'
            if fieldInfo['condition_type'] in ['equal', 'range']:
                tType = f'const std::vector<{tType}> &';
                note = '// 传空列表示不对此条件做限制'
            inputParams.append(tab * 2 + f'{tType} {fieldInfo["name"]}, {note} ')
            fieldItem = {}
            fieldItem["name"] = fieldInfo["name"]
            inputInfos.append(fieldItem)
        if fieldInfo['detail_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem["link_table"] = fieldInfo["link_table"]
            fieldItem["link_field"] = fieldInfo["link_field"]
            outputInfos.append(fieldItem)

    code = serviceTemplate.replace("$inputParams$", ',\n'.join(inputParams))

    passParams = ','.join([fieldItem["name"] for fieldItem in inputInfos]);
    code = code.replace("$passParams$", passParams)

    retAssign = n.join([tab * 5 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                        for i, e in enumerate(outputInfos)])
    code = code.replace("$retAssign$", retAssign)

    linkAssign = n.join([tab * 5 + f'e.{e["name"]}_{e["link_field"]} = dataItem.{e["name"]}_{e["link_field"]};' \
                         for i, e in enumerate(outputInfos) if e['link_table'] is not None])
    code = code.replace("$linkAssign$", linkAssign)
    return code


def genThriftCodeInfoDetail(tableName, operateInfo, genConfig):
    retType = f'''
    struct {tableName}InfoDetailRet{{
        1:i32 retCode,# 返回码，0正常，-2未知异常
        2:string retDesc,#返回描述
        3:i32 dataTotal, #数据总量
        4:list<{tableName}Entity> data #数据内容列表
    }}
    '''
    serviceTemplate = f'''
        # {operateInfo["table_name"]}详情查询
        {tableName}InfoDetailRet get{tableName}InfoDetail(
$inputParams$
        )
    '''
    inputParams = []
    inputParams.append(tab * 3 + f'1:list<string> ids # data id')
    inputParams.append(tab * 3 + f'2:{tableName}OrderFields orderField #')
    inputParams.append(tab * 3 + f'3:OrderType orderType # order type')
    service = serviceTemplate.replace("$inputParams$", '\n'.join(inputParams))
    return retType, service


def genDaoCodeInsert(tableName, operateInfo, genConfig):
    template = f'''
    struct insert{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据插入
    void insert{tableName}(
        insert{tableName}Ret &ret,
        const std::vector<Entity>& datas
    ) {{
        try {{
            log_info("Dao insert{tableName} start");
            int batchSize = datas.size();
            if(batchSize <=0) {{
                ret.retCode = -1;
                ret.retDesc = "The batchSize of data equals to 0.";
                return;
            }}
            std::vector<std::string> id;
$inputParam$
            for(auto dataItem:datas){{
                std::string idStr;
                if(dataItem.id == ""){{
                    idStr = getUUID(1)[0];
                }}else{{
                    idStr = dataItem.id;
                }}
                toUpperCase(idStr);
                id.push_back(idStr);
$fetchField$
            }}
            std::string sql = str(format("insert into public.\\"{tableName}\\"(\\"id\\", $insertFields$)\\n"
                                         "values (?, $insertPlace$)\\n"));
            nanodbc::statement statement(*dbConn);
            log_info("Dao insert{tableName} excuting sql:\\n" + sql);
            prepare(statement, sql);
            int i = 0;
            statement.bind_strings(i++,id);
$insertBind$
            transact(statement,batchSize);
            ret.retCode = 0;
            ret.retDesc = "success";
        }} catch (std::exception &e) {{
            log_error("Error in Dao insert{tableName}");
            log_error(e.what());
            dbConn = dbPool->getConnection();
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("Dao insert{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['type'] = f'std::vector<{trans2CppType(fieldInfo["type"])}>'
            inputInfos.append(fieldItem)
    assert len(inputInfos) > 0, "insert operation has no input field"
    inputParam = n.join([tab * 3 + f'{e["type"]} {e["name"]};' \
                         for e in inputInfos if e["name"] != 'id']);
    code = template.replace('$inputParam$', inputParam)

    fetchField = n.join([tab * 4 + f'{e["name"]}.push_back(dataItem.{e["name"]});'
                         for e in inputInfos if e["name"] != 'id'])
    code = code.replace('$fetchField$', fetchField)

    batchSizeJudge = tab * 3 + f'int batchSize = std::max({{{",".join([e["name"] + ".size()" for e in inputInfos])}}});'
    batchSizeJudge += f'''
            if({'||'.join([f'{e["name"]}.size() != batchSize' for e in inputInfos])}||batchSize==0) {{
                ret.retCode = -1;
                ret.retDesc = "length of insert fields is not equal or the batchSize equals to 0.";
                return;
            }}
    '''
    code = code.replace("$batchSizeJudge$", batchSizeJudge)

    insertFields = ','.join([f'\\"{e["name"]}\\"' for e in inputInfos if e["name"] != 'id'])
    insertPlace = ','.join(['?' for e in inputInfos if e["name"] != 'id'])
    code = code.replace("$insertFields$", insertFields)
    code = code.replace("$insertPlace$", insertPlace)

    insertBind = n.join([tab * 3 + f'statement.bind_strings(i++,{e["name"]});' if e['rawType'] == "std::string"
                         else f'statement.bind(i++, {e["name"]}.data(), batchSize);'
                         for i, e in enumerate(inputInfos) if e["name"] != 'id'])
    code = code.replace("$insertBind$", insertBind)

    return code


def genServiceCodeInsert(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct insert{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据新增服务
    void insert{tableName}(
        insert{tableName}Ret &ret,
        const std::vector<Entity>& datas
    ) {{
        try {{
            log_info("service insert{tableName} start");
            {tableName}Dao daoObj;
            {tableName}Dao::insert{tableName}Ret daoRet;
            std::vector<{tableName}Dao::Entity> daoDatas;
            for(auto dataItem:datas){{
                {tableName}Dao::Entity e;
$transInput$
                daoDatas.push_back(e);
            }}
            daoObj.insert{tableName}(daoRet, daoDatas);
            ret.retCode = daoRet.retCode;
            ret.retDesc = daoRet.retDesc;
        }} catch (std::exception &e) {{
            log_error("Error in service insert{tableName}");
            log_error(e.what());
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("service insert{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            inputInfos.append(fieldItem)

    transInput = n.join([tab * 4 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                         for i, e in enumerate(inputInfos)])
    code = funcTemplate.replace('$transInput$', transInput)

    return code


def genControllerCodeInsert(tableName, operateInfo, genConfig):
    serviceTemplate = f'''
    // {operateInfo["table_name"]}数据新增
    void insert{tableName}(
        {tableName}InsertRet &_return, //返回内容
        const std::vector<{tableName}Entity> & datas
    ){{
        try{{
            log_info("handler insert{tableName} process start");
            {tableName}Service srvObj;
            {tableName}Service::insert{tableName}Ret srvRet;
            std::vector<{tableName}Service::Entity> srvDatas;
            for(auto dataItem:datas){{
                {tableName}Service::Entity e;
$transInput$
                srvDatas.push_back(e);
            }}
            srvObj.insert{tableName}(srvRet, srvDatas);
            _return.retCode = srvRet.retCode;
            _return.retDesc = srvRet.retDesc;
        }}catch(std::exception & e){{
            log_error("ERROR in handler insert{tableName} process:");
            log_error(e.what());
            _return.retCode = -2;
            _return.retDesc = e.what();
        }}
        log_info("handler insert{tableName} process finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            inputInfos.append(fieldItem)

    transInput = n.join([tab * 4 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                         for i, e in enumerate(inputInfos)])
    code = serviceTemplate.replace('$transInput$', transInput)
    return code


def genThriftCodeInsert(tableName, operateInfo, genConfig):
    retType = f'''
    struct {tableName}InsertRet{{
        1:i32 retCode,# 返回码，0正常，-2未知异常
        2:string retDesc,#返回描述
    }}
    '''
    service = f'''
        # {operateInfo["table_name"]}数据插入
        {tableName}InsertRet insert{tableName}(
            1:list<{tableName}Entity> datas
        )
    '''
    return retType, service


def genDaoCodeUpdate(tableName, operateInfo, genConfig):
    template = f'''
    struct update{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据更新
    void update{tableName}(
        update{tableName}Ret &ret,
        const std::vector<Entity>& datas
    ) {{
        try {{
            log_info("Dao update{tableName} start");
            int totalSize = datas.size();
            if(totalSize <=0) {{
                ret.retCode = -1;
                ret.retDesc = "The batchSize of data equals to 0.";
                return;
            }}
            nanodbc::statement statement(*dbConn);
            for(auto dataItem:datas){{
                if(dataItem.id == ""){{
                    ret.retCode = -3;
                    ret.retDesc = "data id should not be empty in update method.";
                    return;
                }}
                std::vector<std::string> id = {{dataItem.id}};
                std::string conditionSqls = sql_condition_gen<std::string>("equal",id, "id");

                std::string sql = str(format("update \\"{tableName}\\" set\\n"
$updateField$
                                             "where is_delete=false %1%") % conditionSqls);
                log_info("Dao update{tableName} excuting sql:\\n" + sql);
                prepare(statement, sql);
                int i = 0;
$updateBind$
                statement.bind(i++, dataItem.id.c_str());
                statement.execute(1, dbPool->sqlTimeout);
            }}
            ret.retCode = 0;
            ret.retDesc = "success";
        }} catch (std::exception &e) {{
            log_error("Error in Dao update{tableName}");
            log_error(e.what());
            dbConn = dbPool->getConnection();
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("Dao update{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['type'] = f'std::vector<{trans2CppType(fieldInfo["type"])}>'
            inputInfos.append(fieldItem)
    assert len(inputInfos) > 0, "insert operation has no input field"

    updateField = '\n'.join([tab * 11 + f'"\\"{e["name"]}\\" = ?$\\n"'
                             for i, e in enumerate(inputInfos)])
    updateField = updateField.replace('$', ',', len(inputInfos) - 1)
    updateField = updateField.replace('$', '', 1)
    code = template.replace("$updateField$", updateField)

    updateBind = n.join([
        tab * 4 + f'''statement.bind(i++, {f'dataItem.{e["name"]}.c_str()' if e['rawType'] == 'std::string' else f'&dataItem.{e["name"]}'});'''
        for i, e in enumerate(inputInfos)])
    code = code.replace("$updateBind$", updateBind)

    return code


def genServiceCodeUpdate(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct update{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据更新服务
    void update{tableName}(
        update{tableName}Ret &ret,
        const std::vector<Entity>& datas
    ) {{
        try {{
            log_info("service update{tableName} start");
            {tableName}Dao daoObj;
            {tableName}Dao::update{tableName}Ret daoRet;
            std::vector<{tableName}Dao::Entity> daoDatas;
            for(auto dataItem:datas){{
                {tableName}Dao::Entity e;
                e.id = dataItem.id;
$transInput$
                daoDatas.push_back(e);
            }}
            daoObj.update{tableName}(daoRet, daoDatas);
            ret.retCode = daoRet.retCode;
            ret.retDesc = daoRet.retDesc;
        }} catch (std::exception &e) {{
            log_error("Error in service update{tableName}");
            log_error(e.what());
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("service update{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            inputInfos.append(fieldItem)

    transInput = n.join([tab * 4 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                         for i, e in enumerate(inputInfos)])
    code = funcTemplate.replace('$transInput$', transInput)

    return code


def genControllerCodeUpdate(tableName, operateInfo, genConfig):
    serviceTemplate = f'''
    // {operateInfo["table_name"]}数据更新
    void update{tableName}(
        {tableName}UpdateRet &_return, //返回内容
        const std::vector<{tableName}Entity> & datas
    ){{
        try{{
            log_info("handler update{tableName} process start");
            {tableName}Service srvObj;
            {tableName}Service::update{tableName}Ret srvRet;
            std::vector<{tableName}Service::Entity> srvDatas;
            for(auto dataItem:datas){{
                {tableName}Service::Entity e;
                e.id = dataItem.id;
$transInput$
                srvDatas.push_back(e);
            }}
            srvObj.update{tableName}(srvRet, srvDatas);
            _return.retCode = srvRet.retCode;
            _return.retDesc = srvRet.retDesc;
        }}catch(std::exception & e){{
            log_error("ERROR in handler update{tableName} process:");
            log_error(e.what());
            _return.retCode = -2;
            _return.retDesc = e.what();
        }}
        log_info("handler update{tableName} process finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['in_up_param']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            inputInfos.append(fieldItem)

    transInput = n.join([tab * 4 + f'e.{e["name"]} = dataItem.{e["name"]};' \
                         for i, e in enumerate(inputInfos)])
    code = serviceTemplate.replace('$transInput$', transInput)
    return code


def genThriftCodeUpdate(tableName, operateInfo, genConfig):
    retType = f'''
    struct {tableName}UpdateRet{{
        1:i32 retCode,# 返回码，0正常，-2未知异常
        2:string retDesc,#返回描述
    }}
    '''
    service = f'''
        # {operateInfo["table_name"]}数据更新
        {tableName}UpdateRet update{tableName}(
            1:list<{tableName}Entity> datas
        )
    '''
    return retType, service


def genDaoCodeDelete(tableName, operateInfo, genConfig):
    template = f'''
    struct delete{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据删除
    void delete{tableName}(
        delete{tableName}Ret &ret,
        vector<std::string> id,
$inputParam$
    ) {{
        try {{
            log_info("Dao delete{tableName} start");
            toUpperCase(id);
            std::string conditionSqls;
            conditionSqls += sql_condition_gen<std::string>("equal",id, "id");
$SQLCondition$
            std::string curTime = getCurTimestr();
            std::string sql = str(format("update public.\\"{tableName}\\" set\\n"
                                         "is_delete = true, delete_time='%1%'\\n"
                                         "where 1=1 %2%\\n")%curTime%conditionSqls);
            nanodbc::statement statement(*dbConn);
            log_info("Dao delete{tableName} excuting sql:\\n" + sql);
            prepare(statement, sql);
            int i = 0;
            for (int j = 0; j < id.size(); j++) {{
                statement.bind(i++, id[j].c_str());
            }}
$deleteBind$
            nanodbc::result sqlResult = statement.execute(1, dbPool->sqlTimeout);
            ret.retCode = 0;
            ret.retDesc = "success";
        }} catch (std::exception &e) {{
            log_error("Error in Dao delete{tableName}");
            log_error(e.what());
            dbConn = dbPool->getConnection();
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("Dao delete{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['condition_type'] is not None:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            if fieldInfo['condition_type'] in ["range", 'equal']:
                fieldItem['type'] = f'const std::vector<{trans2CppType(fieldInfo["type"])}> &'
                fieldItem['note'] = "指定范围的开始和结束" if fieldInfo['condition_type'] == "range" else "取值在此列表中"
            else:
                fieldItem['type'] = trans2CppType(fieldInfo['type'])
                fieldItem['note'] = "取值与此输入相等"
            inputInfos.append(fieldItem)
    assert len(inputInfos) > 0, "DELETE operation has no input field"
    inputParam = n.join([tab * 2 + f'{fieldItem["type"]} {fieldItem["name"]}$// {fieldItem["note"]}' \
                         for fieldItem in inputInfos]);
    inputParam = inputParam.replace('$', ',', len(inputInfos) - 1)
    inputParam = inputParam.replace('$', '')
    code = template.replace('$inputParam$', inputParam)

    SQLCondition = n.join([f'''
            if({e['name']}.size() != 2)
                throw std::exception("range input parameter {e['name']} should be have size of 2");
    '''
    for e in inputInfos if e['condition_type'] == 'range'])
    SQLCondition += n.join([
        tab * 3 + f'conditionSqls += sql_condition_gen<{e["rawType"]}>("{e["condition_type"]}", {e["name"]}, "{e["name"]}");' \
        for e in inputInfos])
    code = code.replace("$SQLCondition$", SQLCondition)

    deleteBind = ''
    for inputItem in inputInfos:
        if inputItem["rawType"] == "std::string":
            bindExp = f'statement.bind(i++, {inputItem["name"]}[j].c_str());'
        else:
            bindExp = f'statement.bind(i++, &{inputItem["name"]}[j]);'
        deleteBind += f'''
            for (int j = 0; j < {inputItem["name"]}.size(); j++) {{
                {bindExp}
            }}
        '''
    code = code.replace("$deleteBind$", deleteBind)

    return code


def genServiceCodeDelete(tableName, operateInfo, genConfig):
    funcTemplate = f'''
    struct delete{tableName}Ret{{
        int retCode;
        std::string retDesc;
    }};
    // {operateInfo["table_name"]}数据删除
    void delete{tableName}(
        delete{tableName}Ret &ret,
        vector<std::string> id,
$inputParam$
    ) {{
        try {{
            log_info("service delete{tableName} start");
            {tableName}Dao daoObj;
            {tableName}Dao::delete{tableName}Ret daoRet;
            daoObj.delete{tableName}(daoRet, id, $passParams$);
            ret.retCode = daoRet.retCode;
            ret.retDesc = daoRet.retDesc;
        }} catch (std::exception &e) {{
            log_error("Error in service delete{tableName}");
            log_error(e.what());
            ret.retCode = -2;
            ret.retDesc = e.what();
        }}
        log_info("service delete{tableName} finish");
    }}
    '''
    inputInfos = []
    for fieldInfo in operateInfo['fields']:
        if fieldInfo['condition_type'] is not None:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['rawType'] = trans2CppType(fieldInfo["type"])
            fieldItem['condition_type'] = fieldInfo['condition_type']
            if fieldInfo['condition_type'] in ["range", 'equal']:
                fieldItem['type'] = f'const std::vector<{trans2CppType(fieldInfo["type"])}> &'
                fieldItem['note'] = "指定范围的开始和结束" if fieldInfo['condition_type'] == "range" else "取值在此列表中"
            else:
                fieldItem['type'] = trans2CppType(fieldInfo['type'])
                fieldItem['note'] = "取值与此输入相等"
            inputInfos.append(fieldItem)

    inputParam = n.join([tab * 2 + f'{fieldItem["type"]} {fieldItem["name"]}$// {fieldItem["note"]}' \
                         for fieldItem in inputInfos]);
    inputParam = inputParam.replace('$', ',', len(inputInfos) - 1)
    inputParam = inputParam.replace('$', '')
    code = funcTemplate.replace('$inputParam$', inputParam)

    passParams = ','.join([fieldItem["name"] for fieldItem in inputInfos]);
    code = code.replace("$passParams$", passParams)

    return code


def genControllerCodeDelete(tableName, operateInfo, genConfig):
    serviceTemplate = f'''
    // {operateInfo["table_name"]}数据删除
    void delete{tableName}(
        {tableName}DeleteRet &_return, //返回内容
        const std::vector<std::string> & id,//待删除数据ID，为空则不根据ID删除
$inputParams$
    ){{
        try{{
            log_info("handler delete{tableName}InfoList process start");
            {tableName}Service serviceObj;
            {tableName}Service::delete{tableName}Ret ret;
            serviceObj.delete{tableName}(ret,id, $passParams$);
            _return.retCode = ret.retCode;
            _return.retDesc = ret.retDesc;
        }}catch(std::exception & e){{
            log_error("ERROR in handler delete{tableName} process:");
            log_error(e.what());
            _return.retCode = -2;
            _return.retDesc = e.what();
        }}
        log_info("handler delete{tableName} process finish");
    }}
    '''
    inputParams = []
    outputInfos = []
    inputInfos = []
    for fieldInfo in operateInfo["fields"]:
        if fieldInfo['condition_type'] is not None:
            cfgType = fieldInfo['type']
            tType = trans2CppType(cfgType)
            note = ''
            assert  fieldInfo['condition_type'] in ['equal', 'range'], 'unsupported condition_type'
            if fieldInfo['condition_type'] in ['equal', 'range']:
                tType = f'const std::vector<{tType}> &';
                note = '// 传空列表示不对此条件做限制'
            inputParams.append(tab * 2 + f'{tType} {fieldInfo["name"]}$ {note} ')
            fieldItem = {}
            fieldItem["name"] = fieldInfo["name"]
            inputInfos.append(fieldItem)
        if fieldInfo['list_return']:
            fieldItem = {}
            fieldItem['name'] = fieldInfo['name']
            fieldItem['link_table'] = fieldInfo['link_table']
            fieldItem['link_field'] = fieldInfo['link_field']
            fieldItem['rawType'] = trans2CppType(fieldInfo['type'])
            outputInfos.append(fieldItem)

    code = serviceTemplate.replace("$inputParams$", '\n'.join(inputParams).replace('$',',',len(inputParams)-1).replace('$',''))

    passParams = ','.join([fieldItem["name"] for fieldItem in inputInfos]);
    code = code.replace("$passParams$", passParams)

    return code


def genThriftCodeDelete(tableName, operateInfo, genConfig):
    retType = f'''
    struct {tableName}DeleteRet{{
        1:i32 retCode,# 返回码，0正常，-2未知异常
        2:string retDesc,#返回描述
    }}
    '''
    serviceTemplate = f'''
        # {operateInfo["table_name"]}数据删除
        {tableName}DeleteRet delete{tableName}(
$inputParams$
        )
    '''
    inputParams = []
    inputParams.append(tab * 3 + f'1:list<string> id # 待删除数据id，为空表示不根据此字段筛选 ')
    idx = 2
    for fieldInfo in operateInfo["fields"]:
        if fieldInfo['condition_type'] is None:
            continue
        tType = trans2thriftType(fieldInfo['type'])
        assert  fieldInfo['condition_type'] in ['equal', 'range'], 'unsupported condition_type'
        if fieldInfo['condition_type'] in ['equal', 'range']:
            tType = f'list<{tType}>';
            note = '# 过滤字段，列表为空表示不根据此字段过滤'
        inputParams.append(tab * 3 + f'{idx}:{tType} {fieldInfo["name"]} {note} ')
        idx += 1
    service = serviceTemplate.replace('$inputParams$', '\n'.join(inputParams))
    return retType, service


def genThriftCodeEntity(tableName, operateInfo):
    allFields = operateInfo['fields']
    eFields = []
    orderFields = []
    idx = 1
    for field in allFields:
        if field['order']:
            orderFields.append(tab * 2 + f'{field["name"]}')
        if field["detail_return"] or field["list_return"]:
            tType = trans2thriftType(field['type'])
            eFields.append(tab * 2 + f'{idx}:{tType} {field["name"]}')
            idx += 1
            if field["link_table"] is not None:
                eFields.append(tab * 2 + f'{idx}:{tType} {field["name"]}_{field["link_field"]}')
                idx += 1
    n = '\n'
    entityCode = f'''
    struct {tableName}Entity{{
{n.join(eFields)}
    }}
    enum {tableName}OrderFields {{
{n.join(orderFields)}
    }}
    '''
    return entityCode


def genDaoCodeEntity(tableName, operateInfo):
    allFields = operateInfo['fields']
    eFields = []
    orderFields = []
    orderFieldsMap = []
    idx = 1
    for field in allFields:
        if field['order']:
            orderFields.append(tab * 3 + f'{field["name"]}')
            orderFieldsMap.append(tab * 3 + f'{{OrderFields::{field["name"]}, "{field["name"]}"}}')
        if field["detail_return"] or field["list_return"]:
            tType = trans2CppType(field['type'])
            if field['in_up_param']:
                note = "//used in insert or update method"
            else:
                note = ''
            eFields.append(tab * 3 + f'{tType} {field["name"]};{note}')
            idx += 1
    n = '\n'
    entityCode = f'''
    struct Entity{{
{n.join(eFields)}
    }};
    enum OrderFields {{
{(',' + n).join(orderFields)}
    }};
    map<int, std::string> OrderFieldsMap = {{
{(',' + n).join(orderFieldsMap)}
    }};
    '''
    return entityCode


def genServiceCodeEntity(tableName, operateInfo):
    allFields = operateInfo['fields']
    eFields = []
    orderFields = []
    orderFieldsMap = []
    linkTables = set()
    idx = 1
    for field in allFields:
        if field['order']:
            orderFields.append(tab * 3 + f'{field["name"]}')
            orderFieldsMap.append(tab * 3 + f'{{OrderFields::{field["name"]}, "{field["name"]}"}}')
        if field["detail_return"] or field["list_return"]:
            tType = trans2CppType(field['type'])
            if field['in_up_param']:
                note = "//used in insert or update method"
            else:
                note = ''
            eFields.append(tab * 3 + f'{tType} {field["name"]};{note}')
            if field["link_table"] is not None:
                eFields.append(tab * 3 + f'{tType} {field["name"]}_{field["link_field"]};')
                linkTables.add(field["link_table"])
            idx += 1
    n = '\n'
    entityCode = f'''
    struct Entity{{
{n.join(eFields)}
    }};
    enum OrderFields {{
{(',' + n).join(orderFields)}
    }};
    map<int, std::string> OrderFieldsMap = {{
{(',' + n).join(orderFieldsMap)}
    }};
    '''
    return entityCode, linkTables


def genThriftCode(dataInfo, genConfig):
    if not genConfig['thrift']['enable']:
        return
    thriftCodeTemplate = f'''
namespace cpp {genConfig['thrift']['namespace']}
    enum OrderType{{
        ASC,
        DESC,
        STAY
    }}
$entityTypes$
$retTypes$    
    
    service {genConfig['thrift']['service_name']}{{
$thriftServices$
    }}
    '''
    entityTypes = [];
    retTypes = [];
    thriftServices = [];
    for tableName, operateInfo in dataInfo.items():
        print("talbe name:", tableName)
        entityTypes.append(genThriftCodeEntity(tableName, operateInfo));
        accessTypes = operateInfo["access_type"]
        for accessType in accessTypes:
            access_name, asService = accessType.values()
            if not asService:
                continue
            if access_name == "info_list":
                retType, service = genThriftCodeInfoList(tableName, operateInfo, genConfig);
            elif access_name == "info_detail":
                retType, service = genThriftCodeInfoDetail(tableName, operateInfo, genConfig);
            elif access_name == "insert":
                retType, service = genThriftCodeInsert(tableName, operateInfo, genConfig);
            elif access_name == "update":
                retType, service = genThriftCodeUpdate(tableName, operateInfo, genConfig);
            elif access_name == "delete":
                retType, service = genThriftCodeDelete(tableName, operateInfo, genConfig);
            else:
                continue
            retTypes.append(retType)
            thriftServices.append(service)
    thriftCode = thriftCodeTemplate.replace("$entityTypes$", '\n'.join(entityTypes)). \
        replace("$retTypes$", '\n'.join(retTypes)). \
        replace("$thriftServices$", '\n'.join(thriftServices))
    save_dir = genConfig['thrift']['save_path']
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    with open(save_dir + f'/{genConfig["thrift"]["service_name"]}.thrift', 'w', encoding='utf-8') as f:
        f.write(thriftCode)

    cmd =f' "{genConfig["thrift"]["cmd_path"]}"" -gen cpp -o "{genConfig["thrift"]["save_path"]}" "{genConfig["thrift"]["save_path"]}/{genConfig["thrift"]["service_name"]}.thrift" '
    print("thrift gen CMD:"+cmd)
    os.system(cmd)


def genDaoCode(dataInfo, genConfig):
    if not genConfig['dao']['enable']:
        return
    save_dir = genConfig['dao']['save_path']
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # each table a Dao file
    for tableName, operateInfo in dataInfo.items():
        func_codes = []
        accessTypes = operateInfo["access_type"]
        for accessType in accessTypes:
            access_name, asService = accessType.values()
            if access_name == "info_list":
                func_code = genDaoCodeInfoList(tableName, operateInfo, genConfig);
            elif access_name == "info_detail":
                func_code = genDaoCodeInfoDetail(tableName, operateInfo, genConfig);
            elif access_name == "insert":
                func_code = genDaoCodeInsert(tableName, operateInfo, genConfig);
            elif access_name == "update":
                func_code = genDaoCodeUpdate(tableName, operateInfo, genConfig);
            elif access_name == "delete":
                func_code = genDaoCodeDelete(tableName, operateInfo, genConfig);
            else:
                continue
            func_codes.append(func_code)
        entity = genDaoCodeEntity(tableName, operateInfo)
        n = '\n'
        daoCode = f'''
#ifndef {tableName}DAO_HPP
#define {tableName}DAO_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <mutex>
#include <thread>
#include <algorithm>
#include <map>

#include <boost/format.hpp>
#include <inicpp.h>


#include "common/EasyLogger.hpp"
#include "common/utils.hpp"
#include "nanodbc.h"
#include "dao/DataAccessor.hpp"

class {tableName}Dao: public DataAccessor{{
public:
{entity}
    {tableName}Dao(){{
    }}
{n.join(func_codes)}
private:
    int timeout;
    
}};
#endif
        '''
        with open(save_dir + f'/{tableName}Dao.hpp', 'w', encoding='utf-8') as of:
            of.write(daoCode)


def genServiceCode(dataInfo, genConfig):
    if not genConfig['service']['enable']:
        return
    save_dir = genConfig['service']['save_path']
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # each table a Dao file
    for tableName, operateInfo in dataInfo.items():
        func_codes = []
        accessTypes = operateInfo["access_type"]

        for accessType in accessTypes:
            access_name, asService = accessType.values()
            if access_name == "info_list":
                func_code = genServiceCodeInfoList(tableName, operateInfo, genConfig);
            elif access_name == "info_detail":
                func_code = genServiceCodeInfoDetail(tableName, operateInfo, genConfig);
            elif access_name == "insert":
                func_code = genServiceCodeInsert(tableName, operateInfo, genConfig);
            elif access_name == "update":
                func_code = genServiceCodeUpdate(tableName, operateInfo, genConfig);
            elif access_name == "delete":
                func_code = genServiceCodeDelete(tableName, operateInfo, genConfig);
            else:
                continue
            func_codes.append(func_code)
        entity, linkTables = genServiceCodeEntity(tableName, operateInfo)
        n = '\n'
        daoCode = f'''
#ifndef {tableName}SERVICE_HPP
#define {tableName}SERVICE_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <mutex>
#include <thread>
#include <algorithm>
#include <map>

#include <boost/format.hpp>
#include <inicpp.h>


#include "common/EasyLogger.hpp"
#include "common/utils.hpp"
#include "service/BaseService.hpp"
#include "dao/{tableName}Dao.hpp"
{n.join([f'#include "dao/{tName}Dao.hpp"' for tName in linkTables])}

class {tableName}Service: public BaseService{{
public:
{entity}
    {tableName}Service(){{
    }}
{n.join(func_codes)}
    
}};
#endif
        '''
        with open(save_dir + f'/{tableName}Service.hpp', 'w', encoding='utf-8') as of:
            of.write(daoCode)


def genControllerCode(dataInfo, genConfig):
    if not genConfig['controller']['enable']:
        return
    controllerName = genConfig['controller']['controller_name']
    thriftName = genConfig['thrift']['service_name']
    thriftCodeTemplate = f'''
#ifndef {controllerName}CONTROLLER_HPP
#define {controllerName}CONTROLLER_HPP


#include "{thriftName}.h"

$inlcudeService$


using namespace  ::{genConfig['thrift']['namespace'].replace('.', '::')};

class {thriftName}Handler : virtual public {thriftName}If {{
    public:
    {thriftName}Handler() {{
    // Your initialization goes here
    }}

$methods$

}};
#endif
    '''
    inlcudeService = [];
    methods = [];
    for tableName, operateInfo in dataInfo.items():
        print("talbe name:", tableName)
        inlcudeService.append(f'#include "service/{tableName}Service.hpp"');
        accessTypes = operateInfo["access_type"]
        for accessType in accessTypes:
            access_name, asService = accessType.values()
            if not asService:
                continue
            if access_name == "info_list":
                method = genControllerCodeInfoList(tableName, operateInfo, genConfig);
            elif access_name == "info_detail":
                method = genControllerCodeInfoDetail(tableName, operateInfo, genConfig);
            elif access_name == "insert":
                method = genControllerCodeInsert(tableName, operateInfo, genConfig);
            elif access_name == "update":
                method = genControllerCodeUpdate(tableName, operateInfo, genConfig);
            elif access_name == "delete":
                method = genControllerCodeDelete(tableName, operateInfo, genConfig);
            else:
                continue
            methods.append(method)
    controllerCode = thriftCodeTemplate.replace("$inlcudeService$", '\n'.join(inlcudeService)). \
        replace("$methods$", '\n'.join(methods))
    save_dir = genConfig['controller']['save_path']
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    with open(save_dir + f'/{genConfig["controller"]["controller_name"]}Controller.hpp', 'w', encoding='utf-8') as f:
        f.write(controllerCode)

def genApplicationCodeThreadPool(dataInfo, genConfig):
    code = f'''
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TSocket.h>
#include <thrift/concurrency/ThreadManager.h>
#include <thrift/server/TThreadPoolServer.h>
#include <boost/format.hpp>

#include "controller/AddrEventHandler.hpp"
#include "controller/{genConfig['application']['application_name']}Controller.hpp"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;
using namespace ::apache::thrift::concurrency;

int main(int argc, char **argv) {{
    std::string configPathRaw = "config/applicationConfig.ini";
    std::string configPath = findTargetFile(configPathRaw);
    if(configPath == ""){{
        log_error("----ERROR: can not find config file at "+ configPathRaw);
        return -1;
    }}
    ini::IniFile config;
    config.load(configPath);
    std::string IP = config["ADDRESS"]["ServiceIP"].as<std::string>();
    int port = config["ADDRESS"]["ServicePort"].as<int>();
    int workerCnt = config["RUMTIME"]["workerCnt"].as<int>();
    if(IP=="" || port == 0 || workerCnt == 0){{
        log_error("failed to read configuration correctly");
        log_error("loaded configuration:");
        log_error(str(format("[ip=%1%, port=%2%, workerCnt]...")%IP%port%workerCnt));
        return -1;
    }}
    
    ::std::shared_ptr<{genConfig['controller']['controller_name']}Handler> handler(new {genConfig['controller']['controller_name']}Handler());
    ::std::shared_ptr<TProcessor> processor(new {genConfig['controller']['controller_name']}Processor(handler));
    ::std::shared_ptr<TServerTransport> serverTransport(new TServerSocket(IP, port));
    ::std::shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
    ::std::shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

    ::std::shared_ptr<ThreadManager> threadManager = ThreadManager::newSimpleThreadManager(workerCnt);
    ::std::shared_ptr<ThreadFactory> threadFactory = ::std::shared_ptr<ThreadFactory>(new ThreadFactory);
    threadManager->threadFactory(threadFactory);
    threadManager->start();
    TThreadPoolServer server(processor, serverTransport, transportFactory, protocolFactory, threadManager);
    log_info(str(format("start {genConfig['application']['application_name']} Service[ip=%1%,port=%2%]...")%IP%port));
    cout<<endl;
    ::std::shared_ptr<TServerEventHandler> addrEventHandler(new RemoteAddrEventHandler());
    server.setServerEventHandler(addrEventHandler);
    server.serve();
    return 0;
}}
    '''
    return code

def genApplicationCode(dataInfo, genConfig):
    code = ""
    if genConfig['application']['mode'] == "threadPool":
        code = genApplicationCodeThreadPool(dataInfo,genConfig)
    save_dir = genConfig['application']['save_path']
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    with open(save_dir + f'/{genConfig["application"]["application_name"]}Application.cpp', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == "__main__":
    print('----------------generate thrift-----------------------')
    genThriftCode(dataInfo, genConfig)
    print('----------------generate Dao--------------------------')
    genDaoCode(dataInfo, genConfig)
    print('----------------generate Service----------------------')
    genServiceCode(dataInfo, genConfig)
    print('----------generate Controller(Handdler)---------------')
    genControllerCode(dataInfo, genConfig)
    print('----------generate Application---------------')
    genApplicationCode(dataInfo, genConfig)
