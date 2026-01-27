## **Social Media RESTful API Backend**
1. Designed and built a production-ready RESTful API using FastAPI to power a social media-like platform,
   supporting full CRUD operations for posts with ownership enforcement, user registration/authentication, and a voting/liking system.
2. Implementation of secure JWT-based authentication (OAuth2 password flow) with bcrypt password hashing using passlib and python-jose.
3. Integration of PostgreSQL database via SQLAlchemy ORM and Alembic migrations, modeling relational data (users, posts, votes) with complex joins,
   pagination, filtering, and search capabilities.
4. Deployed to DigitalOcean Ubuntu VPS with Nginx reverse proxy, Gunicorn/Uvicorn, and systemd management.

## API Endpoints
#### Posts
Method,Endpoint,Description,Auth Required,Parameters / Body,Response Example
GET,/posts,Get all posts with vote counts (paginated),No,"Query params: limit (default 10), skip (default 0), search (title substring)",List of posts with votes count
GET,/post/{id},Get a single post by ID with vote count,No,Path param: id,Single post object with votes
POST,/createpost,Create a new post,Yes,"json { ""title"": ""My Post"", ""content"": ""Post content"", ""published"": true }",Created post object
DELETE,/post/{id},Delete a post (owner only),Yes,Path param: id,No content (204)
PUT,/post/{id},Update a post (owner only),Yes,"Path param: id
Body: partial update json { ""title"": ""Updated"", ""content"": ""...""}",Updated post object
