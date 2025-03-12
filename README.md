# DietMate
DietMate – Your Smart Diet Companion.  Plan meals, track calories, and balance nutrients effortlessly. Achieve your health goals with AI-powered recommendations. Eat smart, live better! 🍏

---

### Deployment

#### 1. VSCode Extension Method

1. Install "Restore Terminals" extension in VSCode
2. Restart VSCode
3. The extension will automatically run application.

**Access Points:**
- Local: `http://localhost:3000`
- Network: `http://<SERVER_IP>:3000`

***Note***: 
- This approach allows for automatic refreshing of the application in the browser after changes are made to the frontend code.
- Changes are immediately visible, which accelerates the development and testing process.
- Ideal for developers working on the frontend who need quick feedback

#### 2. Docker Compose Method

Run all services with:
```bash
docker-compose up --build
```

You can choose between local or cloud database source:
[5-6 docker-compose.yml](./docker-compose.yml#L5-L6)

**Access Points:**
- Local: `http://localhost:3000`
- Network: `http://<SERVER_IP>:3000`

***Note***:
- In this approach, after making changes to the frontend code, the frontend container must be restarted to see those changes.
- This means a longer response time when modifications are made, which can slow down the development process.
- May be beneficial during testing or preparation for deployment when application stability is a priority
