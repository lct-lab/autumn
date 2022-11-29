/*********************************************************************
* Copyright (c) 2022（年）,ZZKJ-IIE单位技术研发部门
* All rights reserved.
*
* 文件名称：utils.h
* 文件标识：
* 摘    要：简要描述本文件的内容XXXXX
*
* 当前版本：1.0
* 作    者：王新
* 完成日期：2022年08月24日
*
* 取代版本：xx
* 原作者  ：xxx
* 完成日期：xxxx年xx月xx日
************************************************************************/

#ifndef COMPUTEFLOW_UTILS_HPP
#define COMPUTEFLOW_UTILS_HPP

#include<boost/any.hpp>
#include<filesystem>
#include <boost/uuid/uuid.hpp>            // uuid class
#include <boost/uuid/uuid_generators.hpp> // generators
#include <boost/uuid/uuid_io.hpp>
#include <algorithm>


using namespace std;

std::string any2str(boost::any obj){
    if(obj.type() == typeid(int))
        return std::to_string(boost::any_cast<int>(obj));
    else if(obj.type() == typeid(double))
        return std::to_string(boost::any_cast<double>(obj));
    else if(obj.type() == typeid(std::string))
        return boost::any_cast<std::string>(obj);
    else
        return "";
}

string getCurTimestr(string space=" ", string colon=":"){
    time_t timep;
    time(&timep);
    char datetime[64];
    strftime(datetime, sizeof(datetime), ("%Y-%m-%d"+space+"%H"+colon+"%M"+colon+"%S").c_str(), localtime(&timep));
    return datetime;
}

//在工作目录或执行文件所在目录为base，查找目标文件的绝对路径
string findTargetFile(string targetRelativePath, bool usingWorkDir=true, bool usingProcDir=true){
    filesystem::path target = filesystem::path(targetRelativePath);
    if(usingWorkDir){
        filesystem::path workDir = filesystem::current_path();
        if(filesystem::exists(workDir/target)){
            return (workDir/target).string();
        }
    }
    if(usingProcDir){
        std::string procPath = _pgmptr;
        filesystem::path procDir(filesystem::absolute(procPath));
        procDir = procDir.parent_path();
        if(filesystem::exists(procDir/target)){
            return (procDir/target).string();
        }
    }
    return "";
}


string progressStr(int cur, int total) {
    string pStr = "";
    int targetNum = 100;
    if (cur > 1) {
        for (int i = 0; i < targetNum + 2; i++) {
            pStr += "\b";
        }
    }
    pStr += "|";
    for (int i = 0; i < targetNum; i++) {
        if (cur * targetNum / total < i) {
            if (cur * targetNum / total >= (i - 1))
                pStr += ">";
            else
                pStr += " ";
        } else {
            pStr += "-";
        }
    }
    pStr += "|";
    return pStr;
}

vector<std::string> getUUID(int number){
    vector<std::string> uuids;
    boost::uuids::random_generator generator;
    if(number <= 0){
        return uuids;
    }
    for(int i=0; i< number; i++){
        std::string uuid = boost::uuids::to_string(generator());
        uuids.push_back(uuid);
    }
    return uuids;
}

void toUpperCase(vector<std::string> & strs){
    for(int i=0; i< strs.size();i++){
        transform(strs[i].begin(), strs[i].end(), strs[i].begin(), ::toupper);
    }
}

void toUpperCase(std::string & str){
    transform(str.begin(), str.end(), str.begin(), ::toupper);
}

void toLowerCase(vector<std::string> & strs){
    for(int i=0; i< strs.size();i++){
        transform(strs[i].begin(), strs[i].end(), strs[i].begin(), ::tolower);
    }
}

void toLowerCase(std::string & str){
    transform(str.begin(), str.end(), str.begin(), ::tolower);
}

#endif //COMPUTEFLOW_UTILS_HPP
