# AI Portfolio Backend

This is the backend part of the AI Portfolio project, which utilizes Flask to serve a Stable Diffusion model for generating images based on text prompts.

## Requirements

To run this backend application, you need to have Python installed along with the required dependencies. You can install the dependencies using the following command:

```
pip install -r requirements.txt
```

## Running the Application

To start the Flask server, run the following command:

```
python app.py
```

The server will start on `http://127.0.0.1:5000/` by default.

## API Endpoint

### POST /generate

This endpoint generates an image based on the provided text prompt.

#### Request

- **Content-Type:** application/json
- **Body:**
  ```json
  {
    "prompt": "Your text prompt here"
  }
  ```

#### Response

- **Success (200):**
  ```json
  {
    "image": "Base64 encoded image string"
  }
  ```

- **Error (400):**
  ```json
  {
    "error": "Prompt is required"
  }
  ```

## License

This project is licensed under the MIT License.