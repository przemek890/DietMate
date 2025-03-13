# DietMate
DietMate – Your Smart Diet Companion.  Plan meals, track calories, and balance nutrients effortlessly. Achieve your health goals with AI-powered recommendations. Eat smart, live better! 🍏

---

### Quick Start

Before running the application, configure the following environment variables in your shell:

```bash
REACT_APP_DOMAIN=http://localhost # This will be replaced with domain in production
```
```bash
# For cloud database:
MONGO_CONNECTION_STRING=mongodb+srv://admin:admin@dietmate.gzxwa.mongodb.net/
# OR for local database:
MONGO_CONNECTION_STRING=mongodb://admin:admin@mongodb:27017/
```

```bash
# Get your API key at https://console.groq.com/keys
GROQ_API_KEY=<<API_KEY>>
```

These variables are essential for proper application functionality. Set them in your host shell environment before proceeding with deployment.


### How to Run

There are two main methods to run DietMate:

1. Using VSCode Extension (recommended for development)
2. Using Docker Compose (recommended for production)

#### 1. VSCode Extension Method

1. Install "Restore Terminals" extension in VSCode
2. Restart VSCode
3. The extension will automatically run application.

#### 2. Docker Compose Method

Run all services with:
```bash
docker-compose up --build
```



