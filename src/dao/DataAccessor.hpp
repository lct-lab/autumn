

#ifndef DATAACCESS_HPP
#define DATAACCESS_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <mutex>
#include <thread>
#include <map>

#include <boost/format.hpp>
#include <boost/algorithm/string/join.hpp>
#include <inicpp.h>


#include "common/EasyLogger.hpp"
#include "common/utils.hpp"
#include "nanodbc.h"

using namespace boost;

class DBPool
{
private:
    map<std::string, nanodbc::connection *> _conns; // each thread a connection
    int connectTimeout;
    int connectRetryTimes;
    bool pooling;
    std::string dsn;
    std::string user;
    std::string passwd;
    DBPool(std::string configPath = "config/dbConfig.ini") {
        configPath = findTargetFile(configPath);
        if(configPath == ""){
            log_error("Database connection config file not found");
            throw std::exception("Database connection config file not found");
        }
        log_info("-----Load DB config file from " + configPath);
        ini::IniFile config;
        config.load(configPath);
        connectTimeout = config["CONNECTION"]["connectTimeout"].as<int>();
        sqlTimeout = config["CONNECTION"]["sqlTimeout"].as<int>();
        connectRetryTimes = config["CONNECTION"]["connectRetryTimes"].as<int>();
        dsn = config["CONNECTION"]["dsn"].as<std::string>();
        user = config["CONNECTION"]["user"].as<std::string>();
        passwd = config["CONNECTION"]["passwd"].as<std::string>();
        sqlTimeout = config["EXECUTE"]["sqlTimeout"].as<int>();
    }
    ~DBPool() {
        for(auto &t : _conns){
            t.second->disconnect();
        }
    };
    DBPool(const DBPool&){

    }
    DBPool& operator=(const DBPool&){

    }
public:
    int sqlTimeout;
    static DBPool* getInstance()
    {
        static DBPool instance;
        return &instance;
    }
    nanodbc::connection *getConnection() {
        std::stringstream ss;
        ss << std::this_thread::get_id();
        std::string curPid = ss.str();
        bool need2Connect = false;
        try{
            if (_conns.find(curPid) == _conns.end() || !_conns[curPid]->connected()) {
                need2Connect = true;
            }else{
                execute(*_conns[curPid], "select 1;");
                need2Connect = false;
            }
        }catch(nanodbc::database_error &e){
            log_info("psuedo connected connection process");
            need2Connect = true;
        }
        if (need2Connect) {
            if (_conns.find(curPid) != _conns.end()) {
                _conns[curPid]->disconnect();
            }
            int i = 0;
            while (true) {
                try {
                    i++;
                    _conns[curPid] = new nanodbc::connection(dsn, user, passwd, connectTimeout, pooling);
                    log_info("gen connection of thread:" +  curPid);
                    return _conns[curPid];
                } catch (std::exception &e) {
                    log_error("connection to database error, tried " + std::to_string(i)+ " times.");
                    log_error( e.what() );
                    if (i >= connectRetryTimes) {
                        throw e;
                    }
                }
            }
        } else {
            return _conns[curPid];
        }
    }
};


class DataAccessor{
public:
    enum OrderType{
        ASC ,
        DESC,
        STAY // stay the same with the input ids when query in detail method
    };
protected:
    nanodbc::connection * dbConn;
    DBPool* dbPool;

    map<int, std::string> OrderTypeMap = {
            {OrderType::ASC, "ASC"},
            {OrderType::DESC, "DESC"}
    };

    template<class T>
    std::string sql_condition_gen(std::string conditionType, // range or equal
                                  std::vector<T> conditionValue, // [minvalue,maxvalue] if range,
                                  std::string conditionKey, // column name of the talble
                                  bool using_placeholder = true
    ) {
        try {
            std::string conditionSql = "";
            if (conditionValue.empty())
                return conditionSql;
            if (conditionType == "range") {
                assert(conditionValue.size() == 2);
                std::string min = using_placeholder ? "?" : str(format("%1%") % conditionValue[0]);
                std::string max = using_placeholder ? "?" : str(format("%1%") % conditionValue[1]);
                if (typeid(conditionValue[0]) == typeid(std::string) && !using_placeholder) {
                    min = str(format("'%1%'") % min);
                    max = str(format("'%1%'") % max);
                }
                conditionSql += str(format("(%3% between %1% and %2%)") % min % max % conditionKey);
            } else if (conditionType == "equal") {
                if (conditionValue.size() == 1) {
                    std::string v = using_placeholder ? "?" : str(format("%1%") % conditionValue[0]);
                    if (typeid(conditionValue[0])  == typeid(std::string) && !using_placeholder)
                        v = str(format("'%1%'") % v);
                    conditionSql += str(format("(%1%=%2%)") % conditionKey % v);
                } else {
                    vector<string> vs;
                    for (T v:conditionValue) {
                        if(using_placeholder){
                            vs.push_back("?");
                        }else{
                            std::string sv = typeid(v) == typeid(std::string) ? str(format("'%1%'") % v) : str(format("%1%") % v);
                            vs.push_back(sv);
                        }
                    }
                    conditionSql += str(format("(%1% in (%2%) )") % conditionKey % join(vs,","));
                }
            }
            return "and " + conditionSql + "\n";
        }
        catch (std::exception &e) {
            log_error(e.what());
            return "";
        }
    }
public:
    DataAccessor(){
        dbPool = DBPool::getInstance();
        dbConn = dbPool->getConnection();
    }
};
#endif
        