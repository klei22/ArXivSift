from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import xml.etree.ElementTree as ET
import json
import os

app = Flask(__name__)

# File paths for storing data
REVIEWED_PAPERS_FILE = 'reviewed_papers.json'
SELECTED_PAPERS_FILE = 'selected_papers.json'
READ_PAPERS_FILE = 'read_papers.json'

# Load reviewed papers (list of paper IDs)
if os.path.exists(REVIEWED_PAPERS_FILE):
    with open(REVIEWED_PAPERS_FILE, 'r') as file:
        reviewed_papers = json.load(file)
else:
    reviewed_papers = []

# Load selected papers (list of paper dictionaries)
if os.path.exists(SELECTED_PAPERS_FILE):
    with open(SELECTED_PAPERS_FILE, 'r') as file:
        selected_papers = json.load(file)
else:
    selected_papers = []

# Load read papers (list of paper dictionaries)
if os.path.exists(READ_PAPERS_FILE):
    with open(READ_PAPERS_FILE, 'r') as file:
        read_papers = json.load(file)
else:
    read_papers = []

@app.route('/')
def index():
    return render_template('index.html')

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
    global selected_papers, read_papers  # Declare global variables

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

    elif action == 'read':
        if paper_id not in [paper['paper_id'] for paper in read_papers]:
            read_papers.append(paper_data)
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)

        # Remove from selected_papers if present
        selected_papers = [paper for paper in selected_papers if paper['paper_id'] != paper_id]
        with open(SELECTED_PAPERS_FILE, 'w') as file:
            json.dump(selected_papers, file)

    return jsonify({'status': 'ok'})

@app.route('/unread_papers', methods=['GET', 'POST'])
def unread_papers():
    global selected_papers, read_papers

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
        elif action == 'get_links':
            # Return the abstract links of selected papers
            links = ' '.join([paper['link'] for paper in selected_papers if paper['paper_id'] in selected_ids])
            return jsonify({'links': links})
        return redirect(url_for('unread_papers'))

    return render_template('unread_papers.html', papers=selected_papers)

@app.route('/read_papers', methods=['GET', 'POST'])
def read_papers_route():
    global selected_papers, read_papers

    if request.method == 'POST':
        action = request.form.get('action')
        selected_ids = request.form.getlist('selected_papers')
        if action == 'move_to_unread':
            for paper_id in selected_ids:
                # Move from read_papers to selected_papers
                paper = next((p for p in read_papers if p['paper_id'] == paper_id), None)
                if paper:
                    read_papers = [p for p in read_papers if p['paper_id'] != paper_id]
                    selected_papers.append(paper)
            # Save changes
            with open(READ_PAPERS_FILE, 'w') as file:
                json.dump(read_papers, file)
            with open(SELECTED_PAPERS_FILE, 'w') as file:
                json.dump(selected_papers, file)
        elif action == 'get_links':
            # Return the abstract links of selected papers
            links = ' '.join([paper['link'] for paper in read_papers if paper['paper_id'] in selected_ids])
            return jsonify({'links': links})
        return redirect(url_for('read_papers_route'))

    return render_template('read_papers.html', papers=read_papers)

@app.route('/get_selected_papers')
def get_selected_papers():
    links = ' '.join([paper['link'] for paper in selected_papers])
    return jsonify({'links': links})

@app.route('/get_read_papers')
def get_read_papers():
    return jsonify({'papers': read_papers})

if __name__ == '__main__':
    app.run(debug=True)

