USE SPU_AIML;

DROP TABLE IF EXISTS ARB_APIKeyManagement;
CREATE TABLE `ARB_APIKeyManagement` (
  `DepartmentID`   INT NOT NULL,
  `APIKey`         VARCHAR(255) NOT NULL,
  `CreatedDate`    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`DepartmentID`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS ARB_EntityExtraction;
CREATE TABLE `ARB_EntityExtraction` (
  `RequestID`       BIGINT AUTO_INCREMENT,
  `ServiceID`       INT NOT NULL,
  `Question`        VARCHAR(255) NOT NULL,
  `Entities`        VARCHAR(255),
  `FunctionCalled`  VARCHAR(255),
  `RunningTime`     DECIMAL(4, 2) NOT NULL,
  `CreatedDate`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`RequestID`, `ServiceID`)
) ENGINE=InnoDB;
