#!/usr/bin/env python3
"""Count read-aloud Afrikaans words in Volume 1 stories."""
import re, glob, os

def count_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    lines = content.split('\n')
    word_count = 0
    in_beeldnota = False
    skip_sections = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if stripped.startswith('!['):
            continue
        if stripped.startswith('> **Beeldnota:**'):
            in_beeldnota = True
            continue
        if in_beeldnota:
            if stripped.startswith('>') or stripped == '':
                continue
            in_beeldnota = False
        if 'produksie-notas' in stripped.lower() or stripped.startswith('## Produksie'):
            skip_sections = True
            continue
        if skip_sections:
            continue
        if stripped == '---':
            continue
        if not stripped:
            continue
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'〔[^〕]+〕', '', text)
        word_count += len(text.split())
    return word_count

if __name__ == '__main__':
    files = sorted(glob.glob('/agent/manuscripts/volume-01/*.md'))
    counts = []
    for f in files:
        wc = count_words(f)
        counts.append((os.path.basename(f), wc))
        status = 'OK' if 500 <= wc <= 650 else 'OUT'
        print(f"{os.path.basename(f)}: {wc} [{status}]")
    print(f"\nMin: {min(c[1] for c in counts)}, Max: {max(c[1] for c in counts)}, Avg: {sum(c[1] for c in counts)/len(counts):.0f}")
    outside = [c for c in counts if c[1] < 500 or c[1] > 650]
    if outside:
        print(f"Outside range: {len(outside)} files")
