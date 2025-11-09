#!/usr/bin/env python3
"""
WordPress Blog Analytics Dashboard
Analysiert WordPress-Posts via REST API und erstellt detaillierte Statistiken
"""

import requests
import json
import sys
from datetime import datetime
from collections import Counter
import re
from typing import List, Dict
import argparse


class WordPressAnalytics:
    def __init__(self, blog_url: str):
        """
        Initialisiert den Analytics-Client

        Args:
            blog_url: URL des WordPress-Blogs (z.B. https://meinblog.de)
        """
        self.blog_url = blog_url.rstrip('/')
        self.api_url = f"{self.blog_url}/wp-json/wp/v2"
        self.posts = []

    def fetch_posts(self) -> bool:
        """Lädt alle veröffentlichten Posts vom Blog"""
        try:
            print(f"📡 Verbinde mit {self.blog_url}...")

            # Alle Posts laden (paginiert)
            page = 1
            all_posts = []

            while True:
                response = requests.get(
                    f"{self.api_url}/posts",
                    params={
                        'per_page': 100,
                        'page': page,
                        'status': 'publish'
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    if page == 1:
                        print(f"❌ Fehler beim Abrufen der Posts: {response.status_code}")
                        return False
                    break

                posts = response.json()
                if not posts:
                    break

                all_posts.extend(posts)
                page += 1

            self.posts = all_posts
            print(f"✅ {len(self.posts)} Posts geladen\n")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Verbindungsfehler: {e}")
            return False

    def clean_html(self, html_text: str) -> str:
        """Entfernt HTML-Tags aus Text"""
        text = re.sub(r'<[^>]+>', '', html_text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def analyze_posts(self) -> Dict:
        """Führt die Hauptanalyse durch"""
        if not self.posts:
            return {}

        analysis = {
            'total_posts': len(self.posts),
            'posts': [],
            'word_counts': [],
            'dates': [],
            'all_words': [],
            'reading_times': []
        }

        for post in self.posts:
            # Text extrahieren und säubern
            content = self.clean_html(post.get('content', {}).get('rendered', ''))
            title = self.clean_html(post.get('title', {}).get('rendered', ''))

            # Wortanzahl
            words = content.split()
            word_count = len(words)

            # Lesezeit (ca. 200 Wörter/Minute)
            reading_time = max(1, round(word_count / 200))

            # Datum parsen
            date_str = post.get('date', '')
            try:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                date = datetime.now()

            analysis['posts'].append({
                'title': title,
                'word_count': word_count,
                'reading_time': reading_time,
                'date': date,
                'link': post.get('link', '')
            })

            analysis['word_counts'].append(word_count)
            analysis['reading_times'].append(reading_time)
            analysis['dates'].append(date)
            analysis['all_words'].extend([w.lower() for w in words if len(w) > 3])

        return analysis

    def generate_report(self, analysis: Dict, format: str = 'terminal'):
        """Generiert den Report"""
        if not analysis:
            print("Keine Daten für Report verfügbar.")
            return

        if format == 'terminal':
            self._terminal_report(analysis)
        elif format == 'html':
            self._html_report(analysis)
        elif format == 'json':
            self._json_report(analysis)

    def _terminal_report(self, analysis: Dict):
        """Erstellt einen formatierten Terminal-Report"""
        print("=" * 70)
        print("📊 WORDPRESS BLOG ANALYTICS DASHBOARD")
        print("=" * 70)
        print()

        # Übersicht
        print("📈 ÜBERSICHT")
        print("-" * 70)
        print(f"Anzahl Posts:        {analysis['total_posts']}")

        if analysis['word_counts']:
            avg_words = sum(analysis['word_counts']) / len(analysis['word_counts'])
            total_words = sum(analysis['word_counts'])
            print(f"Gesamt Wörter:       {total_words:,}")
            print(f"Durchschn. Wörter:   {avg_words:.0f} pro Post")
            print(f"Durchschn. Lesezeit: {sum(analysis['reading_times']) / len(analysis['reading_times']):.1f} Minuten")

        # Zeitraum
        if analysis['dates']:
            earliest = min(analysis['dates'])
            latest = max(analysis['dates'])
            print(f"Zeitraum:            {earliest.strftime('%d.%m.%Y')} - {latest.strftime('%d.%m.%Y')}")

        print()

        # Einzelne Posts
        print("📝 POSTS IM DETAIL")
        print("-" * 70)

        for i, post in enumerate(analysis['posts'], 1):
            print(f"\n{i}. {post['title']}")
            print(f"   📅 {post['date'].strftime('%d.%m.%Y')}")
            print(f"   📄 {post['word_count']} Wörter | ⏱️  {post['reading_time']} Min. Lesezeit")
            print(f"   🔗 {post['link']}")

        print()

        # Häufigste Wörter
        if analysis['all_words']:
            print("🔤 TOP 15 HÄUFIGSTE WÖRTER")
            print("-" * 70)
            word_freq = Counter(analysis['all_words'])

            for word, count in word_freq.most_common(15):
                bar = "█" * min(50, count)
                print(f"{word:.<20} {count:>4} {bar}")

        print()
        print("=" * 70)

    def _html_report(self, analysis: Dict):
        """Erstellt einen HTML-Report"""
        html = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordPress Blog Analytics</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin: 30px 0 15px 0;
            font-size: 1.5em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        .post {
            background: #f8f9fa;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .post-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .post-meta {
            color: #7f8c8d;
            font-size: 0.9em;
            margin: 5px 0;
        }
        .post-link {
            color: #3498db;
            text-decoration: none;
            font-size: 0.9em;
        }
        .post-link:hover {
            text-decoration: underline;
        }
        .word-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        .word-item {
            background: #ecf0f1;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #2c3e50;
        }
        .chart {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .bar {
            background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
            height: 25px;
            border-radius: 4px;
            margin: 8px 0;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 WordPress Blog Analytics Dashboard</h1>

        <div class="stats">
"""

        # Statistik-Karten
        total_words = sum(analysis['word_counts']) if analysis['word_counts'] else 0
        avg_words = total_words / len(analysis['word_counts']) if analysis['word_counts'] else 0
        avg_reading = sum(analysis['reading_times']) / len(analysis['reading_times']) if analysis[
            'reading_times'] else 0

        html += f"""
            <div class="stat-card">
                <div class="stat-label">Anzahl Posts</div>
                <div class="stat-value">{analysis['total_posts']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Gesamt Wörter</div>
                <div class="stat-value">{total_words:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">⌀ Wörter/Post</div>
                <div class="stat-value">{avg_words:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">⌀ Lesezeit</div>
                <div class="stat-value">{avg_reading:.1f} Min</div>
            </div>
        </div>

        <h2>📝 Posts</h2>
"""

        # Posts
        for post in analysis['posts']:
            html += f"""
        <div class="post">
            <div class="post-title">{post['title']}</div>
            <div class="post-meta">📅 {post['date'].strftime('%d.%m.%Y')}</div>
            <div class="post-meta">📄 {post['word_count']} Wörter | ⏱️ {post['reading_time']} Min. Lesezeit</div>
            <a href="{post['link']}" class="post-link" target="_blank">🔗 Post öffnen</a>
        </div>
"""

        # Häufigste Wörter
        if analysis['all_words']:
            word_freq = Counter(analysis['all_words'])
            html += """
        <h2>🔤 Häufigste Wörter</h2>
        <div class="chart">
"""
            max_count = word_freq.most_common(1)[0][1] if word_freq else 1
            for word, count in word_freq.most_common(20):
                width = (count / max_count) * 100
                html += f"""
            <div class="bar" style="width: {width}%">
                {word}: {count}
            </div>
"""
            html += """
        </div>
"""

        html += """
    </div>
</body>
</html>
"""

        filename = f"wp_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ HTML-Report erstellt: {filename}")

    def _json_report(self, analysis: Dict):
        """Exportiert Daten als JSON"""
        # Datetime-Objekte in Strings konvertieren
        export_data = {
            'total_posts': analysis['total_posts'],
            'posts': []
        }

        for post in analysis['posts']:
            export_data['posts'].append({
                'title': post['title'],
                'word_count': post['word_count'],
                'reading_time': post['reading_time'],
                'date': post['date'].isoformat(),
                'link': post['link']
            })

        if analysis['all_words']:
            word_freq = Counter(analysis['all_words'])
            export_data['top_words'] = dict(word_freq.most_common(50))

        filename = f"wp_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON-Export erstellt: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='WordPress Blog Analytics Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s https://meinblog.de
  %(prog)s https://meinblog.de --format html
  %(prog)s https://meinblog.de --format json
        """
    )

    parser.add_argument(
        'blog_url',
        help='URL des WordPress-Blogs (z.B. https://meinblog.de)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['terminal', 'html', 'json'],
        default='terminal',
        help='Ausgabeformat (default: terminal)'
    )

    args = parser.parse_args()

    # Analytics durchführen
    analytics = WordPressAnalytics(args.blog_url)

    if not analytics.fetch_posts():
        sys.exit(1)

    if analytics.posts:
        analysis = analytics.analyze_posts()
        analytics.generate_report(analysis, format=args.format)
    else:
        print("❌ Keine Posts gefunden.")
        sys.exit(1)


if __name__ == '__main__':
    main()