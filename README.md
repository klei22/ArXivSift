# ArXivSift - 📚✨ - Efficiently Filter and Organize arXiv AI Papers

ArXivSift is built to help you efficiently navigate and manage the overwhelming
number of AI papers on arXiv, providing tools to categorize and review papers
according to your interests.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Swipe Interface](#swipe-interface)
  - [Paper Categories](#paper-categories)
  - [Viewing Papers and Taking Notes](#viewing-papers-and-taking-notes)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Data Persistence](#data-persistence)
- [Contributing](#contributing)
- [License](#license)

## Overview

With the rapid growth of AI research, staying up-to-date with the latest publications can be challenging. ArXivSift streamlines this process by providing tools to:

- **Efficiently browse new papers from arXiv.**
- **Categorize papers based on your interest and review status.**
- **Read papers in a focused, full-screen environment.**
- **Take and save notes for each paper.**

## Features

- **Swipe-Based Browsing**: Quickly navigate through arXiv AI papers using intuitive swipe actions or buttons.
- **Paper Categorization**: Organize papers into Unread, In Review, Read, and Disliked categories.
- **Full-Screen PDF Viewer**: Read papers without distractions in a minimalist interface.
- **Notes Panel**: Take notes while reading, with auto-saving functionality.
- **Copy Abstract Links**: Easily copy links to paper abstracts for sharing or reference.
- **Local Data Storage**: All data is stored locally on your machine.

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **pip** package manager

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/arxivsift.git
   cd arxivsift
   ```

2. **Create a Virtual Environment (Optional)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not available, install dependencies manually:*

   ```bash
   pip install flask requests
   ```

4. **Run the Application**

   ```bash
   python app.py
   ```

   Open your browser and navigate to `http://127.0.0.1:5000/` to start using ArXivSift.

## Usage

### Swipe Interface

- **Access the Home Page**: Go to `http://127.0.0.1:5000/`.
- **Browsing Papers**: The app fetches the latest AI papers from arXiv.
- **Actions**:
  - **Interested**: Click "Swipe Right" or swipe right to mark a paper as interested (moves to Unread).
  - **Not Interested**: Click "Swipe Left" or swipe left to dismiss a paper (moves to Disliked).
  - **Read Now**: Click "Read Now" or swipe up to open the paper immediately.
  - **In Review**: Click "Move to In Review" or swipe down to save the paper for later consideration.

*Note: Swipe gestures are available on touch-enabled devices. Use buttons on desktops.*

### Paper Categories

Access different categories from the navigation menu:

- **Unread Papers**: Papers you've marked as interested but haven't read yet.
- **In Review Papers**: Papers you're considering for further review.
- **Read Papers**: Papers you've read.
- **All Papers**: View all papers you've interacted with.

**Managing Papers:**

- **Move Between Categories**: Select papers using checkboxes and choose an action to move them.
- **Copy Abstract Links**: Select papers and click "Copy Abstract Links" to copy their arXiv links.

### Viewing Papers and Taking Notes

- **Open a Paper**:
  - In any category, click "View & Take Notes" next to a paper.
- **Reading Interface**:
  - The paper opens in a full-screen PDF viewer for focused reading.
- **Taking Notes**:
  - Click the "Notes" button at the bottom right to open the notes panel.
  - Type your notes; they auto-save after a brief pause.
- **Notes Persistence**:
  - Your notes are saved locally and will be visible when you return to the paper.

## Configuration

- **Change arXiv Category**:
  - In `app.py`, modify the `search_query` parameter in the `/get_paper` route to fetch papers from a different category.
  - Example: Change `cat:cs.AI` to `cat:stat.ML` for machine learning papers.

## Project Structure

```
arxivsift/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── unread_papers.html
│   ├── in_review_papers.html
│   ├── read_papers.html
│   ├── all_papers.html
│   └── view_paper.html
├── static/
│   └── (Optional static files like CSS or JS)
├── notes/
│   └── (Stored notes files)
├── pdfs/
│   └── (Cached PDF files)
├── reviewed_papers.json
├── selected_papers.json
├── in_review_papers.json
├── read_papers.json
└── left_swiped_papers.json
```

- **app.py**: Main application file.
- **templates/**: HTML templates for rendering pages.
- **notes/**: Directory for storing notes.
- **pdfs/**: Directory for caching PDF files.
- **JSON Files**: Store categorized paper data.

## Data Persistence

- **Paper Data**: Stored in JSON files in the root directory.
- **Notes**: Saved as text files in the `notes/` directory.
- **PDFs**: Cached in the `pdfs/` directory to reduce repeated downloads.

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**: Click on "Fork" at the top of the GitHub page.

2. **Clone Your Forked Repository**:

   ```bash
   git clone https://github.com/yourusername/arxivsift.git
   cd arxivsift
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**: Implement your feature or fix.

5. **Commit Your Changes**:

   ```bash
   git commit -am 'Add new feature'
   ```

6. **Push to Your Branch**:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Submit a Pull Request**: Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

