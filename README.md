# SwipeXiv 📚✨ - Swipe Your Way Through Academic Papers

[![SwipeXiv Demo](https://img.shields.io/badge/SwipeXiv-Demo-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-Papers-red)](https://arxiv.org/)

Discovering new research papers has never been this engaging! SwipeXiv brings a fresh and fun approach to browsing arXiv papers, allowing you to quickly sift through the latest findings and keep track of what matters to you.

## Table of Contents

- [What is SwipeXiv?](#what-is-swipexiv)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## What is SwipeXiv?

SwipeXiv is an intuitive web application that lets you explore academic papers from [arXiv](https://arxiv.org/) with a swipe-based interface. Whether you're a researcher, student, or just curious, SwipeXiv makes it effortless to find and organize papers of interest.

## Features

- 🚀 **Swipe Interface**: Quickly browse through papers with simple swipe actions.
  - **Swipe Right** 👍: Mark a paper as interested.
  - **Swipe Left** 👎: Skip papers that aren't relevant.
  - **Swipe Up** 📖: Read the paper immediately.
  - **Swipe Down** 🤔: Save papers for further review.
- 📁 **Organize Papers**: Categorize papers into Unread, In Review, Read, and Disliked.
- 📝 **Notes Panel**: Take notes while reading, with an auto-saving feature.
- 🖥️ **Full-Screen PDF Viewer**: Read papers in a distraction-free environment.
- 🔗 **Copy Links**: Easily copy abstract links for sharing or reference.
- 💾 **Local Storage**: All data is stored locally on your machine for privacy and speed.

## Installation

Ready to dive in? Follow these steps to get SwipeXiv up and running:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/swipexiv.git
   cd swipexiv
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is missing, install dependencies manually:*

   ```bash
   pip install flask requests
   ```

4. **Run the Application**

   ```bash
   python app.py
   ```

   Open your browser and navigate to `http://127.0.0.1:5000/` to start using SwipeXiv!

## Usage

### Swipe Interface

- **Access the Swipe Interface**: Go to the home page at `http://127.0.0.1:5000/`.
- **Browsing Papers**: The app fetches the latest papers from arXiv in the `cs.AI` category by default.
- **Swiping Actions**:
  - **Swipe Right (Interested)** 👍: Adds the paper to your Unread list.
  - **Swipe Left (Not Interested)** 👎: Moves the paper to the Disliked list.
  - **Swipe Up (Read Now)** 📖: Opens the paper for immediate reading.
  - **Swipe Down (In Review)** 🤔: Saves the paper for further consideration.

*Note: On desktops, use the buttons provided. On touch devices, swipe gestures are supported.*

### Organizing Your Papers

Access different paper categories via the navigation menu:

- **Unread Papers** 📥: Papers you've marked as interested.
- **In Review Papers** 🕒: Papers pending further evaluation.
- **Read Papers** ✅: Papers you've read and possibly taken notes on.
- **All Papers** 🗂️: A consolidated list of all papers you've interacted with.

### Viewing Papers and Taking Notes

- **Viewing a Paper**:
  - From any list, click "View & Take Notes" to open the paper.
- **Full-Screen PDF Viewer**:
  - The paper opens in a full-screen PDF viewer for an immersive reading experience.
- **Notes Panel** 📝:
  - Click the floating "Notes" button at the bottom right corner.
  - The notes panel slides up smoothly, allowing you to jot down thoughts.
- **Auto-Save and Persistence**:
  - Your notes are automatically saved as you type.
  - Notes are stored locally and will be available when you return to the paper.

### Managing Papers

- **Moving Papers Between Categories**:
  - Select papers using checkboxes in the lists.
  - Use the action buttons to move papers to different categories.
- **Copying Abstract Links** 🔗:
  - Select papers and click "Copy Abstract Links" to copy their arXiv links.
  - Useful for sharing or citing in your work.

## Screenshots

*(Add screenshots to visually showcase the app's features.)*

![Swipe Interface](screenshots/swipe_interface.png)
*Swipe through papers quickly and intuitively.*

![Full-Screen PDF Viewer](screenshots/fullscreen_viewer.png)
*Read papers in a distraction-free environment.*

![Notes Panel](screenshots/notes_panel.png)
*Take notes that auto-save and persist.*

## Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**

   Click the "Fork" button at the top right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/swipexiv.git
   cd swipexiv
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Commit Your Changes**

   ```bash
   git commit -am 'Add a cool feature'
   ```

5. **Push to Your Branch**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**

   We'll review your PR and discuss any changes needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

