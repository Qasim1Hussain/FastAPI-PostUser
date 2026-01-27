Social Media RESTful API Backend
1. Designed and built a production-ready RESTful API using FastAPI to power a social media-like platform,
   supporting full CRUD operations for posts with ownership enforcement, user registration/authentication, and a voting/liking system.
2. Implementation of secure JWT-based authentication (OAuth2 password flow) with bcrypt password hashing using passlib and python-jose.
3. Integration of PostgreSQL database via SQLAlchemy ORM and Alembic migrations, modeling relational data (users, posts, votes) with complex joins,
   pagination, filtering, and search capabilities.
4. Deployed to DigitalOcean Ubuntu VPS with Nginx reverse proxy, Gunicorn/Uvicorn, and systemd management.
