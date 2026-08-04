import json

import requests

try:
    import brotli
except ImportError:  # pragma: no cover - optional dependency
    brotli = None

URL = "https://chartink.com/screener/process"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://chartink.com",
    "priority": "u=1, i",
    "referer": "https://chartink.com/screener/copy-rsi-above-55-and-breakout-615",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "eyJpdiI6IkVhTE9nVThwZk1aY0ppQWFDMVFKOGc9PSIsInZhbHVlIjoiZ1MxQUdZL2NCYzJHWHFQelZJTElqSVFWWlBnclBZYzZ5YW9CdTRQRkRNOXZ0bmpxZHhnOWIzQ3piYXBGZkRQQVpIQU4rL2lnakFmT1YxVzJRWHRzUzlmYUJBMWtTZUxNVXc1aVg1a3M3czBwZTFmbzRQUXJvY3ZOY0gwSHZOV1AiLCJtYWMiOiJjNjhlZTJkZTg4ZmE4NDAzZDljOWQ2MjJhMjQxMzM4OGUxNzMzODU5NjM4MGVkODE4YWJmNTg2Zjg1YjAxNzJiIiwidGFnIjoiIn0=",
}

cookie_header = (
    "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkhDd05qM2pTT1JVZW0vdGVHOWNQYlE9PSIsInZhbHVlIjoiNWpJVlIzdW8vRnpWemJGWW80ZWVKelBQUmJqSUZiNy9MWW1HbXk5UEFTa2RWaEJFekNxY0F2bHRpc3M0S2hOR0JGQU5pbzZYNityTURhTGJrT25RcHVNQjR3N2dnNTNWRnhwV1o5QlNnT1ZVYlh4UWgrMWNuYlprM2VMR0tTZmoxczdRRXNFMnIzMndsaUp4MWp1bU00d0tKK3FyNnlhdDgyaytXdmZhUm91NGtLa25JcDYwYkIzTCs5M0Y0VDZnUk92ZWdVQytya0JIdkx1RGlsS1hZdzlUMEJ5RGJXSjZqb0Y3YytwK2V3VT0iLCJtYWMiOiJhOGZiOGY1ZDFiYmExNDRhNmVhMjRmZmExN2FmOGI1Y2VjMDYwZDNkNzZkOGMyOGIzYmM0OWU3M2VkZGEzZWY3IiwidGFnIjoiIn0%3D; _cc_id=ddd4893ce0c7883fd0816bb00b1dd02a; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%226f1b27a0-7d11-4a14-98ae-03a35fed3e2a%5C%22%2C%5B1784555417%2C262000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol-TAHbJACJY4lTrE5ZSlvrKAxjPJXn5e-ns2BOn-gqwuibhr6NbHGZUaZzRF80Ca7kNMBb7QAhsRqSehMMwoudMOCcEK5KcwrhEfRWcCXflfJ6qWQ5mePeAXNlA69Fav4cxcIwmIYxtne0C09Q3gSkT2v11bg%3D%3D%22%5D%5D; __utma=102564947.1968319544.1784554512.1784685434.1784685434.1; __utmz=102564947.1784685434.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.1711244705.1785667224; _ga=GA1.1.1968319544.1784554512; XSRF-TOKEN=eyJpdiI6IkVhTE9nVThwZk1aY0ppQWFDMVFKOGc9PSIsInZhbHVlIjoiZ1MxQUdZL2NCYzJHWHFQelZJTElqSVFWWlBnclBZYzZ5YW9CdTRQRkRNOXZ0bmpxZHhnOWIzQ3piYXBGZkRQQVpIQU4rL2lnakFmT1YxVzJRWHRzUzlmYUJBMWtTZUxNVXc1aVg1a3M3czBwZTFmbzRQUXJvY3ZOY0gwSHZOV1AiLCJtYWMiOiJjNjhlZTJkZTg4ZmE4NDAzZDljOWQ2MjJhMjQxMzM4OGUxNzMzODU5NjM4MGVkODE4YWJmNTg2Zjg1YjAxNzJiIiwidGFnIjoiIn0%3D; ci_session=eyJpdiI6IkY1c09MOXdNc2JPcTZSUlRKNUNSS0E9PSIsInZhbHVlIjoiYjI0dG84dXNpTzV2czladlhSWC9qZmdEa0Ixa3JxTTRXTmU4QStEdUZTNmU5UURyYmpqbkk5VjREb0tYbUxTcE5NcEdXa09pdTdCQVQ1Qy9wMkIzNVgvQlMwU1Z6eEZHbmJDbXRBek1vREQ3RHF4VGs1U2hpMFJYaHlsNmdTZ2giLCJtYWMiOiIyNzZiYzMzNGRjOTlkYTJmNjZkN2Q5YzYyYWRmMTUyMGZhMWYwMDA1ZTQ3M2FhYmYxNzEwZmI5NjAzNWY5NjE4IiwidGFnIjoiIn0%3D; __gads=ID=a475dc11d13edfcf:T=1784555440:RT=1785667724:S=ALNI_MYui5MgqrqdpMh-ReKIEte6_hI-uA; __gpi=UID=000014cd24fad536:T=1784555440:RT=1785667724:S=ALNI_MZGgCFV-utYaaRCbqopFGIu-JkQow; __eoi=ID=262f680056f8b3e7:T=1784555440:RT=1785667724:S=AA-Afja56EFTSdPZv4hb308AWKUH; _ga_7P3KPC3ZPP=GS2.1.s1785665055$o7$g1$t1785667725$j33$l0$h0"
)

