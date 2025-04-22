DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_ARB_APIKeyManagement_Update_APIKey`$$


CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_ARB_APIKeyManagement_Update_APIKey`(    
    IN  ip_DepartmentID      INT,
    IN  ip_APIKey            VARCHAR(255),
    
    OUT op_ErrorMessage     VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
    /*
        Created:    20250601@Leon.Pham
        Task:       Update API Key [Redmine ID: #220692]
        DB:         SPU_AIML
        Original: 

        Revisions:
            - 20250601@Leon.Pham: Created [Redmine ID: #220692]
            
        Example:call SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Update_APIKey(1, 'mgkgh#ebg82935bn2i-jk@biesbg',@msg);    
            
    */ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

    UPDATE SPU_AIML.ARB_APIKeyManagement
    SET APIKey = ip_APIKey
    WHERE DepartmentID = ip_DepartmentID;
END
