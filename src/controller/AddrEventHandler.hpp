/*********************************************************************
* Copyright (c) 2022���꣩,ZZKJ-IIE��λ�����з�����
* All rights reserved.
*
* �ļ����ƣ�EventHandler.h
* �ļ���ʶ��
* ժ    Ҫ����Ҫ�������ļ�������XXXXX
*
* ��ǰ�汾��1.0
* ��    �ߣ�����
* ������ڣ�2022��11��28��
*
* ȡ���汾��xx
* ԭ����  ��xxx
* ������ڣ�xxxx��xx��xx��
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
