/*********************************************************************
* Copyright (c) 2022���꣩,ZZKJ-IIE��λ�����з�����
* All rights reserved.
*
* �ļ����ƣ�BaseService.h
* �ļ���ʶ��
* ժ    Ҫ����Ҫ�������ļ�������XXXXX
*
* ��ǰ�汾��1.0
* ��    �ߣ��������ߣ����޸��ߣ�����
* ������ڣ�2022��11��25��
*
* ȡ���汾��xx
* ԭ����  ��xxx
* ������ڣ�xxxx��xx��xx��
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
