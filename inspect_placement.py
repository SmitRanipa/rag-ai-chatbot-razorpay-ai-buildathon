import json

with open('data/raw/placements.jsonl', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        if '2026' in d['url'] and 'btech-computer' in d['url']:
            lines = d['text'].split('\n')
            output_lines = lines[:10]
            output_lines.append('...')
            student_lines = [l for l in lines if 'Enrollment Number' in l]
            output_lines += student_lines[:10]
            with open('inspect_out.txt', 'w', encoding='utf-8') as out:
                out.write('\n'.join(output_lines))
            break

print("Done. Check inspect_out.txt")
