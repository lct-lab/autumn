//
// Created by WX on 2022/11/21.
//
#include <vector>
#include <iostream>
#include <thread>

#include "BasicDataAccess.h"
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>

#include "dao/TargetTypesDao.hpp"
#include "dao/SysLogDao.hpp"
#include "service/SysLogService.hpp"

using namespace std;

using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace Radar::Buisiness;

void testDaoInfoList() {
    SysLogDao ttDao;
    std::vector<std::string> createTime;
    std::vector<std::string> insertTime = {"2022-05-01", "2023-05-01"};
    std::vector<std::string> updateTime;
    std::vector<std::string> users;
    std::vector<std::string> subSys;
    std::vector<std::string> types;
    SysLogDao::getSysLogInfoListRet ret;
    ttDao.getSysLogInfoList(ret, createTime, insertTime, updateTime, users, subSys, types);
    log_info("testDaoInfoList : " + to_string(ret.retCode));
    log_info("testDaoInfoList : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testDaoInfoList : name = " + ret.data[i].name + ",desc = " + ret.data[i].desc);
        }
}

void testDaoInfoDetail() {
    TargetTypesDao ttDao;
    std::vector<std::string> id = {"701507ce-3dbd-410a-bc55-50f0e0d5af98", "fe622b23-2952-48e6-8171-e0b1e15a05b4"};
//    std::vector<std::string> id = {};
    TargetTypesDao::getTargetTypesInfoDetailRet ret;
    ttDao.getTargetTypesInfoDetail(ret, id, TargetTypesDao::OrderFields::insert_time,
                                   DataAccessor::OrderType::DESC);
    log_info("testDaoInfoDetail : " + to_string(ret.retCode));
    log_info("testDaoInfoDetail : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testDaoInfoDetail : name = " + ret.data[i].name + ",desc = " + ret.data[i].desc);
        }
}

void testDaoInsert() {
    SysLogDao slDao;
    SysLogDao::Entity dataItem1;
    dataItem1.name = "FF123";
    dataItem1.desc = "123";
    dataItem1.create_time = "2022-05-01";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    SysLogDao::Entity dataItem2;
    dataItem2.name = "FF-245";
    dataItem2.desc = "dapao";
    dataItem2.create_time = "2022-06-01";
    dataItem2.user = "fdd3533e-5c94-86db-f3a5-ca4e053320f7";
    dataItem2.sub_sys = "fab91ac1-2210-d01d-aeae-ab0531765965";
    dataItem2.content = "{}";
    std::vector<SysLogDao::Entity> datas = {dataItem1, dataItem2};
    SysLogDao::insertSysLogRet ret;
    slDao.insertSysLog(ret, datas);
    log_info("testDaoInsert : " + to_string(ret.retCode));
    log_info("testDaoInsert : " + ret.retDesc);
}

void testDaoUpdate() {
    SysLogDao ttDao;
    SysLogDao::Entity dataItem1;
    dataItem1.id = "27610a6c-15bb-4106-86f3-d3c7c3fb5ca2";
    dataItem1.name = "FF123";
    dataItem1.desc = "飞机";
    dataItem1.create_time = "2022-05-01 00:00:00";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    std::vector<SysLogDao::Entity> datas = {dataItem1};
    SysLogDao::updateSysLogRet ret;
    ttDao.updateSysLog(ret, datas);
    log_info("testDaoUpdate : " + to_string(ret.retCode));
    log_info("testDaoUpdate : " + ret.retDesc);
//    TargetTypesDao ttDao;
//    TargetTypesDao::Entity dataItem1;
//    dataItem1.id = "27610a6c-15bb-4106-86f3-d3c7c3fb5ca2";
//    dataItem1.name = "GG123";
//    dataItem1.desc = "�ɻ�";
//    std::vector<TargetTypesDao::Entity> datas={dataItem1};
//    TargetTypesDao::updateTargetTypesRet ret;
//    ttDao.updateTargetTypes(ret, datas);
//    log_info("testDaoUpdate : " + to_string(ret.retCode));
//    log_info("testDaoUpdate : " + ret.retDesc);
}

void testDaoDelete() {
    TargetTypesDao ttDao;
    std::vector<std::string> id = {"701507ce-3dbd-410a-bc55-50f0e0d5af98"};
    std::vector<std::string> insertTime = {"2022-05-01", "2023-05-01"};
    std::vector<std::string> updateTime;
    TargetTypesDao::deleteTargetTypesRet ret;
    ttDao.deleteTargetTypes(ret, id, insertTime, updateTime);
    log_info("testDaoDelete : " + to_string(ret.retCode));
    log_info("testDaoDelete : " + ret.retDesc);
}


