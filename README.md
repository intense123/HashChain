# Hash Chain System with Web Interface

A distributed hash chain implementation with a web-based interface for managing servers and data distribution. The system uses consistent hashing to distribute data across multiple servers and provides real-time visualization of data movement during server changes.

## Features

- Consistent hashing implementation for data distribution
- Dynamic server addition and removal
- Real-time visualization of data movement
- Web-based interface for system management
- Animated data redistribution when servers change

## Components

1. **hashchain.py**: Core implementation of the hash chain system
   - Server management
   - Data distribution logic
   - Consistent hashing implementation

2. **app.py**:
   Flask web server
   - RESTful API endpoints
   - Server-side logic
   - Integration with hash chain system

3. **Web Interface**:
   - Interactive UI for system management
   - Real-time visualization
   - Animated data movement


