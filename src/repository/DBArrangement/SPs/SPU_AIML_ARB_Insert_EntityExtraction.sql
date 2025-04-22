DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_ARB_Insert_EntityExtraction`$$

CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_ARB_Insert_EntityExtraction`(
    IN  ip_ServiceID 		INT,
	IN 	ip_EntityInfo 		JSON,
    IN  ip_RunningTime      DECIMAL(4, 1),

    OUT op_ErrorMessage 	VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
	/*
		Created:	20251004@Leon.Pham
		Task:		Insert Entity Extraction [Redmine ID: #220692]
		DB:			SPU_AIML
		Original: 

		Revisions:
			- 20251004@Leon.Pham: Created [Redmine ID: #220692]
            
		Example:
			CALL SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Insert_EntityExtraction (201, '[{"Q":"I want to get Winlost Report day 10 for SportsBook", "E":"10/04/2025, SportsBook", "F":"/get_winlost_report"}]',1.52, @msg);    
	*/ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

	INSERT INTO SPU_AIML.ARB_EntityExtraction(ServiceID, Question, Entities, FunctionCalled, RunningTime, CreatedDate)
    SELECT  
        ip_ServiceID,  
        tmpTable.Question,
        tmpTable.Entities,
        tmpTable.FunctionCalled,
        ip_RunningTime,
        CURRENT_TIMESTAMP 
	FROM JSON_TABLE(ip_EntityInfo,
        "$[*]" COLUMNS(
            Question        TEXT PATH "$.Q",
            Entities        TEXT PATH "$.E",
            FunctionCalled  TEXT PATH "$.F"
        )
    ) AS tmpTable;
    
END$$
DELIMITER ;