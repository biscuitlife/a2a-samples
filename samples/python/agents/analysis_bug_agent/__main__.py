import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import AnalysisBugAgentExecutor
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=10003)
def main(host, port):
    try:
        capabilities = AgentCapabilities(
            streaming=False,
        )
        
        skill = AgentSkill(
            id='analyze_bug',
            name='Bug Analysis Tool',
            description='Analyze code errors and provide detailed error reports with line number location and fix suggestions',
            tags=['debug', 'code-analysis', 'error-analysis'],
            examples=[
                'Analyze this file error: /path/to/file.py, error message: NameError: name "x" is not defined',
                'Help me check what\'s wrong with this code: main.py, error: IndexError: list index out of range',
            ],
        )
        
        agent_card = AgentCard(
            name='Analysis Bug Agent',
            description='Professional code error analysis Agent that can read local code files, analyze error stacks, locate error line numbers, and provide detailed fix suggestions and code examples',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=['text/plain'],
            default_output_modes=['text/plain'],
            capabilities=capabilities,
            skills=[skill],
        )
        
        agent_executor = AnalysisBugAgentExecutor()
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )
        
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )
        
        import uvicorn
        
        logger.info(f"🚀 Starting Analysis Bug Agent at http://{host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)
        
    except Exception as e:
        logger.error(f'Service startup failed: {e}')
        exit(1)


if __name__ == '__main__':
    main()
