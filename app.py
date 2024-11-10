import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import requests
import xml.etree.ElementTree as ET
import json
from pdfminer.high_level import extract_text  # Use pdfminer.six for PDF text extraction

app = Flask(__name__)

# File paths for storing data
REVIEWED_PAPERS_FILE = 'reviewed_papers.json'
SELECTED_PAPERS_FILE = 'selected_papers.json'  # Unread papers
IN_REVIEW_PAPERS_FILE = 'in_review_papers.json'
READ_PAPERS_FILE = 'read_papers.json'
LEFT_SWIPED_PAPERS_FILE = 'left_swiped_papers.json'
NOTES_DIR = 'notes'  # Directory to store notes
PDF_DIR = 'pdfs'     # Directory to cache PDFs

# Ensure directories exist
os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Load data
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

reviewed_papers = load_json(REVIEWED_PAPERS_FILE)
selected_papers = load_json(SELECTED_PAPERS_FILE)
in_review_papers = load_json(IN_REVIEW_PAPERS_FILE)
read_papers = load_json(READ_PAPERS_FILE)
left_swiped_papers = load_json(LEFT_SWIPED_PAPERS_FILE)

# Load settings
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    else:
        return {
            "dark_mode": False,
            "theme": "default"
        }

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

settings = load_settings()

# Function to sanitize paper IDs for filenames
def sanitize_filename(filename):
    return filename.replace('/', '_').replace(':', '_')

@app.route('/')
def index():
    return render_template('index.html', settings=settings)

@app.route('/get_paper')
def get_paper():
    start = int(request.args.get('start', 0))
    max_results = 1

    while True:
        url = (
            f'http://export.arxiv.org/api/query?search_query=cat:cs.AI'
            f'&sortBy=submittedDate&sortOrder=descending&start={start}&max_results={max_results}'
        )
        response = requests.get(url)
        root = ET.fromstring(response.content)

        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        if not entries:
            return jsonify({'status': 'no_more_papers'})

        paper = entries[0]
        paper_id = paper.find('{http://www.w3.org/2005/Atom}id').text

        if paper_id in reviewed_papers:
            start += 1
            continue

        title = paper.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = paper.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        link = paper_id  # The ID is also the link to the paper

        return jsonify({
            'status': 'ok',
            'paper_id': paper_id,
            'title': title,
            'summary': summary,
            'link': link,
            'next_start': start + 1
        })

@app.route('/review_paper', methods=['POST'])
def review_paper():
    global selected_papers, read_papers, in_review_papers, left_swiped_papers

    data = request.json
    paper_id = data['paper_id']
    action = data['action']
    title = data.get('title')
    summary = data.get('summary')
    link = data.get('link')

    if paper_id not in reviewed_papers:
        reviewed_papers.append(paper_id)
        with open(REVIEWED_PAPERS_FILE, 'w') as file:
            json.dump(reviewed_papers, file)

    paper_data = {
        'paper_id': paper_id,
        'title': title,
        'summary': summary,
        'link': link
    }

    if action == 'like':
        if paper_id not in [paper['paper_id'] for paper in selected_papers]:
            selected_papers.append(paper_data)
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
    elif action == 'dislike':
        if paper_id not in [paper['paper_id'] for paper in left_swiped_papers]:
            left_swiped_papers.append(paper_data)
            with open(LEFT_SWIPED_PAPERS_FILE, 'w') as file:
                json.dump(left_swiped_papers, file)
    elif action == 'read':
        if paper_id not in [paper['paper_id'] for paper in read_papers]:
            read_papers.append(paper_data)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
        # Remove from other lists if present
        selected_papers = [paper for paper in selected_papers if paper['paper_id'] != paper_id]
        in_review_papers = [paper for paper in in_review_papers if paper['paper_id'] != paper_id]
        left_swiped_papers = [paper for paper in left_swiped_papers if paper['paper_id'] != paper_id]
        with open(SELECTED_PAPERS_FILE, 'w') as file:
            json.dump(selected_papers, file)
        with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
            json.dump(in_review_papers, file)
        with open(LEFT_SWIPED_PAPERS_FILE, 'w') as file:
            json.dump(left_swiped_papers, file)
    elif action == 'in_review':
        if paper_id not in [paper['paper_id'] for paper in in_review_papers]:
            in_review_papers.append(paper_data)
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
        # Remove from selected_papers if present
        selected_papers = [paper for paper in selected_papers if paper['paper_id'] != paper_id]
        left_swiped_papers = [paper for paper in left_swiped_papers if paper['paper_id'] != paper_id]
        with open(SELECTED_PAPERS_FILE, 'w') as file:
            json.dump(selected_papers, file)
        with open(LEFT_SWIPED_PAPERS_FILE, 'w') as file:
            json.dump(left_swiped_papers, file)

    return jsonify({'status': 'ok'})

