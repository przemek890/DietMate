# DietMate
DietMate – Your Smart Diet Companion.  Plan meals, track calories, and balance nutrients effortlessly. Achieve your health goals with AI-powered recommendations. Eat smart, live better! 🍏

## Deployment (Not working yet !!!)

To deploy the application locally, you have two options:
1. Using VSCode extension (recommended for development)
2. Using Docker Compose

### 1. VSCode Extension Method

1. Install "Restore Terminals" extension in VSCode
2. Restart VSCode
3. The extension will automatically open terminals for:
    - Backend:
      ```bash
      cd backend
      python3 -m venv venv && source venv/bin/activate
      poetry install && python3.12 main.py
      ```
    - Frontend:
      ```bash
      cd frontend && npm start
      ```

**Access Points:**
- Local: `http://localhost:3000`
- Network: `http://<SERVER_IP>:3000`

***Note***: 
- This approach allows for automatic refreshing of the application in the browser after changes are made to the frontend code.
- Changes are immediately visible, which accelerates the development and testing process.
- Ideal for developers working on the frontend who need quick feedback

### 2. Docker Compose Method

Run all services with:
```bash
docker-compose up --build
```

**Access Points:**
- Local: `http://localhost:3000`
- Network: `http://<SERVER_IP>:3000`

***Note***:
- In this approach, after making changes to the frontend code, the frontend container must be restarted to see those changes.
- This means a longer response time when modifications are made, which can slow down the development process.
- May be beneficial during testing or preparation for deployment when application stability is a priority
