/*********************************************************************
* Copyright (c) 2022（年）,ZZKJ-IIE单位技术研发部门
* All rights reserved.
*
* 文件名称：EasyLogger.h
* 文件标识：
* 摘    要：简要描述本文件的内容XXXXX
*
* 当前版本：1.0
* 作    者：输入作者（或修改者）名字
* 完成日期：2022年08月23日
*
* 取代版本：xx
* 原作者  ：xxx
* 完成日期：xxxx年xx月xx日
************************************************************************/

#ifndef COMPUTEFLOW_EasyLogger_H
#define COMPUTEFLOW_EasyLogger_H
//#define UNICODE

#include <iostream>
#include <string>
#include <mutex>
#include <log4cplus/helpers/loglog.h>
#include <log4cplus/logger.h>
#include <log4cplus/initializer.h>
#include <log4cplus/log4cplus.h>
#include <log4cplus/fileappender.h>
#include <log4cplus/consoleappender.h>
#include <log4cplus/layout.h>
#include <log4cplus/tchar.h>
#include <log4Cplus/configurator.h>
#include <log4Cplus/loggingmacros.h>
#include <log4Cplus/helpers/stringhelper.h>

#include "common/utils.hpp"

#define log_trace(logEvent)			LOG4CPLUS_TRACE(logger, logEvent)
#define log_debug(logEvent)			LOG4CPLUS_DEBUG(logger, logEvent)
#define log_debug_f(...)            LOG4CPLUS_DEBUG_FMT(logger, __VA_ARGS__)
#define log_info(logEvent)			LOG4CPLUS_INFO(logger, logEvent)
#define log_warn(logEvent)			LOG4CPLUS_WARN(logger, logEvent)
#define log_error(logEvent)			LOG4CPLUS_ERROR(logger, logEvent)
#define log_fatal(logEvent)			LOG4CPLUS_FATAL(logger, logEvent)

using namespace log4cplus;
using namespace log4cplus::helpers;
using namespace std;

class EasyLogger {
public:
    static Logger *getInstace() {
        if (NULL == m_logger) {
            lock_guard<mutex> mg(logMutex);
            if (NULL == m_logger) {
                m_logger = new EasyLogger;//在堆上建立
            }
        }
        return &m_logger->logger;
    }

    //static void deleteInstance();
    Logger logger;

    void shutDown() {
        log4cplus::Logger::shutdown();
    }

    void closeLog() {
        log4cplus::deinitialize();
    }

private:
    EasyLogger() {
        log4cplus::initialize();
        std:string LOG_CFG_FILE = "config/log.properties";
        std::string cfgPath = findTargetFile(LOG_CFG_FILE);
        if(cfgPath == ""){
            cerr << "----ERROR: can not find config file at "<< LOG_CFG_FILE << endl;
            throw std::exception(("ERROR: can not find config file at "+ LOG_CFG_FILE).c_str());
        }
        cout <<"---------Load log config path: " << cfgPath << "--------" << endl;
        try {
            PropertyConfigurator::doConfigure(cfgPath);
            logger = Logger::getRoot();
        }catch(exception &e){
            cerr << "----ERROR:" << e.what() << endl;
            throw e;
        }
//        cout << "Create Singleton for log4cplus!" << endl;
    }

    ~EasyLogger() {
//        std::cout << "Destory singleton for log4cplus!!" << std::endl;
    }

    static EasyLogger *m_logger;
    static std::mutex logMutex;
private:
    //内部类来删除对象
    class Garbo {
    public:
        Garbo() {}
        ~Garbo() {
            if (m_logger != NULL) {
                delete m_logger;
                m_logger = nullptr;
            }
        }
    };
    static Garbo _garbo;
};
EasyLogger *EasyLogger::m_logger = NULL;
mutex EasyLogger::logMutex;
EasyLogger::Garbo EasyLogger::_garbo;
log4cplus::Logger logger = *EasyLogger::getInstace();


#endif //COMPUTEFLOW_EasyLogger_H