@app.route('/view_paper/<path:paper_id>', methods=['GET', 'POST'])
def view_paper(paper_id):
    paper_id_full = 'http://' + paper_id  # Reconstruct full URL
    # Find the paper in any category
    paper = next((p for p in selected_papers + read_papers + in_review_papers + left_swiped_papers if p['paper_id'] == paper_id_full), None)
    if not paper:
        return "Paper not found.", 404

    # Sanitize filename
    sanitized_id = sanitize_filename(paper_id)

    # PDF file path
    pdf_path = os.path.join(PDF_DIR, f'{sanitized_id}.pdf')

    # Download PDF if not already cached
    if not os.path.exists(pdf_path):
        # Construct PDF URL from paper ID
        pdf_url = paper_id_full.replace('abs', 'pdf') + '.pdf'
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
        else:
            return "Unable to download PDF.", 500

    # Handle notes
    notes_path = os.path.join(NOTES_DIR, f'{sanitized_id}.txt')
    if request.method == 'POST':
        notes = request.form.get('notes', '')
        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write(notes)
        return jsonify({'status': 'saved'})
    else:
        # Load existing notes if any
        if os.path.exists(notes_path):
            with open(notes_path, 'r', encoding='utf-8') as f:
                notes = f.read()
        else:
            notes = ''
        return render_template('view_paper.html', paper=paper, notes=notes, pdf_filename=f'{sanitized_id}.pdf', settings=settings)

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_file(os.path.join(PDF_DIR, filename))

@app.route('/unread_papers', methods=['GET', 'POST'])
def unread_papers():
    global selected_papers, read_papers, in_review_papers, left_swiped_papers

    if request.method == 'POST':
        action = request.form.get('action')
        selected_ids = request.form.getlist('selected_papers')
        if action == 'move_to_read':
            for paper_id in selected_ids:
                # Move from selected_papers to read_papers
                paper = next((p for p in selected_papers if p['paper_id'] == paper_id), None)
                if paper:
                    selected_papers = [p for p in selected_papers if p['paper_id'] != paper_id]
                    read_papers.append(paper)
            # Save changes
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
        elif action == 'move_to_in_review':
            for paper_id in selected_ids:
                # Move from selected_papers to in_review_papers
                paper = next((p for p in selected_papers if p['paper_id'] == paper_id), None)
                if paper:
                    selected_papers = [p for p in selected_papers if p['paper_id'] != paper_id]
                    in_review_papers.append(paper)
            # Save changes
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
        elif action == 'get_links':
            # Return the abstract links of selected papers
            links = ' '.join([paper['link'] for paper in selected_papers if paper['paper_id'] in selected_ids])
            return jsonify({'links': links})
        return redirect(url_for('unread_papers'))

    return render_template('unread_papers.html', papers=selected_papers, settings=settings)

@app.route('/in_review_papers', methods=['GET', 'POST'])
def in_review_papers_route():
    global selected_papers, read_papers, in_review_papers, left_swiped_papers

    if request.method == 'POST':
        action = request.form.get('action')
        selected_ids = request.form.getlist('selected_papers')
        if action == 'move_to_read':
            for paper_id in selected_ids:
                # Move from in_review_papers to read_papers
                paper = next((p for p in in_review_papers if p['paper_id'] == paper_id), None)
                if paper:
                    in_review_papers = [p for p in in_review_papers if p['paper_id'] != paper_id]
                    read_papers.append(paper)
            # Save changes
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
        elif action == 'move_to_unread':
            for paper_id in selected_ids:
                # Move from in_review_papers to selected_papers
                paper = next((p for p in in_review_papers if p['paper_id'] == paper_id), None)
                if paper:
                    in_review_papers = [p for p in in_review_papers if p['paper_id'] != paper_id]
                    selected_papers.append(paper)
            # Save changes
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
        elif action == 'get_links':
            # Return the abstract links of selected papers
            links = ' '.join([paper['link'] for paper in in_review_papers if paper['paper_id'] in selected_ids])
            return jsonify({'links': links})
        return redirect(url_for('in_review_papers_route'))

    return render_template('in_review_papers.html', papers=in_review_papers, settings=settings)

@app.route('/read_papers', methods=['GET', 'POST'])
def read_papers_route():
    global selected_papers, read_papers, in_review_papers, left_swiped_papers

    if request.method == 'POST':
        action = request.form.get('action')
        selected_ids = request.form.getlist('selected_papers')
        if action == 'move_to_in_review':
            for paper_id in selected_ids:
                # Move from read_papers to in_review_papers
                paper = next((p for p in read_papers if p['paper_id'] == paper_id), None)
                if paper:
                    read_papers = [p for p in read_papers if p['paper_id'] != paper_id]
                    in_review_papers.append(paper)
            # Save changes
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
        elif action == 'get_links':
            # Return the abstract links of selected papers
            links = ' '.join([paper['link'] for paper in read_papers if paper['paper_id'] in selected_ids])
            return jsonify({'links': links})
        return redirect(url_for('read_papers_route'))

    return render_template('read_papers.html', papers=read_papers, settings=settings)

