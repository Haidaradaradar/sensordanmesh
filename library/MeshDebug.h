#pragma once               
#include <Arduino.h>       
#include <painlessMesh.h>  
#include <ArduinoJson.h>   

class MeshDebug {
public:
    MeshDebug();

    void begin(String prefix, String password, uint16_t port);
    void update();

    void sendHeartbeat();
    void setDebug(bool enable); 
    
    // FUNGSI BARU: Menerima data sensor dari .ino
    void setSensorData(float tempDHT, float tempBMP);

private:
    painlessMesh mesh;
    Scheduler userScheduler;
    Task taskHeartbeat;

    static MeshDebug* instance;
    bool debugEnabled; 
    
    // VARIABEL BARU: Menyimpan data suhu terakhir
    float lastTempDHT;
    float lastTempBMP;

    static void heartbeatCallback();
    void receivedCallback(uint32_t from, String &msg);
    void newConnectionCallback(uint32_t nodeId);
    void changedConnectionCallback();
};
