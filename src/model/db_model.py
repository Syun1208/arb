import dataclasses

@dataclasses.dataclass
class DBModel:
    REQUEST_ID = 'request_id'
    QUESTION = "question"
    ENTITIES = "entities"
    FUNCTION_CALLED = "function_called"
    CREATED_DATE = "created_date"
    ARB_ENTITY_EXTRACTION = {
        QUESTION: "Q",
        ENTITIES: "E",
        FUNCTION_CALLED: "F"
    }