HEADERS["cookie"] = cookie_header

COOKIES = {}
for raw_cookie in cookie_header.split(";"):
    if "=" in raw_cookie:
        key, value = raw_cookie.split("=", 1)
        COOKIES[key.strip()] = value.strip()

PAYLOADS = {
    "RSIAbove50": {
        "scan_clause": "( {cash} (  weekly close >=  52 and  daily ema( close,5 ) >  daily ema( close,26 ) and  daily ema( close,13 ) >  daily ema( close,26 ) and  daily close >  1 day ago close *  1.03 and  daily volume >  daily sma( volume,20 ) *  1.0 and  daily ema( close,5 ) >  daily ema( close,13 ) and  daily high =  daily max( 260 ,  daily high ) *  1 and  1 day ago close >  2 days ago close *  0.98 and  daily rsi( 14 ) >  55 ) )",
        "debug_clause": "groupcount( 1 where  weekly close >=  52),groupcount( 1 where  daily ema( close,5 ) >  daily ema( close,26 )),groupcount( 1 where  daily ema( close,13 ) >  daily ema( close,26 )),groupcount( 1 where  daily close >  1 day ago close *  1.03),groupcount( 1 where  daily volume >  daily sma( volume,20 ) *  1.0),groupcount( 1 where  daily ema( close,5 ) >  daily ema( close,13 )),groupcount( 1 where  daily high =  daily max( 260 ,  daily high ) *  1),groupcount( 1 where  1 day ago close >  2 days ago close *  0.98),groupcount( 1 where  daily rsi( 14 ) >  55)",
        "column_clause": " Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'",
    },
    "ShortTermBreakouts": {
        "scan_clause": "( {cash} (  daily max( 5 ,  daily close ) >  6 days ago max( 120 ,  daily close ) *  1.05 and  daily volume >  daily sma( volume,5 ) and  daily close >  1 day ago close ) )",
        "debug_clause": "groupcount( 1 where  daily max( 5 ,  daily close ) >  6 days ago max( 120 ,  daily close ) *  1.05),groupcount( 1 where  daily volume >  daily sma( volume,5 )),groupcount( 1 where  daily close >  1 day ago close)",
        "column_clause": " Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily \"close - 1 candle ago close / 1 candle ago close * 100\" >  0,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'",
    },
    "52wHighBreakouts": {
        "scan_clause":"( {cash} (  daily close >  1 day ago max( 240 ,  daily high ) ) )","debug_clause":"groupcount( 1 where  daily close >  1 day ago max( 240 ,  daily high ))","column_clause":" Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'"
        },
    "Dr J VIP daily Breakout scanner": {
        "scan_clause":"( {cash} ( ( {cash} (  daily volume >  10000 and  monthly close >  100 and( {cash} (  daily close >=  1 day ago max( 10 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 20 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 30 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 40 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 50 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 60 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 70 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 80 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 90 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 100 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 110 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 120 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 130 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 140 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 150 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 160 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 170 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 180 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 190 ,  daily high ) *  1.02 or  daily close >=  1 day ago max( 200 ,  daily high ) *  1.02 ) ) and  yearly debt equity ratio <  1 and  quarterly foreign institutional investors percentage >  0.5 and  market cap >  500 and  quarterly mutual funds or uti percentage >  0.5 ) ) ) )","debug_clause":"groupcount( 1 where      daily volume >  10000),groupcount( 1 where      monthly close >  100),groupcount( 1 where          daily close >=  1 day ago max( 10 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 20 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 30 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 40 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 50 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 60 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 70 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 80 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 90 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 100 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 110 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 120 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 130 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 140 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 150 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 160 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 170 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 180 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 190 ,  daily high ) *  1.02),groupcount( 1 where          daily close >=  1 day ago max( 200 ,  daily high ) *  1.02),groupcount( 1 where      yearly debt equity ratio <  1),groupcount( 1 where      quarterly foreign institutional investors percentage >  0.5),groupcount( 1 where      market cap >  500),groupcount( 1 where      quarterly mutual funds or uti percentage >  0.5)","column_clause":" Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'"
        },
    "Volume Shockers":{
        "scan_clause":"( {cash} (  daily volume >  daily sma( volume,20 ) *  5 ) )","debug_clause":"groupcount( 1 where  daily volume >  daily sma( volume,20 ) *  5)","column_clause":" Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'"
    },
    "15min Breakout":{"scan_clause":"( {cash} ( ( {cash} (  [0] 15 minute close >  [0] 15 minute max( 6 ,  [-1] 15 minute high ) or  [0] 15 minute close <  [0] 15 minute min( 6 ,  [-1] 15 minute low ) ) ) and( {cash} (  [0] 15 minute close >  [0] 15 minute supertrend( 9,2 ) or  [0] 15 minute close >  [0] 15 minute supertrend( 9,2 ) and  [ -1 ] 15 minute close <=  [ -1 ] 15 minute supertrend( 9,2 ) ) ) and( {cash} (  [0] 15 minute macd line( 26,12,9 ) >  [0] 15 minute macd signal( 26,12,9 ) and  daily volume >  300000 and  daily close >  500 ) ) ) )","debug_clause":"groupcount( 1 where      [0] 15 minute close >  [0] 15 minute max( 6 ,  [-1] 15 minute high )),groupcount( 1 where      [0] 15 minute close <  [0] 15 minute min( 6 ,  [-1] 15 minute low )),groupcount( 1 where      [0] 15 minute close >  [0] 15 minute supertrend( 9,2 )),groupcount( 1 where      [0] 15 minute close >  [0] 15 minute supertrend( 9,2 ) and  [ -1 ] 15 minute close <=  [ -1 ] 15 minute supertrend( 9,2 )),groupcount( 1 where      [0] 15 minute macd line( 26,12,9 ) >  [0] 15 minute macd signal( 26,12,9 )),groupcount( 1 where      daily volume >  300000),groupcount( 1 where      daily close >  500)","column_clause":" Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'"
    },
    "Potential Breakouts":{"scan_clause":"( {cash} (  daily close *  1.05 >  daily max( 200 ,  daily high ) and  daily max( 30 ,  daily high ) <=  30 days ago max( 8 ,  daily high ) and  daily volume >  daily sma(  daily volume , 50 ) and  daily close >  90 ) )","debug_clause":"groupcount( 1 where  daily close *  1.05 >  daily max( 200 ,  daily high )),groupcount( 1 where  daily max( 30 ,  daily high ) <=  30 days ago max( 8 ,  daily high )),groupcount( 1 where  daily volume >  daily sma(  daily volume , 50 )),groupcount( 1 where  daily close >  90)","column_clause":" Daily Close as 'scan-column-default-close',  Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close >  1 day ago close,1) as 'default-percent-change-conditional-filters-color',  Daily Volume as 'scan-column-default-volume'"
    }

}

