-- script that creates a table users with attributes id, email and name. If users table exists, the script does not fail and can be executed on any database
CREATE TABLE IF NOT EXISTS users(
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id), 
  email VARCHAR(255) NOT NULL UNIQUE, 
  name VARCHAR(255)
);