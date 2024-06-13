#!/usr/bin/python3

"""
markdown2html - A script to convert Markdown to HTML
"""

import sys
import os
import hashlib

def convert_md_to_html(input_file, output_file):
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    html_lines = []
    in_paragraph = False
    in_unordered_list = False
    in_ordered_list = False

    for line in lines:
        line = line.rstrip()
        
        # Handle headings
        if line.startswith('#'):
            level = len(line.split(' ')[0])
            content = line[level + 1:].strip()
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue
        
        # Handle unordered lists
        if line.startswith('- '):
            if not in_unordered_list:
                html_lines.append("<ul>")
                in_unordered_list = True
            html_lines.append(f"    <li>{line[2:].strip()}</li>")
            continue
        elif in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False

        # Handle ordered lists
        if line.startswith('* '):
            if not in_ordered_list:
                html_lines.append("<ol>")
                in_ordered_list = True
            html_lines.append(f"    <li>{line[2:].strip()}</li>")
            continue
        elif in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False

        # Handle paragraphs
        if line == '':
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            continue
        else:
            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            html_lines.append(f"    {line.replace('**', '<b>').replace('__', '<em>').replace('[[' , '').replace(']]' , '').replace('((' , '').replace('))' , '')}<br />")
    
    # Close any open tags at the end of file
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")
    if in_paragraph:
        html_lines.append("</p>")
    
    with open(output_file, 'w') as f:
        for line in html_lines:
            f.write(f"{line}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_md_to_html(input_file, output_file)
    sys.exit(0)
