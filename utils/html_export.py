from __future__ import annotations

import os
import html


def export_html(report: str, filename: str) -> None:
    """
    Export report as HTML.
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    html_report = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Video Analyzer Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin:40px;
    line-height:1.6;
}}

pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
}}

h1 {{
    color:#2563eb;
}}

</style>

</head>

<body>

<h1>AI Video Analyzer Report</h1>

<pre>
{html.escape(report)}
</pre>

</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_report)