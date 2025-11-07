from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, Task, TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from agent import AnalysisBugAgent


class AnalysisBugAgentExecutor(AgentExecutor):
    """Code Bug Analysis Agent Executor"""
    
    def __init__(self):
        self.agent = AnalysisBugAgent()
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute error analysis"""
        query = context.get_user_input()
        task = context.current_task
        
        # Create task if not exists
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        
        # Call Agent for analysis
        async for item in self.agent.stream(query, task.context_id):
            is_task_complete = item['is_task_complete']
            
            if not is_task_complete:
                # Update progress
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(
                        item['updates'],
                        task.context_id,
                        task.id
                    ),
                )
                continue
            
            # Task completed, output result
            await updater.add_artifact(
                [Part(root=TextPart(text=item['content']))],
                name='bug_analysis_report'
            )
            await updater.complete()
            break
    
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())
