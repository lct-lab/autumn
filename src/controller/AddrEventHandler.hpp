/*********************************************************************
* Copyright (c) 2022（年）,ZZKJ-IIE单位技术研发部门
* All rights reserved.
*
* 文件名称：EventHandler.h
* 文件标识：
* 摘    要：简要描述本文件的内容XXXXX
*
* 当前版本：1.0
* 作    者：王新
* 完成日期：2022年11月28日
*
* 取代版本：xx
* 原作者  ：xxx
* 完成日期：xxxx年xx月xx日
************************************************************************/

#ifndef RADAR_BACKEND_ADDREVENTHANDLER_HPP
#define RADAR_BACKEND_ADDREVENTHANDLER_HPP

#include <iostream>

#include <boost/format.hpp>
#include <thrift/server/TServer.h>

#include "common/EasyLogger.hpp"

using namespace apache::thrift::server;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

class RemoteAddress{
public:
    std::string ip;
    std::string port;
};

class RemoteAddrEventHandler: public TServerEventHandler {
public:
    /**
     * Called before the server begins.
     */
    virtual void preServe() {}

    /**
     * Called when a new client has connected and is about to being processing.
     */
    virtual void* createContext(std::shared_ptr<TProtocol> input,
                                std::shared_ptr<TProtocol> output) {
//        std::shared_ptr<TSocket> transport = std::dynamic_pointer_cast<TSocket>(input->getTransport());
//        TSocket& socket = *transport;
//        std::string ip =  socket.getPeerAddress();
//        int port = socket.getPeerPort();
//        log_info(str(boost::format("Processing call from client ip:port = %1%%2%")%ip%port));
        return new RemoteAddress;
    }

    /**
     * Called when a client has finished request-handling to delete server
     * context.
     */
    virtual void deleteContext(void* serverContext,
                               std::shared_ptr<TProtocol> input,
                               std::shared_ptr<TProtocol> output) {
        (void)serverContext;
        (void)input;
        (void)output;
        delete (RemoteAddress*) serverContext;
    }

    /**
     * Called when a client is about to call the processor.
     */
    virtual void processContext(void* serverContext, std::shared_ptr<TTransport> transport) {
        (void)serverContext;
        TSocket& socket = dynamic_cast<TSocket &>(*transport);
        std::string ip =  socket.getPeerAddress();
        int port = socket.getPeerPort();
        log_info(str(boost::format("Processing call from client ip:port = %1%%2%")%ip%port));
        std::cout<< std::endl;
    }

};

#endif //RADAR_BACKEND_ADDREVENTHANDLER_HPP
