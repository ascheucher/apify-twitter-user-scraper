#!/usr/bin/env python3
import os
import re

def sanitize_filename(url):
    """Convert URL to sanitized filename"""
    # Remove the base URL
    path = url.replace('https://docs.apify.com/platform', '')
    if path.startswith('/'):
        path = path[1:]
    
    # If it's the root platform page, name it 'platform'
    if not path:
        path = 'platform'
    
    # Replace slashes with hyphens
    filename = path.replace('/', '-')
    
    # Remove any special characters that might cause issues
    filename = re.sub(r'[^a-zA-Z0-9-_]', '', filename)
    
    # Add .md extension
    filename += '.md'
    
    return filename

def main():
    base_dir = '/Users/admin/Documents/VSC-Projects/AI-Tools/WebDoc2MD/Documentation/APIFY/Platform'
    
    # Read all URLs
    urls = []
    with open(os.path.join(base_dir, 'Platform.txt'), 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('https://'):
                urls.append(line)
    
    # Get existing files
    existing_files = set()
    for filename in os.listdir(base_dir):
        if filename.endswith('.md'):
            existing_files.add(filename)
    
    # Find missing URLs
    missing_urls = []
    for url in urls:
        expected_filename = sanitize_filename(url)
        if expected_filename not in existing_files:
            missing_urls.append((url, expected_filename))
    
    print(f"Total URLs: {len(urls)}")
    print(f"Existing files: {len(existing_files)}")
    print(f"Missing URLs: {len(missing_urls)}")
    print("\nMissing URLs and their expected filenames:")
    for url, filename in missing_urls:
        print(f"{url} -> {filename}")

if __name__ == "__main__":
    main()