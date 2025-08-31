# Contributing to Corpus Collection Engine

Thank you for your interest in contributing to the Corpus Collection Engine! This project aims to preserve Indian cultural diversity through community contributions.

## How to Contribute

### 🎯 Ways to Contribute

1. **Cultural Content**: Upload text, images, audio, or video representing Indian culture
2. **Code Contributions**: Improve features, fix bugs, add new functionality
3. **Documentation**: Help improve guides, tutorials, and documentation
4. **Testing**: Report bugs, test new features, provide feedback
5. **Translation**: Help translate the interface to more Indian languages

### 📝 Content Contribution Guidelines

#### What to Upload
- **Authentic Cultural Content**: Stories, folklore, traditions, recipes, music, art
- **Educational Material**: Historical information, cultural practices, local knowledge
- **Visual Heritage**: Traditional art, architecture, festivals, ceremonies
- **Audio Heritage**: Folk songs, oral traditions, regional dialects, stories

#### Content Standards
- **Original or Properly Licensed**: Ensure you have rights to share the content
- **Culturally Respectful**: Content should honor and respect cultural traditions
- **Accurate Information**: Provide correct metadata (language, region, category)
- **Family-Friendly**: Keep content appropriate for all audiences

#### Categories Available
- Art, Culture, Food, Literature, Music, Architecture
- Folk Talks, Traditional Skills, Local History
- Flora, Fauna, Education, Events, People
- And 10+ more cultural categories

### 💻 Code Contribution Process

#### Getting Started
1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/corpus-collection-engine.git
   cd corpus-collection-engine
   ```

2. **Set Up Development Environment**
   ```bash
   pip install -r requirements.txt
   python run.py
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

##### File Structure
```
├── app.py                 # Main Streamlit application
├── init_data.py          # Data initialization
├── run.py                # Application launcher
├── requirements.txt      # Dependencies
├── utils/
│   ├── auth.py          # Authentication utilities
│   ├── database.py      # Database operations
│   └── file_handler.py  # File processing
├── data/                # Local storage (not committed)
│   ├── users.json       # User credentials
│   ├── contributions.json # Contribution metadata
│   └── uploads/         # Media files
└── README.md            # Documentation
```

##### Testing
- Test your changes locally before submitting
- Ensure all existing functionality still works
- Add tests for new features when possible
- Test with different file types and sizes

##### Security Considerations
- Never commit sensitive data (passwords, keys, tokens)
- Validate all user inputs
- Follow secure file handling practices
- Maintain authentication and authorization checks

#### Submitting Changes

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all checks pass

### 🐛 Bug Reports

#### Before Reporting
- Check if the issue already exists
- Try to reproduce the bug consistently
- Test with the latest version

#### Bug Report Template
```markdown
**Bug Description**
Clear description of what went wrong

**Steps to Reproduce**
1. Go to...
2. Click on...
3. Upload file...
4. See error

**Expected Behavior**
What should have happened

**Screenshots**
If applicable, add screenshots

**Environment**
- OS: [e.g., Windows 10, macOS, Ubuntu]
- Browser: [e.g., Chrome, Firefox, Safari]
- Python Version: [e.g., 3.8, 3.9, 3.10]
```

### 💡 Feature Requests

#### Suggesting New Features
- Check existing issues and discussions
- Provide clear use case and benefits
- Consider implementation complexity
- Align with project goals of cultural preservation

#### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Screenshots, mockups, or examples
```

### 🌐 Translation Contributions

#### Adding New Languages
1. Copy `i18n/en.json` to `i18n/[language_code].json`
2. Translate all strings while preserving placeholders
3. Update `SUPPORTED_LANGUAGES` in `config.py`
4. Test the interface with new language

#### Translation Guidelines
- Use culturally appropriate terms
- Maintain consistent terminology
- Keep technical terms in English if commonly used
- Consider regional variations

### 📋 Code Review Process

#### For Contributors
- Respond to feedback promptly
- Make requested changes in separate commits
- Keep discussions focused and respectful
- Update documentation if needed

#### Review Criteria
- Code quality and style
- Security considerations
- Performance impact
- User experience
- Documentation completeness

### 🏆 Recognition

#### Contributors
- All contributors are acknowledged in the project
- Significant contributions are highlighted in releases
- Community contributors get special recognition

#### Cultural Contributors
- Content contributors are credited in the dashboard
- Quality contributions are featured
- Community building efforts are recognized

### 📞 Getting Help

#### Community Support
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and community chat
- **Email**: [project-email] for sensitive issues

#### Development Help
- Check existing documentation first
- Search closed issues for similar problems
- Provide detailed context when asking questions
- Be patient and respectful with responses

### 📜 Code of Conduct

#### Our Standards
- **Respectful**: Treat all community members with respect
- **Inclusive**: Welcome contributors from all backgrounds
- **Collaborative**: Work together towards common goals
- **Cultural Sensitivity**: Respect all cultures and traditions

#### Unacceptable Behavior
- Harassment or discrimination
- Inappropriate content or language
- Spam or self-promotion
- Violation of cultural sensitivity

### 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping preserve Indian cultural heritage! 🏛️**

Every contribution, whether code or cultural content, helps build a more inclusive and representative digital future.