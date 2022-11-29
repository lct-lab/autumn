/*********************************************************************
* Copyright (c) 2022（年）,ZZKJ-IIE单位技术研发部门
* All rights reserved.
*
* 文件名称：BaseService.h
* 文件标识：
* 摘    要：简要描述本文件的内容XXXXX
*
* 当前版本：1.0
* 作    者：输入作者（或修改者）名字
* 完成日期：2022年11月25日
*
* 取代版本：xx
* 原作者  ：xxx
* 完成日期：xxxx年xx月xx日
************************************************************************/

#ifndef BASESERVICE_HPP
#define BASESERVICE_HPP

class BaseService {
public:
    enum OrderType{
        ASC ,
        DESC,
        STAY // stay the same with the input ids when query in detail method
    };
};

#endif //RADAR_BACKEND_BASESERVICE_HPP
