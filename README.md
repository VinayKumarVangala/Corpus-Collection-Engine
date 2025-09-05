# Corpus Collection Engine

An AI-powered, open-source Streamlit application for preserving Indian culture and diversity through multi-media corpus collection with **persistent data storage** and **secure authentication**.

## ✨ Features

- **Multi-Category Collection**: 10 API-compatible categories optimized for cultural preservation
- **Multi-Media Support**: Text, Image, Audio, and Video uploads with chunked upload
- **Backend Integration**: Full API connectivity with environment-based configuration
- **Secure Authentication**: Phone/OTP authentication with JWT token management
- **User Dashboard**: Track contributions, view stats, and manage content
- **Modern UI**: Professional dark/light theme with square category buttons
- **Top Navigation**: Clean navbar with Home, Contribute, Dashboard, Browse, About, and Logout
- **Multilingual**: Support for 12+ Indian languages

## 🚀 Quick Start

### Step 1: Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API credentials
# Update API_BASE_URL and JWT_SECRET_KEY
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
# Method 1: Using runner script (Recommended)
python run.py

# Method 2: Direct streamlit
streamlit run app.py
```

### Step 4: Configure Environment
Edit `.env` file with your actual values:
```env
API_BASE_URL=https://your-actual-api-domain.com
JWT_SECRET_KEY=your-actual-jwt-secret-key
```

### Access the App
Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── config.py              # Environment-based configuration
├── run.py                 # Application runner with setup
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── utils/                # Utility modules
│   ├── api_client.py     # Backend API integration
│   ├── categories.py     # Category management
│   ├── file_upload.py    # Chunked file upload
│   ├── geospatial.py     # Location-based features
│   ├── permissions.py    # Role-based access control
│   └── data_export.py    # Data export functionality
├── admin_panel.py        # Admin management interface
└── README.md             # Documentation
```

## 🎯 Usage Guide

### 1. User Registration & Login
- **Register**: Create account with email, name, and password
- **Secure Storage**: Passwords hashed with bcrypt
- **Persistent Sessions**: User data survives app restarts
- **Login Validation**: Only registered users can access

### 2. Contributing Content
1. **Login**: Access with your registered credentials
2. **Select Category**: Choose from 23+ cultural categories with matching emojis
3. **Choose Media Type**: Text, Image, Audio, or Video
4. **Upload Content**: Add your cultural contribution
5. **Add Metadata**: Title, description, language, and privacy settings
6. **Submit**: Contribution saved permanently to disk

### 3. Dashboard Analytics
- **Total Contributions**: Count of all your submissions
- **Storage Usage**: Track total file sizes
- **Category Breakdown**: See which categories you've contributed to
- **Public vs Private**: Monitor your public contributions
- **Recent Activity**: View your latest submissions

### 4. Browse Public Content
- **Filter Options**: By category, media type, and language
- **Community Gallery**: Discover contributions from other users
- **Search Functionality**: Find specific cultural content

## 🔐 Security & Data Storage

### Authentication
- **bcrypt Hashing**: Military-grade password security
- **Session Management**: Secure user sessions
- **Access Control**: Protected routes and data

### Data Persistence
- **User Credentials**: `data/users.json` (passwords hashed)
- **Contributions**: `data/contributions.json` + individual files
- **Media Files**: `data/uploads/` directory
- **Backup System**: Multiple storage formats for reliability

### File Security
- **Type Validation**: Only allowed file types accepted
- **Size Limits**: Text (200KB), Image (10MB), Audio (25MB), Video (100MB)
- **Sanitization**: Files processed and validated
- **Secure Storage**: Protected file system access

## 🎨 Categories Supported

**10 API-Compatible Categories:**

| Category | Description |
|----------|-------------|
| Art 🎨 | Creative works, paintings, sculptures, and artistic expressions |
| Culture 🏛️ | Traditions, customs, folklore, people, and cultural practices |
| Food 🍛 | Culinary content, recipes, agriculture, and food-related information |
| Literature 📖 | Books, poems, stories, newspapers, and written works |
| Music 🎵 | Musical content, songs, instruments, and audio experiences |
| Architecture 🏗️ | Buildings, structures, monuments, and architectural designs |
| Education 🎓 | Learning materials, skills, tutorials, and educational content |
| Flora 🌸 | Plants, flowers, trees, vegetation, and botanical content |
| Fauna 🦋 | Animals, wildlife, birds, and zoological content |
| Events 🎉 | Festivals, celebrations, ceremonies, and special occasions |

## 🛠️ Development

### Adding New Categories
Edit the `CATEGORIES` dictionary in `app.py`:
```python
CATEGORIES = {
    "Art": "🎨",
    "Your New Category": "🆕"
}
```

### Adding New Languages
Update the language list in the contribute function:
```python
language = st.selectbox("Language", [
    "English", "Hindi", "Telugu", "Your Language"
])
```

## 🚀 Deployment

### Local Production
```bash
# Set production environment
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload all project files
3. Ensure `requirements.txt` includes all dependencies
4. Deploy with Streamlit SDK

## 📊 Data Management

### Backup Your Data
```bash
# Backup user data
cp data/users.json backup/users_backup.json

# Backup contributions
cp data/contributions.json backup/contributions_backup.json

# Backup media files
cp -r data/uploads/ backup/uploads_backup/
```

### Reset Data (Development)
```bash
# Clear all data (WARNING: Irreversible)
rm -rf data/
python init_data.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License. See `LICENSE` file for details.

## 🆘 Support

- **Issues**: Create an issue on the repository
- **Documentation**: Check the code comments and docstrings
- **Community**: Join discussions in the repository

## 🎯 Roadmap

- [ ] Advanced search and filtering
- [ ] Export functionality for researchers
- [ ] AI-powered content tagging
- [ ] Community voting and curation
- [ ] Mobile-responsive design improvements
- [ ] Multi-language UI support

---

**Preserving Indian Culture & Diversity - One Contribution at a Time** 🏛️

*Built with ❤️ using Streamlit, bcrypt, and modern web technologies*