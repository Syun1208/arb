DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_ARB_APIKeyManagement_Insert_APIKey`$$

CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_ARB_APIKeyManagement_Insert_APIKey`(
    IN  ip_DepartmentID 		INT,
	IN 	ip_APIKey 		        VARCHAR(255),

    OUT op_ErrorMessage 	    VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
	/*
		Created:	20251004@Leon.Pham
		Task:		Insert API Key [Redmine ID: #220692]
		DB:			SPU_AIML
		Original: 

		Revisions:
			- 20251004@Leon.Pham: Created [Redmine ID: #220692]
            
		Example:
			CALL SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Insert_APIKey (1, 'mgkgh#ebg82935bn2i-jk@biesbg',@msg);    
	*/ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

	INSERT INTO SPU_AIML.ARB_APIKeyManagement(DepartmentID, APIKey, CreatedDate)
    VALUES(  
        ip_DepartmentID,  
        ip_APIKey,
        CURRENT_TIMESTAMP
    );
	
    
END$$
DELIMITER ;