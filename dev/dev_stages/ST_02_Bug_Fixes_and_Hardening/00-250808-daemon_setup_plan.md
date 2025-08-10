# ST_02: Process Management and Daemon Setup

**Status**: ✅ IN PROGRESS  
**Risk Level**: High  
**Estimated Duration**: 2 sessions  

---

## 🎯 **Objective**
Fix chat monitor persistence and process management so the system runs continuously in the background, surviving session closure and providing real-time monitoring.

## 📋 **Current State Analysis**

### **Current Daemon Issues:**
- `bin/start` launches monitor but doesn't maintain persistence
- Process dies when terminal session ends
- No proper PID file management
- No graceful shutdown handling
- Monitor doesn't survive system restart

### **Expected Behavior:**
- Background service runs continuously 
- Survives terminal/session closure
- Automatic restart on system boot
- Proper start/stop/restart controls
- Real-time file monitoring active 24/7

---

## 📋 **Tasks Checklist**

### **Phase 1: Current Daemon Investigation**
- [ ] **Test Current Daemon Behavior**
  - [ ] Test `bin/start` current functionality
  - [ ] Check if monitor runs in background
  - [ ] Test session persistence (close terminal)
  - [ ] Verify PID file creation and management
  - [ ] Check process lifecycle

### **Phase 2: Daemon Architecture Design**
- [ ] **Design Proper Daemon Mode**
  - [ ] Implement detached process execution
  - [ ] Add PID file management
  - [ ] Design graceful shutdown handling
  - [ ] Plan process restart logic
  - [ ] Design service integration

### **Phase 3: Daemon Implementation**
- [ ] **Implement Background Process Management**
  - [ ] Fix daemon mode in `chat_monitor.py`
  - [ ] Add proper process detachment
  - [ ] Implement PID file creation/cleanup
  - [ ] Add signal handling (SIGTERM, SIGINT)
  - [ ] Test background execution

### **Phase 4: Service Integration** 
- [ ] **Create Service Management Scripts**
  - [ ] Enhanced `bin/start` with daemon features
  - [ ] Create `bin/stop` script
  - [ ] Create `bin/restart` script  
  - [ ] Add status checking capabilities
  - [ ] Test full service lifecycle

---

## ✅ **Entry Criteria**
- ST_01 Universal Access completed successfully
- All commands work without manual venv activation
- JSON processing confirmed working
- System baseline stable

## 🎯 **Exit Criteria** 
- [ ] ✅ **Chat monitor runs persistently in background**
- [ ] ✅ **Process can be started/stopped/restarted reliably**
- [ ] ✅ **Monitor survives terminal session closure**
- [ ] ✅ **Real-time file monitoring active continuously**
- [ ] ✅ **All ST_00 + ST_01 functionality preserved**

---

## 🔧 **Investigation Commands**
```bash
# Test current daemon behavior
bin/start
ps aux | grep chat_monitor
jobs

# Test session persistence
bin/start
# Close terminal, open new one
ps aux | grep chat_monitor

# Test PID management
ls -la *.pid
cat chat_monitor.pid

# Test monitoring functionality  
# (trigger bchat while daemon running)
```

---

## 📊 **Daemon Implementation Strategy**

### **Approach 1: Python Daemon (Recommended)**
- Use `os.fork()` and `os.setsid()` for proper detachment
- Implement PID file management in Python
- Add signal handlers for graceful shutdown
- Redirect stdout/stderr to log files

### **Approach 2: Shell Wrapper Daemon**
- Use `nohup` and `&` for background execution
- Shell script PID management
- Process monitoring and restart logic
- Simpler but less robust

### **Approach 3: System Service Integration**
- Create systemd service file (Linux)
- Create launchd plist (macOS) 
- Full system service integration
- Most robust but platform-specific

---

## ⚠️ **Risk Mitigation**
- **High Risk**: Process management and daemon implementation
- **Backup Strategy**: Full system backup before changes
- **Testing Strategy**: Test each daemon feature incrementally
- **Rollback Plan**: Can restore to working ST_01 state
- **Validation**: Ensure all existing functionality preserved

---

## 🔍 **Success Metrics**

### **Daemon Functionality Tests:**
1. **Background Execution**: Process runs detached from terminal
2. **Session Persistence**: Survives terminal closure  
3. **Process Control**: Start/stop/restart works reliably
4. **PID Management**: PID files created/cleaned properly
5. **Real-time Monitoring**: File watching active continuously
6. **Graceful Shutdown**: No zombie processes or file locks

### **Integration Tests:**
1. **Real-time Processing**: bchat triggers processed immediately
2. **JSON Generation**: Files created while daemon running
3. **Cross-session Functionality**: All features work with daemon
4. **Error Recovery**: Daemon recovers from API failures

---

## 📁 **Expected Deliverables**
- `daemon_investigation.md` - Analysis of current daemon issues  
- `daemon_implementation.md` - Technical implementation details
- Enhanced `bin/start` with proper daemon features
- New `bin/stop` and `bin/restart` scripts
- `validation.sh` - ST_02 specific validation tests
- `backup/` - Pre-ST_02 state backup

---

## 🚀 **Implementation Priority**

**Critical Path**: Fix daemon persistence first, then enhance with service management features.

1. **Core Daemon**: Make monitor run in background persistently
2. **Process Control**: Add start/stop/restart capability  
3. **Service Integration**: Full service management features
4. **Production Hardening**: Error handling and recovery

**Key Insight**: Once daemon persistence works, the system becomes truly production-ready for real-time AI conversation intelligence.

---

**Next Stage**: ST_03 (Real-time Monitoring Integration) - depends on working daemon