"""
Plugin Manager - Handles dynamic plugin loading and execution
"""

import logging
from typing import Dict, List, Any, Callable
import importlib
import os

logger = logging.getLogger(__name__)


class Plugin:
    """Base plugin class"""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality"""
        raise NotImplementedError("Plugins must implement execute method")


class PluginManager:
    """Manages plugin lifecycle and execution"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        logger.info("Plugin Manager initialized")
    
    def register_plugin(self, plugin: Plugin):
        """Register a new plugin"""
        self.plugins[plugin.name] = plugin
        logger.info(f"Plugin registered: {plugin.name}")
    
    def unregister_plugin(self, plugin_name: str):
        """Remove a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logger.info(f"Plugin unregistered: {plugin_name}")
    
    async def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """Execute a specific plugin"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin not found: {plugin_name}")
        
        plugin = self.plugins[plugin_name]
        if not plugin.enabled:
            logger.warning(f"Plugin disabled: {plugin_name}")
            return None
        
        return await plugin.execute(*args, **kwargs)
    
    def list_plugins(self) -> List[str]:
        """Get list of registered plugins"""
        return list(self.plugins.keys())
    
    def register_hook(self, event: str, callback: Callable):
        """Register a hook for an event"""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    async def trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all hooks for an event"""
        if event in self.hooks:
            for callback in self.hooks[event]:
                await callback(*args, **kwargs)
