DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey`$$

CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey`(
    IN  ip_APIKey 		    VARCHAR(255),

    OUT op_ErrorMessage 	VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
	/*
		Created:	20251004@Leon.Pham
		Task:		Authenticate API Key [Redmine ID: #220692]
		DB:			SPU_AIML
		Original: 

		Revisions:
			- 20251004@Leon.Pham: Created [Redmine ID: #220692]
            
		Example:
			CALL SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey ('v_QFvFqLcIxgfWTnbzkRCI0D1w85q5pTaSvHppul4kM', @msg); 
	*/ 

	DECLARE lv_TmpDepartmentID INT;
    DECLARE op_DepartmentID     INT;
    DECLARE op_IsAuthenticated  BOOLEAN;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

    SELECT DepartmentID INTO lv_TmpDepartmentID
    FROM SPU_AIML.ARB_APIKeyManagement
    WHERE APIKey = ip_APIKey;

    IF lv_TmpDepartmentID IS NOT NULL THEN
        SET op_IsAuthenticated = TRUE;
        SET op_DepartmentID = lv_TmpDepartmentID;
    ELSE
        SET op_IsAuthenticated = FALSE;
        SET op_DepartmentID = NULL;
    END IF;

    DROP TABLE IF EXISTS Temp_AuthenticateAPIKey;
    CREATE TEMPORARY TABLE Temp_AuthenticateAPIKey(
		DepartmentID INT NOT NULL,
        IsAuthenticated BOOLEAN NOT NULL
	);

    INSERT INTO Temp_AuthenticateAPIKey (DepartmentID, IsAuthenticated)
    VALUES (op_DepartmentID, op_IsAuthenticated);

    SELECT DepartmentID, IsAuthenticated 
    FROM Temp_AuthenticateAPIKey;

    DROP TABLE Temp_AuthenticateAPIKey;
END$$
DELIMITER ;