
from abc import ABC, abstractmethod
from openhands.sdk import Tool
from pydantic import BaseModel
from openhands.tools import BashTool, FileEditorTool, TaskTrackerTool


class ToolRequest(BaseModel, ABC):
    """ A request to create a tool for use in an LLM. """
    
    @abstractmethod
    def create_tool(self) -> Tool:
        """ Create a tool """


class BashToolRequest(ToolRequest):
    working_dir: str

    def create_tool(self):
        return BashTool.create(working_dir=self.working_dir)
    

class FileEditorToolRequest(ToolRequest):

    def create_tool(self):
        return FileEditorTool.create()
 

class TaskTrackerToolRequest(ToolRequest):
    save_dir: str

    def create_tool(self):
        return TaskTrackerTool.create(save_dir=self.save_dir)
    

ToolRequestType = BashToolRequest | FileEditorToolRequest | TaskTrackerToolRequest
