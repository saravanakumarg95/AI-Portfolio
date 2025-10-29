# AI Portfolio

This project is an AI Portfolio application that utilizes a backend built with Flask and a frontend built with React. The backend serves as an API for generating images using the Stable Diffusion model, while the frontend provides a user interface for interacting with the API.

## Project Structure

```
ai-portfolio
├── backend
│   ├── app.py                # Main application file for the backend
│   ├── requirements.txt      # Python dependencies for the backend
│   └── README.md             # Documentation for the backend
├── frontend
│   ├── src
│   │   ├── components        # React components for the frontend
│   │   ├── pages             # Different pages of the frontend
│   │   └── App.js            # Main entry point for the React application
│   ├── package.json          # Configuration file for npm in the frontend
│   └── README.md             # Documentation for the frontend
└── README.md                 # Main documentation for the entire project
```

## Backend Setup

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```

## Frontend Setup

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm start
   ```

## Usage

- Use the `/generate` endpoint in the backend to generate images based on prompts sent from the frontend.

## License

This project is licensed under the MIT License.