void testServiceInfoDetail() {
    SysLogService s;
    SysLogService::getSysLogInfoDetailRet ret;
    vector<std::string> id = {"d30aacc2-38dc-4a58-812e-b0d49bb177e5"};
    s.getSysLogInfoDetail(ret, id);
    log_info("testServiceInfoDetail : " + to_string(ret.retCode));
    log_info("testServiceInfoDetail : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testServiceInfoDetail : name = " + ret.data[i].name + ",desc = " + ret.data[i].desc +
                     ",user_name = " + ret.data[i].user_name);
        }
};

void testServiceInsert() {
    SysLogService ss;
    SysLogService::Entity dataItem1;
    dataItem1.id = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.name = "FF123";
    dataItem1.desc = "飞机";
    dataItem1.create_time = "2022-05-01";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    SysLogService::Entity dataItem2;
    dataItem2.name = "FF-245";
    dataItem2.desc = "dapao";
    dataItem2.create_time = "2022-06-01";
    dataItem2.user = "fdd3533e-5c94-86db-f3a5-ca4e053320f7";
    dataItem2.sub_sys = "fab91ac1-2210-d01d-aeae-ab0531765965";
    dataItem2.content = "{}";
    std::vector<SysLogService::Entity> datas = {dataItem1, dataItem2};
    SysLogService::insertSysLogRet ret;
    ss.insertSysLog(ret, datas);
    log_info("testServiceInsert : " + to_string(ret.retCode));
    log_info("testServiceInsert : " + ret.retDesc);
}

void testServiceInfoList() {
    SysLogService ttDao;
    std::vector<std::string> createTime;
    std::vector<std::string> insertTime = {"2022-05-01", "2023-05-01"};
    std::vector<std::string> updateTime;
    std::vector<std::string> users;
    std::vector<std::string> subSys;
    std::vector<std::string> types;
    SysLogService::getSysLogInfoListRet ret;
    ttDao.getSysLogInfoList(ret, createTime, insertTime, updateTime, users, subSys, types);
    log_info("testDaoInfoList : " + to_string(ret.retCode));
    log_info("testDaoInfoList : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testDaoInfoList : name = " + ret.data[i].name + ",desc = " + ret.data[i].desc);
        }
}

void testServiceDelete() {
    SysLogService ttDao;
    std::vector<std::string> id = {"0ab10382-bb6d-4646-aa04-d175dcaeb2c3"};
    std::vector<std::string> insertTime;
    std::vector<std::string> updateTime;
    std::vector<std::string> users;
    std::vector<std::string> subSys;
    std::vector<std::string> types;
    SysLogService::deleteSysLogRet ret;
    ttDao.deleteSysLog(ret, id, insertTime, insertTime, updateTime, users, subSys, types);
    log_info("testServiceDelete : " + to_string(ret.retCode));
    log_info("testServiceDelete : " + ret.retDesc);
}

void testServiceUpdate() {
    SysLogService ttDao;
    SysLogService::Entity dataItem1;
    dataItem1.id = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.name = "tt123";
    dataItem1.desc = "飞机";
    dataItem1.create_time = "2022-05-01 00:00:00";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    SysLogService::Entity dataItem2 = dataItem1;
    dataItem2.id = "27610a6c-15bb-4106-86f3-d3c7c3fb5ca2";
    dataItem2.name = "QQ123";
    std::vector<SysLogService::Entity> datas = {dataItem1, dataItem2};
    SysLogService::updateSysLogRet ret;
    ttDao.updateSysLog(ret, datas);
    log_info("testServiceUpdate : " + to_string(ret.retCode));
    log_info("testServiceUpdate : " + ret.retDesc);
}

void testRPCInsert(BasicDataAccessClient &client) {
    SysLogInsertRet ret;
    SysLogEntity dataItem1;
    dataItem1.name = "FF123";
    dataItem1.desc = "消息";
    dataItem1.create_time = "2022-05-01";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    SysLogEntity dataItem2;
    dataItem2.name = "FF-245";
    dataItem2.desc = "132";
    dataItem2.create_time = "2022-06-01";
    dataItem2.user = "fdd3533e-5c94-86db-f3a5-ca4e053320f7";
    dataItem2.sub_sys = "fab91ac1-2210-d01d-aeae-ab0531765965";
    dataItem2.content = "{}";
    std::vector<SysLogEntity> datas = {dataItem1, dataItem2};
    client.insertSysLog(ret, datas);
    log_info("testRPCInsert : " + to_string(ret.retCode));
    log_info("testRPCInsert : " + ret.retDesc);
}

