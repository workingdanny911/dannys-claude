# F1: User Authentication - Design

## Overview

User authentication system design document

## Goals

- Secure login/signup
- JWT-based authentication
- Token refresh mechanism

## Non-Goals

- Social login (separate Feature)
- 2FA (separate Feature)

## API Design

### POST /api/auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

### POST /api/auth/signup

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "User Name"
}
```

**Response (201):**
```json
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

### POST /api/auth/refresh

**Request:**
```json
{
  "refreshToken": "eyJ..."
}
```

**Response (200):**
```json
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ..."  // rotated
}
```

## Security Considerations

- Password: bcrypt (cost factor 12)
- Access Token: 15 min validity
- Refresh Token: 7 day validity, rotation
- Rate limiting: Limit on login failures

## Dependencies

- jsonwebtoken
- bcrypt
- express-validator
