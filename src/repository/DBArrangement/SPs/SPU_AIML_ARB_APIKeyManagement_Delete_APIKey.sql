DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_ARB_APIKeyManagement_Delete_APIKey`$$

CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_ARB_APIKeyManagement_Delete_APIKey`(
    IN  ip_DepartmentID 	INT,

    OUT op_ErrorMessage 	VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
	/*
		Created:	20251004@Leon.Pham
		Task:		Delete API Key [Redmine ID: #220692]
		DB:			SPU_AIML
		Original: 

		Revisions:
			- 20251004@Leon.Pham: Created [Redmine ID: #220692]
            
		Example:
			CALL SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Delete_APIKey(1, @msg);    
	*/ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

    DELETE FROM SPU_AIML.ARB_APIKeyManagement
    WHERE DepartmentID = ip_DepartmentID;
    
END$$
DELIMITER ;