aggregated_rows = {}

for tag, payload in PAYLOADS.items():
    response = requests.post(URL, headers=HEADERS, cookies=COOKIES, json=payload, timeout=30)
    print(f"\nTag: {tag} | Status code: {response.status_code}")

    try:
        content_encoding = response.headers.get("content-encoding", "").lower()
        decoded_body = response.text or ""

        if not decoded_body and brotli is not None and "br" in content_encoding:
            decoded_body = brotli.decompress(response.content).decode("utf-8", errors="replace")
        elif not decoded_body:
            decoded_body = response.content.decode("utf-8", errors="replace")

        data = json.loads(decoded_body)
        rows = data.get("data", [])
        if not rows:
            print(f"No matching records found for {tag}.")
            continue

        for item in rows:
            code = item.get("nsecode", "")
            name = item.get("name", "")
            key = (code, name)

            if key not in aggregated_rows:
                aggregated_rows[key] = {
                    "code": code,
                    "name": name,
                    "close": item.get("scan-column-default-close", ""),
                    "change": item.get("scan-column-default-percent-change", ""),
                    "volume": item.get("scan-column-default-volume", ""),
                    "tags": [tag],
                }
            elif tag not in aggregated_rows[key]["tags"]:
                aggregated_rows[key]["tags"].append(tag)
    except (ValueError, json.JSONDecodeError, AttributeError) as exc:
        print(f"Unable to parse response for {tag}: {exc}")
        print(decoded_body[:4000] if "decoded_body" in locals() else response.text[:4000])

print("\n SCRIPT: MULTI-PAYLOAD SCREENER RESULTS")
print("\nFormatted table:")
if not aggregated_rows:
    print("No matching records found.")
else:
    headers = ["CODE", "NAME", "TAGS", "CLOSE", "CHANGE %", "VOLUME"]
    ranked_rows = sorted(
        aggregated_rows.values(),
        key=lambda item: (-len(item["tags"]), item["code"], item["name"]),
    )
    max_tag_count = max((len(row["tags"]) for row in ranked_rows), default=0)
    shortlisted_rows = [row for row in ranked_rows if len(row["tags"]) == max_tag_count]
    selected_rows = shortlisted_rows[:5]

    rows_display = [
        [
            row["code"],
            row["name"],
            ", ".join(row["tags"]),
            row["close"],
            row["change"],
            row["volume"],
        ]
        for row in selected_rows
    ]

    col_widths = [max(len(str(row[i])) for row in [headers] + rows_display) for i in range(len(headers))]
    print(" | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers)))
    print("-+-".join("-" * width for width in col_widths))
    for row in rows_display:
        print(" | ".join(str(value).ljust(col_widths[i]) for i, value in enumerate(row)))
