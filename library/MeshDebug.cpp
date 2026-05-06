#include "MeshDebug.h"

MeshDebug* MeshDebug::instance = nullptr;

// UPDATE: Tambahkan inisialisasi default 0.0 untuk suhu
MeshDebug::MeshDebug()
: taskHeartbeat(3000, TASK_FOREVER, &MeshDebug::heartbeatCallback), 
  debugEnabled(true), lastTempDHT(0.0), lastTempBMP(0.0) {}

void MeshDebug::setDebug(bool enable) {
    debugEnabled = enable;
}

// UPDATE: Implementasi fungsi setter
void MeshDebug::setSensorData(float tempDHT, float tempBMP) {
    lastTempDHT = tempDHT;
    lastTempBMP = tempBMP;
}

void MeshDebug::heartbeatCallback() {
    if (instance) {
        instance->sendHeartbeat();
    }
}

void MeshDebug::begin(String prefix, String password, uint16_t port) {
    instance = this;
    mesh.init(prefix, password, &userScheduler, port);
    mesh.onReceive([this](uint32_t from, String &msg) { receivedCallback(from, msg); });
    mesh.onNewConnection([this](uint32_t nodeId) { newConnectionCallback(nodeId); });
    mesh.onChangedConnections([this]() { changedConnectionCallback(); });

    userScheduler.addTask(taskHeartbeat);
    taskHeartbeat.enable();

    if (debugEnabled) Serial.println("MeshDebug started");
}

void MeshDebug::update() {
    mesh.update();
}

void MeshDebug::sendHeartbeat() {
    JsonDocument doc; 
    doc["type"] = "HEARTBEAT";
    doc["nodeId"] = mesh.getNodeId();
    
    // UPDATE: Masukkan data sensor asli ke dalam JSON
    doc["t_dht"] = lastTempDHT;
    doc["t_bmp"] = lastTempBMP; 

    String jsonString;
    serializeJson(doc, jsonString);
    mesh.sendBroadcast(jsonString);

    if (debugEnabled) {
        Serial.println("Send JSON: " + jsonString);
    }
}

void MeshDebug::receivedCallback(uint32_t from, String &msg) {
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, msg);

    if (error) {
        if (debugEnabled) Serial.println("Bukan format JSON yang valid");
        return; 
    }

    String msgType = doc["type"];
    uint32_t senderId = doc["nodeId"];
    
    // UPDATE: Ambil dua data suhu sekaligus
    float t_dht = doc["t_dht"]; 
    float t_bmp = doc["t_bmp"];

    if (msgType == "HEARTBEAT" && debugEnabled) {
        Serial.printf("Data dari Node %u | DHT: %.2f C | BMP: %.2f C\n", senderId, t_dht, t_bmp);
    }
}

void MeshDebug::newConnectionCallback(uint32_t nodeId) {
    if (debugEnabled) Serial.printf("New node connected: %u\n", nodeId);
}

void MeshDebug::changedConnectionCallback() {
    if (debugEnabled) Serial.println("Connection changed");
}