from typing import List, Union

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGeneration, Generation

from langchain.agents.agent import MultiActionAgentOutputParser
from langchain.agents.output_parsers.tools import (
    ToolAgentAction
)
import json
from json import JSONDecodeError
from typing import List, Union

from langchain_core.agents import AgentAction, AgentActionMessageLog, AgentFinish
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ToolCall,
)
from langchain_core.outputs import ChatGeneration, Generation

from langchain.agents.agent import MultiActionAgentOutputParser


class ToolAgentAction(AgentActionMessageLog):
    tool_call_id: str
    """Tool call that this message is responding to."""


def parse_ai_message_to_tool_action_custom(
    message: BaseMessage,
    catch_value: str
) -> Union[List[AgentAction], AgentFinish]:
    """Parse an AI message potentially containing tool_calls."""
    if not isinstance(message, AIMessage):
        raise TypeError(f"Expected an AI message got {type(message)}")
    
    actions: List = []
    if message.tool_calls:
        tool_calls = message.tool_calls
    else:
        if not message.additional_kwargs.get("tool_calls"):
            return AgentFinish(
                return_values={"output": message.content}, log=str(message.content)
            )
        # Best-effort parsing
        tool_calls = []
        for tool_call in message.additional_kwargs["tool_calls"]:
            function = tool_call["function"]
            function_name = function["name"]
            if function_name == catch_value:
                args = json.loads(function["arguments"])
                return AgentFinish(return_values=args, log=str(function))
            try:
                args = json.loads(function["arguments"] or "{}")
                tool_calls.append(
                    ToolCall(name=function_name, args=args, id=tool_call["id"])
                )
            except JSONDecodeError:
                raise OutputParserException(
                    f"Could not parse tool input: {function} because "
                    f"the `arguments` is not valid JSON."
                )
    for tool_call in tool_calls:
        # HACK HACK HACK:
        # The code that encodes tool input into Open AI uses a special variable
        # name called `__arg1` to handle old style tools that do not expose a
        # schema and expect a single string argument as an input.
        # We unpack the argument here if it exists.
        # Open AI does not support passing in a JSON array as an argument.
        function_name = tool_call["name"]
        _tool_input = tool_call["args"]
        if "__arg1" in _tool_input:
            tool_input = _tool_input["__arg1"]
        else:
            tool_input = _tool_input

        content_msg = f"responded: {message.content}\n" if message.content else "\n"
        log = f"\nInvoking: `{function_name}` with `{tool_input}`\n{content_msg}\n"
        actions.append(
            ToolAgentAction(
                tool=function_name,
                tool_input=tool_input,
                log=log,
                message_log=[message],
                tool_call_id=tool_call["id"],
            )
        )
    return actions

OpenAIToolAgentAction = ToolAgentAction


def parse_ai_message_to_openai_tool_action_custom(
    message: BaseMessage, catch_value: str
) -> Union[List[AgentAction], AgentFinish]:
    """Parse an AI message potentially containing tool_calls."""
    tool_actions = parse_ai_message_to_tool_action_custom(message, catch_value)
    if isinstance(tool_actions, AgentFinish):
        return tool_actions
    final_actions: List[AgentAction] = []
    for action in tool_actions:
        if isinstance(action, ToolAgentAction):
            final_actions.append(
                OpenAIToolAgentAction(
                    tool=action.tool,
                    tool_input=action.tool_input,
                    log=action.log,
                    message_log=action.message_log,
                    tool_call_id=action.tool_call_id,
                )
            )
        else:
            final_actions.append(action)
    return final_actions


class OpenAIToolsAgentOutputParserCustom(MultiActionAgentOutputParser):
    """Parses a message into agent actions/finish.

    Is meant to be used with OpenAI models, as it relies on the specific
    tool_calls parameter from OpenAI to convey what tools to use.

    If a tool_calls parameter is passed, then that is used to get
    the tool names and tool inputs.

    If one is not passed, then the AIMessage is assumed to be the final output.
    """

    @property
    def _type(self) -> str:
        return "openai-tools-agent-output-parser"

    def parse_result(
        self, result: List[Generation], *, partial: bool = False
    ) -> Union[List[AgentAction], AgentFinish]:
        if not isinstance(result[0], ChatGeneration):
            raise ValueError("This output parser only works on ChatGeneration output")
        message = result[0].message
        catch_value = "Response"
        return parse_ai_message_to_openai_tool_action_custom(message, catch_value)

    def parse(self, text: str) -> Union[List[AgentAction], AgentFinish]:
        raise ValueError("Can only parse messages")