from dependency_injector import containers, providers
from thespian.actors import ActorSystem

from src.service.implement.arb_supporter_impl.prompt_impl import NerAgentConfig, GreetingAgentConfig, GreetingRecognizerAgentConfig, ReportCallingAgentConfig, ConfirmationRecognizerAgentConfig, RemovalEntityDetectionAgentConfig

from src.service.interface.arb_slave_agent.greeting_agent import GreetingAgent
from src.service.implement.arb_slave_agent_impl.greeting_agent_impl import GreetingAgentImpl

from src.service.interface.arb_slave_agent.report_calling_agent import ReportCallingAgent
from src.service.implement.arb_slave_agent_impl.report_calling_agent_impl import ReportCallingAgentImpl

from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.llm_impl import LLMImpl

from src.service.interface.arb_slave_agent.recognizer_agent import RecognizerAgent
from src.service.implement.arb_slave_agent_impl.greeting_recognizer_agent_impl import GreetingRecognizerAgentImpl
from src.service.implement.arb_slave_agent_impl.confirmation_recognizer_agent_impl import ConfirmationRecognizerAgentImpl

from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.implement.arb_slave_agent_impl.ner_agent_impl import NerAgentImpl

from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.service.implement.arb_service_impl.arb_db_service_impl import ARBDBServiceImpl

from src.service.interface.arb_slave_agent.abbreviation_recognizer_agent import AbbreviationRecognizerAgent
from src.service.implement.arb_slave_agent_impl.abbreviation_recognizer_agent_impl import AbbreviationRecognizerAgentImpl

from src.service.interface.arb_slave_agent.removal_entity_detection_agent import RemovalEntityDetectionAgent
from src.service.implement.arb_slave_agent_impl.removal_entity_detection_agent_impl import RemovalEntityDetectionAgentImpl

from src.service.interface.arb_service.arb_vector_db_service import ARBVectorDBService
from src.service.implement.arb_service_impl.arb_vector_db_service_impl import ARBVectorDBServiceImpl

from src.service.interface.arb_master_agent.agent_composer import AgentComposer
from src.service.implement.arb_master_agent_impl.agent_composer_impl import AgentComposerImpl

from src.service.interface.arb_service.arb_service import ARBService
from src.service.implement.arb_service_impl.arb_service_impl import ARBServiceImpl

from src.service.interface.arb_service.arb_auth_service import ARBAuthService
from src.service.implement.arb_service_impl.arb_auth_service_impl import ARBAuthServiceImpl

from src.repository.DataAccess.data_access_connection import BaseRepository
from src.repository.DataAccess.data_access_connection import WasaAiMl


