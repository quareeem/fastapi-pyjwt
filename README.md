# FastAPI JWT Authentication with RSA

This project demonstrates how to implement JWT (JSON Web Token) authentication using RSA digital signatures in a FastAPI application. It includes endpoints for user login and accessing protected resources, with JWTs to ensure secure and stateless authentication.

## Features

- **User Login**: Endpoint for user authentication that returns a JWT upon successful login.
- **Protected Endpoint**: A demonstration of securing an endpoint that requires a valid JWT to access.
- **RSA Signatures**: Utilizes RSA to sign and verify JWTs, ensuring the integrity and authenticity of the tokens.

## Technologies Used

- FastAPI
- PyJWT
- SQLAlchemy
- SQLite

## Project Structure

/src
/config # Configuration files and environment variables
/models # Database models
/schemas # Pydantic models for request and response data
/services # Business logic and data access layer
/utils # Utility functions such as JWT encode and decode

main.py # FastAPI application setup and routes
requirements.txt # Project dependencies

### Launch

# install req
'''
pip install -r requirements.txt
'''

# generate keys
'''
openssl genpkey -algorithm RSA -out jwt-private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in jwt-private.pem -out jwt-public.pem
'''

# launch the app
'''
uvicorn main:app --reload
'''
