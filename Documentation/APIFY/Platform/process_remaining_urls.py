#!/usr/bin/env python3
"""
Process remaining APIFY platform documentation URLs
"""

import re
import os
import time
from pathlib import Path

def url_to_filename(url):
    """Convert URL to sanitized filename"""
    # Remove the base URL
    path = url.replace('https://docs.apify.com/platform', '')
    
    # Remove leading slash
    if path.startswith('/'):
        path = path[1:]
    
    # Replace special characters with hyphens
    path = re.sub(r'[^a-zA-Z0-9/\-_]', '-', path)
    
    # Replace multiple hyphens with single hyphen
    path = re.sub(r'-+', '-', path)
    
    # Replace slashes with hyphens
    path = path.replace('/', '-')
    
    # Remove leading/trailing hyphens
    path = path.strip('-')
    
    # Handle empty path (root)
    if not path:
        path = 'platform'
    
    return f"{path}.md"

def get_existing_files():
    """Get list of existing markdown files"""
    current_dir = Path(__file__).parent
    existing_files = []
    
    for file in current_dir.glob('*.md'):
        existing_files.append(file.name)
    
    return existing_files

def get_all_urls():
    """Extract all URLs from Platform.txt"""
    current_dir = Path(__file__).parent
    platform_file = current_dir / 'Platform.txt'
    
    with open(platform_file, 'r') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    urls = []
    
    for line in lines:
        if line.strip().startswith('https://'):
            urls.append(line.strip())
    
    return urls

def find_missing_urls():
    """Find URLs that haven't been processed yet"""
    all_urls = get_all_urls()
    existing_files = get_existing_files()
    
    missing_urls = []
    
    for url in all_urls:
        expected_filename = url_to_filename(url)
        if expected_filename not in existing_files:
            missing_urls.append(url)
    
    return missing_urls

def main():
    """Main function to identify missing URLs"""
    missing_urls = find_missing_urls()
    
    print(f"Total URLs to process: {len(missing_urls)}")
    print("\nMissing URLs:")
    for i, url in enumerate(missing_urls, 1):
        expected_filename = url_to_filename(url)
        print(f"{i:2d}: {url} -> {expected_filename}")
    
    return missing_urls

if __name__ == "__main__":
    main()