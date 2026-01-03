# 🎙️ AI Call Crew - Voice Testing UI

A comprehensive web-based testing interface with voice support for the AI Call Crew API.

## Features

### Voice Testing
- **Real-time Speech Recognition**: Uses Web Speech API for continuous voice input
- **Microphone Control**: Click the microphone button or press SPACEBAR to record
- **Transcription Display**: Live transcription of speech input
- **Voice Processing**: Send voice input directly to the API for processing
- **Text-to-Speech Response**: Play API responses using browser's speech synthesis

### Manual Testing
- **Call Processing**: Test call processing endpoint with custom patient data
- **Appointment Booking**: Schedule appointments with preferred dates/times
- **Health Checks**: Verify server connectivity and API availability
- **Service Listing**: Browse available services

### Configuration
- **Server Settings**: Configure API endpoint URL
- **API Key Management**: Set OpenAI API key for backend
- **Logging**: Real-time request/response logging
- **History**: View conversation history and previous calls

## How to Use

### 1. Start the Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Server will run on `http://localhost:8000`

### 2. Open the Voice UI
Simply open the HTML file in your browser:
```
frontend/index.html
```

Or serve it via HTTP:
```bash
cd frontend
python -m http.server 8001
# Then visit: http://localhost:8001/index.html
```

### 3. Test with Voice
1. Click "Check Connection" to verify the server is running
2. Click the microphone button 🎤 (or press SPACEBAR)
3. Speak your issue/request
4. Click "Process Call" to send to API
5. Listen to the response using "Play Response" button

### 4. Test Manually
Switch to "Manual Testing" tab to:
- Fill in patient information
- Specify issue type and priority
- Send structured API requests
- Book appointments

## UI Tabs

### Voice Testing Tab
- Server status checker
- Microphone input with live transcription
- Voice call processing
- Response display
- Conversation history

### Manual Testing Tab
- Call processing with form inputs
- Appointment booking form
- Health check endpoint tester
- Services endpoint tester
- Real-time response display

### Configuration Tab
- API endpoint URL configuration
- Logging level selection
- API key input
- Test connection button
- Settings persistence

## Browser Requirements

- **Chrome/Edge/Safari**: Modern browser with Web Speech API support
- **Microphone Access**: Browser will request microphone permissions
- **HTTPS Recommended**: Some browsers require HTTPS for microphone access

## API Endpoints Tested

- `GET /health` - Health check
- `GET /api/services` - Get available services
- `POST /api/call/process` - Process a call
- `POST /api/appointment` - Book an appointment

## Keyboard Shortcuts

- **SPACEBAR**: Start/Stop microphone recording
- **ESC**: Cancel ongoing operation
- **Enter**: Submit form

## Response Format

The UI displays API responses in a formatted JSON view with:
- Status indicators (success/error)
- Response time
- Full request/response bodies
- Error messages with details

## Troubleshooting

### Microphone Not Working
- Check browser permissions for microphone
- Try a different browser (Chrome has best support)
- Ensure HTTPS on production

### Cannot Connect to Server
- Verify backend is running on localhost:8000
- Check CORS settings in backend
- Ensure no firewall blocking the connection

### Speech Not Transcribing
- Check microphone input levels
- Speak clearly and at normal volume
- Ensure browser supports Web Speech API

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Web Speech API | ✅ | ⚠️ | ✅ | ✅ |
| Microphone Access | ✅ | ✅ | ✅ | ✅ |
| Text-to-Speech | ✅ | ✅ | ✅ | ✅ |
| All Features | ✅ | ✅ | ✅ | ✅ |

## Future Enhancements

- [ ] Audio recording and playback
- [ ] Call duration tracking
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Advanced filtering and search
- [ ] Export conversation history
- [ ] Real-time collaboration

## Development

The UI is built with vanilla JavaScript, HTML5, and CSS3 - no framework dependencies required.

### Key JavaScript Features Used
- Web Speech API (SpeechRecognition)
- Web Audio API
- Fetch API
- Local Storage for persistence
- EventListeners for real-time updates

## File Structure

```
frontend/
├── index.html          # Main UI file
├── styles/            # (Optional) Separate CSS files
├── js/               # (Optional) Separate JavaScript files
└── VOICE_UI_README.md # This file
```

## License

Same as AI Call Crew project
