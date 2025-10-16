# Contributing to Auto Mute

Thank you for considering contributing to Auto Mute! 

## How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly** on Windows
5. **Commit your changes**: `git commit -m 'Add some feature'`
6. **Push to the branch**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Development Setup

```powershell
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Auto-Mute.git
cd Auto-Mute

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test the script
python auto_mute.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

- Test on Windows 10/11
- Verify all scripts work (.py, .ps1, .vbs)
- Check that notifications appear correctly
- Ensure hotkeys work system-wide

## Reporting Bugs

Please include:
- Windows version
- Python version
- Steps to reproduce
- Error messages (if any)
- Expected vs actual behavior

## Feature Requests

Feel free to open an issue to discuss new features!

## Questions?

Open an issue or reach out to [@AndruTjalas1](https://github.com/AndruTjalas1)
