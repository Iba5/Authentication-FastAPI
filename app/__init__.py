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
"""
=============================================================
 FASTAPI AUTHENTICATION PROJECT REVIEW (Score: 6.5 / 10)
=============================================================

SUMMARY:
--------
- Architecture: 7/10   ✅ Good layering
- Security:    5/10   ❌ Critical flaws
- Maintainability: 7/10 ✅ Readable code
- Scalability: 6/10   ⚠️ Needs optimization
- Documentation: 4/10 ❌ Sparse comments

KEY FLAWS TO FIX FIRST:
-----------------------
1. Email not unique in DB  ❌
2. Duplicate password field in schema ❌
3. Bare exception handling in JWT ❌
4. No rate limiting (brute force risk) ❌
5. Delete() refreshes deleted object ❌
6. No password strength validation ❌
7. Missing CORS/security headers ❌

=============================================================
 LIBRARIES USED
=============================================================
- FastAPI → routing, DI, docs
- SQLModel → ORM + validation
- PyJWT → JWT tokens
- Passlib[bcrypt] → password hashing
- Pydantic → schemas & env config
- python-decouple → environment variables

=============================================================
 FILE-BY-FILE REVIEW
=============================================================

1. main.py
----------
- ✅ Lifespan manager for DB init/close
- ⚠️ login() creates token before user validation
- ⚠️ SignIn() missing duplicate email/username check

2. config.py
------------
- ✅ Uses env vars
- ⚠️ No secret key strength validation
- ⚠️ Token duration default may be long

3. auth/hashing.py
------------------
- ✅ bcrypt for hashing
- ❌ Password truncated silently at 72 chars
- ❌ DB queries inside hashing module (bad separation)

FIX:
def VerifyHashedPwd(plain_pwd, hashed_pwd):
    return bcrypt.verify(plain_pwd, hashed_pwd)

4. auth/token.py
----------------
- ✅ Includes iat, exp claims
- ❌ Wrong responsibility: does user validation
- ❌ Bare except hides all errors
- ❌ No refresh tokens, no revocation

5. auth/authenticating.py
-------------------------
- ✅ Uses OAuth2PasswordBearer
- ⚠️ Always queries DB (no caching)
- ⚠️ Returns 404 instead of 401 when user missing

6. auth/authforms.py
--------------------
- ✅ Simplifies OAuth2 form
- ⚠️ Non-standard (not fully OAuth2 compliant)

7. models/table.py
------------------
- ❌ lowercase class name violates PEP8
- ❌ Email not unique
- ❌ No timestamps / account status fields

RECOMMENDED:
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    hashPwd: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

8. models/schemas.py
--------------------
- ❌ Duplicate password field
- ❌ No password/email validation
- ❌ Update schema wrongly includes "id"

RECOMMENDED:
class UserSignUp(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8: raise ValueError("Password too short")
        if not any(c.isdigit() for c in v): raise ValueError("Needs digit")
        return v

9. repository/dbcomm.py
-----------------------
- ✅ Good repository pattern
- ❌ Delete() refreshes deleted object
- ❌ No DB error handling
- ⚠️ Case-sensitive email lookup

FIX:
def Delete(self, id) -> bool:
    data = self.get_by_id(id)
    if not data: return False
    self.db.delete(data)
    self.db.commit()
    return True

10. service/serviceside.py
--------------------------
- ✅ Centralized business logic
- ❌ Update_User ignores "id" param (uses update.id)
- ❌ No duplicate check before user creation

11. controller/endpoints.py
---------------------------
- ✅ All routes protected by default
- ❌ AddUser endpoint available to any user (privilege escalation!)
- ❌ Bug: route "/Display/id" missing leading slash

=============================================================
 CRITICAL SECURITY VULNERABILITIES
=============================================================
- Email not unique
- Bare exception handling in JWT
- No rate limiting → brute force possible
- Silent password truncation at 72 chars
- No CORS headers → unsafe frontend usage
- No refresh tokens / revocation
- No account lockout → infinite retries

=============================================================
 RECOMMENDED FIXES (BEFORE PROD)
=============================================================
1. Make email unique in DB
2. Remove duplicate password schema field
3. Validate password strength
4. Fix Delete() refresh bug
5. Add proper JWT exception handling
6. Implement rate limiting (e.g., slowapi)
7. Add refresh tokens + revocation
8. Add CORS + security headers middleware

=============================================================
 NEXT STEPS
=============================================================
1. Apply fixes to models & schemas
2. Add password + email validation
3. Add rate limiting to login
4. Write unit tests for auth flow
5. Add structured logging
6. Add monitoring & error handling
7. Deploy with HTTPS + secure secrets

=============================================================
 OVERALL
=============================================================
This project is a good start but NOT production ready.
With fixes, can become 8–9/10.
Current rating: 6.5/10
"""