@app.route('/all_papers', methods=['GET', 'POST'])
def all_papers():
    global selected_papers, read_papers, in_review_papers, left_swiped_papers, reviewed_papers

    # Combine all reviewed papers
    papers_data = selected_papers + read_papers + in_review_papers + left_swiped_papers

    # Remove duplicates and create a dictionary
    unique_papers_dict = {paper['paper_id']: paper for paper in papers_data}

    # Build a list of papers with their status
    all_papers = []
    for paper_id, paper in unique_papers_dict.items():
        if any(paper_id == p['paper_id'] for p in selected_papers):
            status = 'unread'
        elif any(paper_id == p['paper_id'] for p in in_review_papers):
            status = 'in_review'
        elif any(paper_id == p['paper_id'] for p in read_papers):
            status = 'read'
        elif any(paper_id == p['paper_id'] for p in left_swiped_papers):
            status = 'left_swiped'
        else:
            status = 'unknown'  # Shouldn't happen
        paper_with_status = paper.copy()
        paper_with_status['status'] = status
        all_papers.append(paper_with_status)

    if request.method == 'POST':
        selected_ids = request.form.getlist('selected_papers')
        action = request.form.get('action')
        if action == 'move_to_unread':
            for paper_id in selected_ids:
                paper = unique_papers_dict.get(paper_id)
                if paper and paper_id not in [p['paper_id'] for p in selected_papers]:
                    selected_papers.append(paper)
            # Remove from other categories
            read_papers = [p for p in read_papers if p['paper_id'] not in selected_ids]
            in_review_papers = [p for p in in_review_papers if p['paper_id'] not in selected_ids]
            left_swiped_papers = [p for p in left_swiped_papers if p['paper_id'] not in selected_ids]
            # Save changes
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
            with open(LEFT_SWIPED_PAPERS_FILE, 'w') as file:
                json.dump(left_swiped_papers, file)
        elif action == 'move_to_left_swiped':
            for paper_id in selected_ids:
                paper = unique_papers_dict.get(paper_id)
                if paper and paper_id not in [p['paper_id'] for p in left_swiped_papers]:
                    left_swiped_papers.append(paper)
            # Remove from other categories
            selected_papers = [p for p in selected_papers if p['paper_id'] not in selected_ids]
            read_papers = [p for p in read_papers if p['paper_id'] not in selected_ids]
            in_review_papers = [p for p in in_review_papers if p['paper_id'] not in selected_ids]
            # Save changes
            with open(LEFT_SWIPED_PAPERS_FILE, 'w') as file:
                json.dump(left_swiped_papers, file)
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
            with open(IN_REVIEW_PAPERS_FILE, 'w') as file:
                json.dump(in_review_papers, file)
        return redirect(url_for('all_papers'))

    return render_template('all_papers.html', papers=all_papers, settings=settings)

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    global settings
    if request.method == 'POST':
        dark_mode = 'dark_mode' in request.form
        theme = request.form.get('theme', 'default')

        settings['dark_mode'] = dark_mode
        settings['theme'] = theme

        save_settings(settings)

        return redirect(url_for('settings_page'))

    return render_template('settings.html', settings=settings)

@app.route('/search', methods=['GET', 'POST'])
def search():
    global selected_papers, in_review_papers, read_papers

    # Combine all papers except those in left_swiped_papers
    papers = selected_papers + in_review_papers + read_papers

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').lower()
        search_pdf = 'search_pdf' in request.form
        search_notes = 'search_notes' in request.form

        results = []

        for paper in papers:
            match_found = False
            paper_title = paper['title'].lower()
            paper_id = paper['paper_id']

            # Sanitize filename
            sanitized_id = sanitize_filename(paper_id.replace('http://', ''))

            # Search in PDF content
            if search_pdf:
                pdf_path = os.path.join(PDF_DIR, f'{sanitized_id}.pdf')
                if os.path.exists(pdf_path):
                    try:
                        text = extract_text(pdf_path)
                        if text and keyword in text.lower():
                            match_found = True
                    except Exception as e:
                        print(f"Error reading PDF {pdf_path}: {e}")
                else:
                    # PDF not downloaded yet
                    pass

            # Search in notes
            if search_notes and not match_found:
                notes_path = os.path.join(NOTES_DIR, f'{sanitized_id}.txt')
                if os.path.exists(notes_path):
                    with open(notes_path, 'r', encoding='utf-8') as f:
                        notes = f.read()
                    if keyword in notes.lower():
                        match_found = True

            if match_found:
                results.append(paper)

        return render_template('search_results.html', papers=results, keyword=keyword, settings=settings)

    return render_template('search.html', settings=settings)

if __name__ == '__main__':
    app.run(debug=True)