class ApplicationContainer(containers.DeclarativeContainer):
    # Set up to get config 
    service_config = providers.Configuration()
    report_config = providers.Configuration()
    
    actor_system = providers.Singleton(ActorSystem)

    wasa_aiml_connector = providers.AbstractSingleton(BaseRepository)
    wasa_aiml_connector.override(
        providers.Singleton(
            WasaAiMl,
            database_name=service_config.sql_config.aiml_mysql.database_name,
            username=service_config.sql_config.aiml_mysql.username,
            password=service_config.sql_config.aiml_mysql.password,
            host=service_config.sql_config.aiml_mysql.host,
            port=service_config.sql_config.aiml_mysql.port,
            dbms_name=service_config.sql_config.aiml_mysql.dbms_name,
        )
    )

    arb_db_service = providers.AbstractSingleton(ARBDBService)
    arb_db_service.override(
        providers.Singleton(
            ARBDBServiceImpl,
            service_id=service_config.default.service_id,
            nosql_connector=service_config.nosql_config.conversation_path,
            sql_connector=wasa_aiml_connector,
            expired_time=service_config.nosql_config.expired_time
        )
    )
    
    arb_auth_service = providers.AbstractSingleton(ARBAuthService)
    arb_auth_service.override(
        providers.Singleton(
            ARBAuthServiceImpl,
            service_id=service_config.default.service_id,
            wasa_aiml_connector=wasa_aiml_connector
        )
    )

    llm = providers.AbstractSingleton(LLM)
    llm.override(
        providers.Singleton(
            LLMImpl,
            api=service_config.llm_config.api,
        )
    )

    greeting_agent = providers.AbstractSingleton(GreetingAgent)
    greeting_agent.override(
        providers.Singleton(
            GreetingAgentImpl,
            llm=llm,
            model=service_config.greeting_agent_config.llm_model,
            name=service_config.greeting_agent_config.name,
            task_description=service_config.greeting_agent_config.task_description,
            report_config=report_config,
            agent_config=GreetingAgentConfig,
            tools=None
        )
    )
    

    confirmation_recognizer_agent = providers.AbstractSingleton(RecognizerAgent)
    confirmation_recognizer_agent.override(
        providers.Singleton(
            ConfirmationRecognizerAgentImpl,
            llm=llm,
            model=service_config.confirmation_recognizer_agent_config.llm_model,
            name=service_config.confirmation_recognizer_agent_config.name,
            task_description=service_config.confirmation_recognizer_agent_config.task_description,
            report_config=report_config,
            agent_config=ConfirmationRecognizerAgentConfig,
            tools=None
        )
    )
    
    removal_entity_detection_agent = providers.AbstractSingleton(RemovalEntityDetectionAgent)
    removal_entity_detection_agent.override(
        providers.Singleton(
            RemovalEntityDetectionAgentImpl,
            llm=llm,
            model=service_config.removal_entity_detection_agent_config.llm_model,
            name=service_config.removal_entity_detection_agent_config.name,
            task_description=service_config.removal_entity_detection_agent_config.task_description,
            report_config=report_config,
            agent_config=RemovalEntityDetectionAgentConfig,
            tools=None
        )
    )
    greeting_recognizer_agent = providers.AbstractSingleton(RecognizerAgent)
    greeting_recognizer_agent.override(
        providers.Singleton(
            GreetingRecognizerAgentImpl,
            llm=llm,
            model=service_config.greeting_recognizer_agent_config.llm_model,
            name=service_config.greeting_recognizer_agent_config.name,
            task_description=service_config.greeting_recognizer_agent_config.task_description,
            report_config=report_config,
            agent_config=GreetingRecognizerAgentConfig,
            tools=None
        )
    )
    
    ner_agent = providers.AbstractSingleton(NerAgent)
    ner_agent.override(
        providers.Singleton(
            NerAgentImpl,
            llm=llm,
            model=service_config.ner_agent_config.llm_model,
            name=service_config.ner_agent_config.name,
            task_description=service_config.ner_agent_config.task_description,
            report_config=report_config,
            agent_config=NerAgentConfig,
            tools=None
        )
    )
    
    report_calling_agent = providers.AbstractSingleton(ReportCallingAgent)
    report_calling_agent.override(
        providers.Singleton(
            ReportCallingAgentImpl,
            llm=llm,
            model=service_config.report_calling_agent_config.llm_model,
            name=service_config.report_calling_agent_config.name,
            task_description=service_config.report_calling_agent_config.task_description,
            report_config=report_config,
            agent_config=ReportCallingAgentConfig,
            tools=None
        )
    )
    
    report_vector_db = providers.AbstractSingleton(ARBVectorDBService)
    report_vector_db.override(
        providers.Singleton(
            ARBVectorDBServiceImpl,
            path_save=service_config.vector_db_config.path_save.report,
            num_workers=service_config.vector_db_config.num_workers
        )
    )
    
    entity_vector_db = providers.AbstractSingleton(ARBVectorDBService)
    entity_vector_db.override(
        providers.Singleton(
            ARBVectorDBServiceImpl,
            path_save=service_config.vector_db_config.path_save.entity,
            num_workers=service_config.vector_db_config.num_workers
        )
    )
    
    abbreviation_recognizer_agent = providers.AbstractSingleton(AbbreviationRecognizerAgent)
    abbreviation_recognizer_agent.override(
        providers.Singleton(
            AbbreviationRecognizerAgentImpl,
            report_vector_db=report_vector_db,
            entity_vector_db=entity_vector_db,
            top_k=service_config.abbreviation_recognizer_agent_config.top_k,
            report_config=report_config,
            num_workers=service_config.abbreviation_recognizer_agent_config.num_workers
        )
    )
    agent_composer = providers.AbstractSingleton(AgentComposer)
    agent_composer.override(
        providers.Singleton(
            AgentComposerImpl,
            greeting_agent=greeting_agent,
            confirmation_recognizer_agent=confirmation_recognizer_agent,
            removal_entity_detection_agent=removal_entity_detection_agent,
            ner_agent=ner_agent,
            report_calling_agent=report_calling_agent,
            greeting_recognizer_agent=greeting_recognizer_agent,
            abbreviation_recognizer_agent=abbreviation_recognizer_agent,
            database=arb_db_service,
            num_workers=service_config.default.spec.num_workers
        )
    )
    
    arb_service = providers.AbstractSingleton(ARBService)
    arb_service.override(
        providers.Singleton(
            ARBServiceImpl,
            agent_composer=agent_composer
        )
    )
    
    