"""
How the Auth takes place

        +----------------+
        |   User Login   |
        +----------------+
                |
        (Submit email/password)
                |
        +----------------+
        |   Verify Hash  |  <- bcrypt/Argon2
        +----------------+
                |
        (If valid)
                |
        +----------------+
        | Generate JWT   |  <- payload: user_id, roles, scopes, exp
        +----------------+
                |
        (Return to client)
                |
        +----------------+          +---------------------+
        | Client Sends   |  ---->   | FastAPI Dependency  |
        | JWT in Header  |          | decode + validate   |
        +----------------+          +---------------------+
                                           |
                                  +---------------------+
                                  | Extract user info   | 
                                  | roles, scopes, sub  |
                                  +---------------------+
                                           |
                                  +---------------------+
                                  | Authorization Check | 
                                  | RBAC / Scope Check  |
                                  +---------------------+
                                           |
                                  +---------------------+
                                  | Execute endpoint    |
                                  | or return 403/401   |
                                  +---------------------+

"""