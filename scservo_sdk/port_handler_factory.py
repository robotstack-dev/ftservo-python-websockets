#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .port_handler import PortHandler
from .websocket_handler import WebSocketHandler

def get_port_handler(port_name):
    """
    Factory function to return the appropriate port handler based on the port name
    
    Args:
        port_name (str): Name of the port (e.g., "COM1", "ws://localhost:8080")
        
    Returns:
        Either PortHandler or WebSocketHandler instance
    """
    if port_name.startswith(('ws://', 'wss://')):
        return WebSocketHandler(port_name)
    else:
        return PortHandler(port_name) 