import json
from urllib.parse import urlparse, urlunparse
from collections import defaultdict

def normalize_url(u: str) -> str:
    p = urlparse(u)
    netloc = (p.netloc or "").lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    # force https, drop fragment
    return urlunparse(("https", netloc, p.path, "", p.query, ""))

def main(inp, outp):
    groups = defaultdict(list)

    with open(inp, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            it = json.loads(line)
            u = it.get("canonical_url") or it.get("url")
            if not u:
                continue
            nu = normalize_url(u)
            it["_norm_url"] = nu
            groups[nu].append(it)

    dedup = []
    for nu, lst in groups.items():
        # keep the best version (longest text); tie-break prefer https + non-www original
        def score(it):
            text_len = it.get("text_length") or len(it.get("text", "") or "")
            u = urlparse(it.get("url") or "")
            https = 1 if u.scheme == "https" else 0
            nonwww = 1 if not (u.netloc or "").lower().startswith("www.") else 0
            return (text_len, https, nonwww)

        best = sorted(lst, key=score, reverse=True)[0]
        best["url"] = nu
        best["canonical_url"] = nu
        best.pop("_norm_url", None)
        dedup.append(best)

    with open(outp, "w", encoding="utf-8") as w:
        for it in dedup:
            w.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"IN : {sum(len(v) for v in groups.values())}")
    print(f"OUT: {len(dedup)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scripts/dedupe_clean.py <input.jsonl> <output.jsonl>")
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])