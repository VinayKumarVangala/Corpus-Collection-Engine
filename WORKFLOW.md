# Workflow Documentation - Corpus Collection Engine

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Design](#architecture-design)
3. [API Integration Workflow](#api-integration-workflow)
4. [Frontend-Backend Connectivity](#frontend-backend-connectivity)
5. [Database Operations](#database-operations)
6. [File Upload & Processing](#file-upload--processing)
7. [Authentication Flow](#authentication-flow)
8. [Development Workflow](#development-workflow)
9. [Deployment Pipeline](#deployment-pipeline)
10. [Testing Strategy](#testing-strategy)
11. [Performance Optimization](#performance-optimization)
12. [Security Implementation](#security-implementation)

---

## Project Overview

The Corpus Collection Engine is a full-stack web application built with Streamlit frontend and Python backend, designed to collect and preserve Indian cultural heritage through multi-media contributions.

### Technology Stack
- **Frontend**: Streamlit (Python-based web framework)
- **Backend**: Python with SQLite/PostgreSQL
- **Authentication**: JWT + bcrypt
- **File Storage**: Local filesystem with cloud storage ready
- **API**: RESTful design with FastAPI integration ready
- **Deployment**: Hugging Face Spaces, Docker containers

---

## Architecture Design

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Streamlit)   │◄──►│   (Python)      │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Storage  │    │   Auth Service  │    │   API Gateway   │
│   (Local/Cloud) │    │   (JWT/bcrypt)  │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Breakdown

#### 1. Frontend Layer (Streamlit)
- **Purpose**: User interface and interaction
- **Components**:
  - Authentication pages (login/register)
  - Category selection interface
  - File upload forms
  - Dashboard analytics
  - Browse/search functionality

#### 2. Backend Layer (Python)
- **Purpose**: Business logic and data processing
- **Components**:
  - User management
  - File processing and validation
  - Database operations
  - API endpoints (future)

#### 3. Data Layer
- **Purpose**: Data persistence and retrieval
- **Components**:
  - User profiles and authentication
  - Contribution metadata
  - File storage references

---

## API Integration Workflow

### Current Implementation (Local)
```python
# Direct function calls within the application
from utils.database import db
from utils.auth import hash_password, verify_password
from utils.file_handler import save_file, validate_file

# Example usage
user = db.get_user_by_email(email)
contribution = db.create_contribution(data)
```

### Future API Integration (RESTful)
```python
# API client implementation
import requests
from config import API_BASE_URL, API_VERSION

class APIClient:
    def __init__(self):
        self.base_url = f"{API_BASE_URL}/{API_VERSION}"
        self.session = requests.Session()
    
    def authenticate(self, email, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            return True
        return False
    
    def create_contribution(self, contribution_data):
        response = self.session.post(
            f"{self.base_url}/contributions",
            json=contribution_data
        )
        return response.json()
    
    def upload_file(self, file_data, contribution_id):
        files = {"file": file_data}
        response = self.session.post(
            f"{self.base_url}/contributions/{contribution_id}/upload",
            files=files
        )
        return response.json()
```

### API Endpoints Design
```
POST   /api/v1/auth/register          # User registration
POST   /api/v1/auth/login             # User login
POST   /api/v1/auth/refresh           # Token refresh
GET    /api/v1/users/profile          # Get user profile
PUT    /api/v1/users/profile          # Update profile

GET    /api/v1/categories             # List categories
POST   /api/v1/contributions          # Create contribution
GET    /api/v1/contributions          # List contributions
GET    /api/v1/contributions/{id}     # Get specific contribution
PUT    /api/v1/contributions/{id}     # Update contribution
DELETE /api/v1/contributions/{id}     # Delete contribution

POST   /api/v1/files/upload           # Upload file
GET    /api/v1/files/{id}             # Download file
DELETE /api/v1/files/{id}             # Delete file

GET    /api/v1/analytics/dashboard    # Dashboard data
GET    /api/v1/search                 # Search contributions
```

---

## Frontend-Backend Connectivity

### Current Architecture (Monolithic)
```python
# Direct database access from Streamlit
def show_contribute():
    # Form handling
    with st.form("contribution_form"):
        # ... form fields ...
        
        if submit:
            # Direct database call
            contribution_data = {...}
            db.create_contribution(contribution_data)
            st.success("Contribution saved!")
```

### Recommended Architecture (API-based)
```python
# API client integration
class ContributionService:
    def __init__(self, api_client):
        self.api = api_client
    
    async def create_contribution(self, form_data):
        try:
            # Validate data
            validated_data = self.validate_contribution(form_data)
            
            # Create contribution via API
            response = await self.api.create_contribution(validated_data)
            
            # Handle file upload if present
            if form_data.get('file'):
                await self.api.upload_file(
                    form_data['file'], 
                    response['contribution_id']
                )
            
            return response
        except Exception as e:
            logger.error(f"Contribution creation failed: {e}")
            raise

# Streamlit integration
def show_contribute():
    service = ContributionService(api_client)
    
    with st.form("contribution_form"):
        # ... form fields ...
        
        if submit:
            with st.spinner("Saving contribution..."):
                try:
                    result = asyncio.run(
                        service.create_contribution(form_data)
                    )
                    st.success("Contribution saved successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
```

### State Management
```python
# Session state management for API integration
class SessionManager:
    @staticmethod
    def initialize_session():
        if 'api_client' not in st.session_state:
            st.session_state.api_client = APIClient()
        if 'user_token' not in st.session_state:
            st.session_state.user_token = None
    
    @staticmethod
    def set_user_session(user_data, token):
        st.session_state.user_id = user_data['id']
        st.session_state.user_email = user_data['email']
        st.session_state.user_token = token
        st.session_state.api_client.set_token(token)
    
    @staticmethod
    def clear_session():
        for key in ['user_id', 'user_email', 'user_token']:
            if key in st.session_state:
                del st.session_state[key]
```

---

## Database Operations

### Current Schema (SQLite)
```sql
-- Users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contributions table
CREATE TABLE contributions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    media_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    language TEXT NOT NULL,
    file_path TEXT,
    file_hash TEXT,
    file_size INTEGER,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Database Operations Workflow
```python
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def create_contribution(self, contribution_data):
        """Create new contribution with transaction safety"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # Validate user exists
            cursor.execute("SELECT id FROM users WHERE id = ?", 
                         (contribution_data['user_id'],))
            if not cursor.fetchone():
                raise ValueError("User not found")
            
            # Insert contribution
            cursor.execute("""
                INSERT INTO contributions 
                (id, user_id, category, media_type, title, description, 
                 language, file_path, file_hash, file_size, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contribution_data['id'],
                contribution_data['user_id'],
                contribution_data['category'],
                contribution_data['media_type'],
                contribution_data['title'],
                contribution_data.get('description', ''),
                contribution_data['language'],
                contribution_data.get('file_path', ''),
                contribution_data.get('file_hash', ''),
                contribution_data.get('file_size', 0),
                contribution_data.get('is_public', False)
            ))
            
            conn.commit()
            return contribution_data['id']
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
```

### Migration to PostgreSQL (Production)
```python
# PostgreSQL configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
    'database': os.getenv('DB_NAME', 'corpus_db'),
    'user': os.getenv('DB_USER', 'corpus_user'),
    'password': os.getenv('DB_PASSWORD', 'secure_password')
}

class PostgreSQLManager:
    def __init__(self, config):
        self.config = config
        self.pool = None
    
    async def initialize_pool(self):
        self.pool = await asyncpg.create_pool(**self.config)
    
    async def create_contribution(self, contribution_data):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Insert with RETURNING clause
                result = await conn.fetchrow("""
                    INSERT INTO contributions 
                    (id, user_id, category, media_type, title, description, 
                     language, file_path, file_hash, file_size, is_public)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    RETURNING id, created_at
                """, *contribution_data.values())
                
                return dict(result)
```

---

## File Upload & Processing

### File Upload Workflow
```
1. Client selects file
2. Frontend validates file type/size
3. File is processed (sanitization, compression)
4. File is uploaded to storage
5. Metadata is saved to database
6. Success/error response to user
```

### Implementation
```python
class FileProcessor:
    def __init__(self, storage_path, max_sizes):
        self.storage_path = Path(storage_path)
        self.max_sizes = max_sizes
    
    def process_upload(self, file, contribution_id, media_type):
        """Complete file processing workflow"""
        try:
            # Step 1: Validate file
            self.validate_file(file, media_type)
            
            # Step 2: Generate secure filename
            filename = self.generate_filename(file, contribution_id)
            
            # Step 3: Process based on media type
            processed_file = self.process_by_type(file, media_type)
            
            # Step 4: Save to storage
            file_path = self.save_file(processed_file, filename)
            
            # Step 5: Generate metadata
            metadata = self.generate_metadata(file, file_path)
            
            return {
                'file_path': str(file_path),
                'file_hash': metadata['hash'],
                'file_size': metadata['size'],
                'mime_type': metadata['mime_type']
            }
            
        except Exception as e:
            logger.error(f"File processing failed: {e}")
            raise
    
    def process_by_type(self, file, media_type):
        """Type-specific processing"""
        if media_type.lower() == 'image':
            return self.process_image(file)
        elif media_type.lower() == 'audio':
            return self.process_audio(file)
        elif media_type.lower() == 'video':
            return self.process_video(file)
        else:
            return file
    
    def process_image(self, image_file):
        """Image processing with EXIF removal"""
        from PIL import Image
        
        img = Image.open(image_file)
        
        # Remove EXIF data
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(list(img.getdata()))
        
        # Optimize for web
        if img.mode in ('RGBA', 'LA'):
            clean_img = clean_img.convert('RGB')
        
        # Save to bytes
        output = BytesIO()
        clean_img.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output
```

### Chunked Upload (Large Files)
```python
class ChunkedUploader:
    def __init__(self, chunk_size=1024*1024):  # 1MB chunks
        self.chunk_size = chunk_size
    
    def upload_large_file(self, file, contribution_id):
        """Handle large file uploads in chunks"""
        file_id = str(uuid.uuid4())
        chunks = []
        
        try:
            # Read file in chunks
            while True:
                chunk = file.read(self.chunk_size)
                if not chunk:
                    break
                
                chunk_id = self.save_chunk(chunk, file_id, len(chunks))
                chunks.append(chunk_id)
            
            # Reassemble file
            final_path = self.reassemble_chunks(chunks, file_id, contribution_id)
            
            # Cleanup chunks
            self.cleanup_chunks(chunks)
            
            return final_path
            
        except Exception as e:
            # Cleanup on error
            self.cleanup_chunks(chunks)
            raise e
```

---

## Authentication Flow

### JWT Authentication Workflow
```
1. User submits credentials
2. Server validates credentials
3. Server generates JWT token
4. Token sent to client
5. Client stores token securely
6. Token included in subsequent requests
7. Server validates token on each request
```

### Implementation
```python
class AuthenticationService:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def authenticate_user(self, email, password):
        """Authenticate user and return token"""
        # Get user from database
        user = db.get_user_by_email(email)
        if not user:
            raise AuthenticationError("User not found")
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            raise AuthenticationError("Invalid password")
        
        # Generate token
        token_data = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
        
        return {
            'access_token': token,
            'token_type': 'bearer',
            'expires_in': 86400,  # 24 hours
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name']
            }
        }
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
```

### Session Management in Streamlit
```python
def require_authentication(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('user_id'):
            st.warning("Please login to access this feature")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

@require_authentication
def show_dashboard():
    # Dashboard code here
    pass
```

---

## Development Workflow

### Local Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd corpus-collection-engine

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Initialize database
python -c "from utils.database import db; db.init_database()"

# 6. Run application
python run.py
```

### Development Commands
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .

# Run tests
pytest tests/ -v --cov=utils

# Build package
python -m build

# Run with debug
DEBUG=true python run.py
```

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Create merge request
# After review and approval, merge to main

# Release tagging
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

---

## Deployment Pipeline

### Hugging Face Spaces Deployment
```yaml
# .github/workflows/deploy.yml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install huggingface_hub
      
      - name: Deploy to HF Spaces
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python scripts/deploy_hf.py
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "enhanced_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Production Configuration
```python
# config/production.py
import os

class ProductionConfig:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # File Storage
    STORAGE_BACKEND = 'cloud'  # 'local' or 'cloud'
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Performance
    REDIS_URL = os.getenv('REDIS_URL')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    
    # Monitoring
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    LOG_LEVEL = 'INFO'
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_auth.py
import pytest
from utils.auth import hash_password, verify_password, create_jwt_token

class TestAuthentication:
    def test_password_hashing(self):
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
    
    def test_jwt_token_creation(self):
        user_id = "test_user_123"
        email = "test@example.com"
        
        token = create_jwt_token(user_id, email)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
```

### Integration Tests
```python
# tests/test_integration.py
import pytest
from utils.database import db
from utils.file_handler import save_file

class TestIntegration:
    def setup_method(self):
        # Setup test database
        self.test_db = db
        self.test_db.init_database()
    
    def test_contribution_workflow(self):
        # Create test user
        user_id = "test_user"
        user_data = {
            'id': user_id,
            'email': 'test@example.com',
            'name': 'Test User',
            'password_hash': 'hashed_password'
        }
        self.test_db.create_user(**user_data)
        
        # Create contribution
        contribution_data = {
            'id': 'test_contribution',
            'user_id': user_id,
            'category': 'Culture',
            'media_type': 'Text',
            'title': 'Test Contribution',
            'language': 'English',
            'is_public': True
        }
        
        result = self.test_db.create_contribution(contribution_data)
        assert result is not None
        
        # Verify contribution exists
        contributions = self.test_db.get_user_contributions(user_id)
        assert len(contributions) == 1
        assert contributions[0]['title'] == 'Test Contribution'
```

### Performance Tests
```python
# tests/test_performance.py
import time
import pytest
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    def test_concurrent_uploads(self):
        """Test system under concurrent load"""
        def upload_file():
            # Simulate file upload
            start_time = time.time()
            # ... upload logic ...
            return time.time() - start_time
        
        # Test with 10 concurrent uploads
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(upload_file) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # Assert all uploads completed within reasonable time
        assert all(result < 5.0 for result in results)  # 5 seconds max
        assert sum(results) / len(results) < 2.0  # Average under 2 seconds
```

---

## Performance Optimization

### Caching Strategy
```python
# utils/cache.py
import functools
import time
from typing import Any, Dict

class SimpleCache:
    def __init__(self, ttl=300):  # 5 minutes default
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            if time.time() - self.cache[key]['timestamp'] < self.ttl:
                return self.cache[key]['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }

# Usage with decorator
cache = SimpleCache()

def cached(ttl=300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        return wrapper
    return decorator

@cached(ttl=600)  # Cache for 10 minutes
def get_public_contributions(category=None, media_type=None):
    return db.get_public_contributions(category, media_type)
```

### Database Optimization
```python
# Database connection pooling
class DatabasePool:
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connections = []
        self.in_use = set()
    
    def get_connection(self):
        # Reuse existing connection or create new one
        for conn in self.connections:
            if conn not in self.in_use:
                self.in_use.add(conn)
                return conn
        
        if len(self.connections) < self.pool_size:
            conn = sqlite3.connect(self.db_path)
            self.connections.append(conn)
            self.in_use.add(conn)
            return conn
        
        raise Exception("No available connections")
    
    def return_connection(self, conn):
        self.in_use.discard(conn)

# Query optimization
def get_user_contributions_optimized(user_id, limit=50, offset=0):
    """Optimized query with pagination"""
    query = """
        SELECT id, title, category, media_type, created_at, file_size, is_public
        FROM contributions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """
    return db.execute_query(query, (user_id, limit, offset))
```

### File Processing Optimization
```python
# Asynchronous file processing
import asyncio
import aiofiles

class AsyncFileProcessor:
    async def process_multiple_files(self, files):
        """Process multiple files concurrently"""
        tasks = []
        for file in files:
            task = asyncio.create_task(self.process_single_file(file))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def process_single_file(self, file):
        """Process single file asynchronously"""
        async with aiofiles.open(file.path, 'rb') as f:
            content = await f.read()
        
        # Process content
        processed = await self.process_content(content)
        
        # Save processed file
        output_path = self.get_output_path(file)
        async with aiofiles.open(output_path, 'wb') as f:
            await f.write(processed)
        
        return output_path
```

---

## Security Implementation

### Input Validation
```python
# utils/validation.py
from typing import Dict, Any
import re

class InputValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_contribution_data(data: Dict[str, Any]) -> Dict[str, str]:
        errors = {}
        
        # Required fields
        required_fields = ['title', 'category', 'media_type', 'language']
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field} is required"
        
        # Title length
        if data.get('title') and len(data['title']) > 200:
            errors['title'] = "Title must be less than 200 characters"
        
        # Category validation
        valid_categories = ['Culture', 'Food', 'Music', 'Literature', ...]
        if data.get('category') not in valid_categories:
            errors['category'] = "Invalid category"
        
        return errors
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', text)
        # Limit length
        return sanitized[:1000]
```

### Rate Limiting
```python
# utils/rate_limiter.py
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=100, window_seconds=3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False

# Usage in Streamlit
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)  # 10 per minute

def check_rate_limit():
    user_id = st.session_state.get('user_id', 'anonymous')
    if not rate_limiter.is_allowed(user_id):
        st.error("Rate limit exceeded. Please try again later.")
        st.stop()
```

### Security Headers and Configuration
```python
# Security configuration
SECURITY_CONFIG = {
    'password_min_length': 8,
    'password_require_special': True,
    'session_timeout_hours': 24,
    'max_login_attempts': 5,
    'lockout_duration_minutes': 15,
    'jwt_expiry_hours': 24,
    'file_scan_enabled': True,
    'max_file_size_mb': 100
}

class SecurityManager:
    def __init__(self, config):
        self.config = config
        self.failed_attempts = defaultdict(list)
    
    def check_password_strength(self, password: str) -> List[str]:
        errors = []
        
        if len(password) < self.config['password_min_length']:
            errors.append(f"Password must be at least {self.config['password_min_length']} characters")
        
        if self.config['password_require_special']:
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append("Password must contain at least one special character")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        return errors
    
    def is_account_locked(self, identifier: str) -> bool:
        now = time.time()
        attempts = self.failed_attempts[identifier]
        
        # Clean old attempts
        cutoff = now - (self.config['lockout_duration_minutes'] * 60)
        recent_attempts = [attempt for attempt in attempts if attempt > cutoff]
        self.failed_attempts[identifier] = recent_attempts
        
        return len(recent_attempts) >= self.config['max_login_attempts']
```

---

## Conclusion

This workflow documentation provides a comprehensive guide for understanding, developing, and maintaining the Corpus Collection Engine. It covers all aspects from architecture design to security implementation, serving as a reference for developers, contributors, and learners.

### Key Takeaways

1. **Modular Architecture**: The system is designed with clear separation of concerns
2. **API-Ready**: Current implementation can be easily extended to support RESTful APIs
3. **Security-First**: Multiple layers of security from authentication to file processing
4. **Scalable Design**: Architecture supports scaling from local development to production
5. **Performance Optimized**: Caching, async processing, and database optimization strategies
6. **Testing Coverage**: Comprehensive testing strategy for reliability
7. **Documentation**: Well-documented codebase for maintainability

### Next Steps for Learners

1. **Start with Local Setup**: Follow the development workflow to set up locally
2. **Understand the Flow**: Trace through a complete contribution workflow
3. **Experiment with APIs**: Implement the API client for backend communication
4. **Add Features**: Contribute new features following the established patterns
5. **Optimize Performance**: Implement caching and async processing
6. **Enhance Security**: Add additional security measures and validation
7. **Deploy to Production**: Set up production deployment with proper configuration

This documentation serves as a living guide that should be updated as the system evolves and new features are added.