void testRPCInfoList(BasicDataAccessClient &client) {
    std::vector<std::string> createTime;
    std::vector<std::string> insertTime = {"2022-05-01", "2023-05-01"};
    std::vector<std::string> updateTime;
    std::vector<std::string> users;
    std::vector<std::string> subSys;
    std::vector<std::string> types;
    SysLogInfoListRet ret;
    client.getSysLogInfoList(ret, createTime, insertTime, updateTime, users, subSys, types,
                             SysLogOrderFields::insert_time, OrderType::DESC, 20, 0);
    log_info("testRPCInfoList : " + to_string(ret.retCode));
    log_info("testRPCInfoList : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testRPCInfoList : name = " + ret.data[i].name + ",desc = "  + ",desc = " + ret.data[i].desc +
                                                                      ",user_name = " + ret.data[i].user_name);
        }
}

void testRPCInfoDetail(BasicDataAccessClient &client) {
    SysLogInfoDetailRet ret;
    vector<std::string> id = {"2b71b274-22ce-40a1-8510-2ade8b39aed3","c00e49a5-ec2b-432f-b202-7bd4b7d1dca9"};
    client.getSysLogInfoDetail(ret, id,SysLogOrderFields::insert_time, OrderType::DESC);
    log_info("testRPCInfoDetail : " + to_string(ret.retCode));
    log_info("testRPCInfoDetail : " + ret.retDesc);
    if (ret.dataTotal > 0)
        for (int i = 0; i < ret.dataTotal; i++) {
            log_info("testRPCInfoDetail : name = " + ret.data[i].name + ",desc = " + ret.data[i].desc +
                             ",user_name = " + ret.data[i].user_name + ",sub_sys_name = " + ret.data[i].sub_sys_name);
        }
};

void testRPCDelete(BasicDataAccessClient &client) {
    SysLogDeleteRet ret;
    vector<std::string> id = {"89a655a6-a251-4215-a008-b08bb54e627e"};
    std::vector<std::string> createTime;
    std::vector<std::string> insertTime = {"2022-05-01", "2023-05-01"};
    std::vector<std::string> updateTime;
    std::vector<std::string> users;
    std::vector<std::string> subSys;
    std::vector<std::string> types;
    client.deleteSysLog(ret, id,createTime,insertTime,updateTime,users,subSys,types);
    log_info("testRPCDelete : " + to_string(ret.retCode));
    log_info("testRPCDelete : " + ret.retDesc);
};

void testRPCUpdate(BasicDataAccessClient &client) {
    SysLogUpdateRet ret;
    SysLogEntity dataItem1;
    dataItem1.id = "bac4f8fb-aa91-4f24-b74e-103a618f493a";
    dataItem1.name = "qqqqqqqqq";
    dataItem1.desc = "消息";
    dataItem1.create_time = "2022-05-01";
    dataItem1.user = "85892ad4-110a-5b01-b887-cb7c160e4d5e";
    dataItem1.sub_sys = "4d4ed2ed-cb9f-4fff-7d9e-e302250fd91d";
    dataItem1.content = "{}";
    std::vector<SysLogEntity> datas = {dataItem1};
    client.updateSysLog(ret, datas);
    log_info("testRPCUpdate : " + to_string(ret.retCode));
    log_info("testRPCUpdate : " + ret.retDesc);
}
int main() {
//    testDaoInfoList();
//    testDaoDelete();
//    testDaoInfoDetail();
//    testDaoInsert();
//    testDaoUpdate();
//    testDaoInfoList();
//    testServiceInfoDetail();
//    testServiceInsert();
//    testServiceInfoList();
//    testServiceDelete();
//    testServiceUpdate();
//    testServiceInfoList();

// thrift test
    std::shared_ptr<TSocket> socket(new TSocket("localhost", 9090));
//    shared_ptr<TSocket> socket(new TSocket("192.168.1.208", 9090));
    std::shared_ptr<TTransport> itransport(new TBufferedTransport(socket));
    std::shared_ptr<TProtocol> iprotocol(new TBinaryProtocol(itransport));
    BasicDataAccessClient client(iprotocol);
    try {
        itransport->open();
        log_info("init client successful");
    }
    catch (TTransportException &e) {
        itransport->close();
        log_info("init client failed");
        log_error(e.what());
    }
//    testRPCInsert(client);
    Sleep(5000);
    testRPCInfoList(client);
    for(int i = 0; i< 5; i++) {
        std::cout << "-----------------" << std::endl;
//        Sleep(5000);
        testRPCInfoDetail(client);
    }
//    testRPCDelete(client);
//    testRPCUpdate(client);
}

