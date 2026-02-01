"""
Generate author pages automatically by scanning markdown files for author attribution.
Run this script before building the Jupyter Book.

Usage: python generate_author_pages.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import yaml

# Configuration
BOOK_DIR = Path(__file__).parent / "energy_modelling_notes"
CONFIG_PATH = BOOK_DIR / "_config.yml"
AUTHOR_PATTERN = re.compile(r'\*Authors?:\s*(.+?)\*', re.IGNORECASE)
AUTHOR_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\([^)]+\)')


def load_authors_from_config() -> dict:
    """Load author data from _config.yml myst_substitutions."""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    substitutions = config.get('sphinx', {}).get('config', {}).get('myst_substitutions', {})
    
    # Extract author IDs by looking for keys ending in _name
    author_ids = set()
    for key in substitutions:
        if key.endswith('_name'):
            author_ids.add(key.replace('_name', ''))
    
    # Build AUTHORS dict from substitutions
    authors = {}
    for author_id in author_ids:
        authors[author_id] = {
            'name': substitutions.get(f'{author_id}_name', author_id.title()),
            'bio': substitutions.get(f'{author_id}_bio', ''),
            'github': substitutions.get(f'{author_id}_github', ''),
            'linkedin': substitutions.get(f'{author_id}_linkedin', ''),
            'email': substitutions.get(f'{author_id}_email', ''),
        }
    
    return authors


# Load authors from config
AUTHORS = load_authors_from_config()

# Section mapping based on TOC structure
SECTIONS = {
    "01-introduction": "Getting Started",
    "02-setup": "Getting Started",
    "03-energy-basics": "Energy System Fundamentals",
    "04-electricity-markets": "Energy System Fundamentals",
    "05-optimization": "Modelling Techniques",
    "06-capacity-expansion": "Modelling Techniques",
}


def extract_authors_from_file(filepath: Path) -> list[str]:
    """Extract author names from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        match = AUTHOR_PATTERN.search(content)
        if match:
            author_text = match.group(1)
            # Extract names from markdown links like [Jonas](intro.md#jonas)
            authors = AUTHOR_LINK_PATTERN.findall(author_text)
            if authors:
                return [a.lower() for a in authors]
            # Fallback: split by comma if no links
            return [a.strip().lower() for a in author_text.split(',')]
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return []


def get_article_title(filepath: Path) -> str:
    """Extract the title (first H1) from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()
    except Exception:
        pass
    return filepath.stem


def scan_articles() -> dict[str, list[tuple[str, str, str]]]:
    """Scan all markdown files and return articles grouped by author."""
    author_articles = defaultdict(list)
    
    for md_file in BOOK_DIR.glob("*.md"):
        # Skip special files
        if md_file.name.startswith(('author-', 'intro', 'references')):
            continue
        
        authors = extract_authors_from_file(md_file)
        title = get_article_title(md_file)
        file_stem = md_file.stem
        section = SECTIONS.get(file_stem, "Other")
        
        for author in authors:
            author_articles[author].append((file_stem, title, section))
    
    # Sort articles by filename
    for author in author_articles:
        author_articles[author].sort(key=lambda x: x[0])
    
    return author_articles


def generate_author_page(author_id: str, articles: list[tuple[str, str, str]]) -> str:
    """Generate the markdown content for an author page."""
    author = AUTHORS.get(author_id)
    if not author:
        print(f"Warning: No metadata found for author '{author_id}'")
        return ""
    
    # Build the page content
    lines = [
        "---",
        "orphan: true",
        "---",
        "",
        f"(author-{author_id}-page)=",
        f"# {author['name']} - Articles",
        "",
        f'<a href="{author["github"]}"><i class="fa-brands fa-github author-icon"></i></a> '
        f'<a href="{author["linkedin"]}"><i class="fa-brands fa-linkedin author-icon"></i></a> '
        f'<a href="mailto:{author["email"]}"><i class="fa-solid fa-envelope author-icon"></i></a>',
        "",
        author['bio'],
        "",
        f"## Articles by {author['name']}",
        "",
    ]
    
    if articles:
        lines.extend([
            "```{list-table}",
            ":header-rows: 1",
            "",
            "* - Article",
            "  - Section",
        ])
        
        for file_stem, title, section in articles:
            lines.extend([
                f"* - {{doc}}`{file_stem}`",
                f"  - {section}",
            ])
        
        lines.append("```")
    else:
        lines.append("*No articles found.*")
    
    lines.extend([
        "",
        f'<a href="intro.html#{author_id}">← Back to About the Author</a>',
        ""
    ])
    
    return '\n'.join(lines)


def main():
    print("Scanning articles for author attribution...")
    author_articles = scan_articles()
    
    print(f"Found articles for {len(author_articles)} authors:")
    for author, articles in author_articles.items():
        print(f"  - {author}: {len(articles)} articles")
    
    # Generate author pages
    for author_id in AUTHORS:
        articles = author_articles.get(author_id, [])
        content = generate_author_page(author_id, articles)
        
        if content:
            output_path = BOOK_DIR / f"author-{author_id}.md"
            output_path.write_text(content, encoding='utf-8')
            print(f"Generated: {output_path.name}")
    
    print("\nDone! Run 'jupyter-book build energy_modelling_notes' to build the book.")


if __name__ == "__main__":
    main()
