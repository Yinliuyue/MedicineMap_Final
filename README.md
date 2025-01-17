To run the application, follow these steps:

1. Navigate to the `backend` folder and run `app.py`.
2. Go to the `frontend` folder and run `npm run serve`.

Each time you use the application, you need to change the CORS path in `backend/app.py` to the path where the frontend is running. Specifically, modify the line `CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://10.21.169.215:8080"}})` to use the network path instead of `http://10.21.169.215:8080`.
