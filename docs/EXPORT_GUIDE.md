# Export Guide

![Export](https://img.shields.io/badge/Export-Guide-blue)
![Formats](https://img.shields.io/badge/Formats-PDF%20%7C%20HTML%20%7C%20Markdown%20%7C%20TXT%20%7C%20JSON-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

The **Export** feature allows you to save generated AI reports in multiple formats for sharing, documentation, or future reference.

---

# Overview

The Export module converts the generated report into different file formats and stores them locally.

Supported export formats:

- PDF
- HTML
- Markdown (.md)
- Text (.txt)
- JSON

---

# Export Workflow

```
Generate Report
       │
       ▼
Choose Export Format(s)
       │
       ▼
Generate Files
       │
       ▼
Save to exports/
```

---

# Export Folder Structure

```
exports/

├── pdf/
├── html/
├── markdown/
├── txt/
└── json/
```

Each exported report is automatically saved into its corresponding folder.

---

# Supported Formats

## PDF

- Professional printable report
- Easy to share
- Suitable for documentation

Extension

```
.pdf
```

---

## HTML

- View in any web browser
- Preserves formatting
- Easy to publish online

Extension

```
.html
```

---

## Markdown

- GitHub compatible
- Easy to edit
- Suitable for documentation

Extension

```
.md
```

---

## Text

- Plain text report
- Lightweight
- Maximum compatibility

Extension

```
.txt
```

---

## JSON

- Machine-readable format
- Stores structured report data
- Useful for integration and automation

Extension

```
.json
```

---

# Export Process

1. Complete video processing.
2. Generate the AI report.
3. Open the **Export** section.
4. Select one or more export formats.
5. Click **Export**.
6. Files are saved automatically.

---

# Generated File Name

Reports are automatically named using the following format:

```
video_name_reportType_timestamp
```

Example

```
meeting_analysis_20260801_101530.pdf
```

---

# Exported Information

Depending on the report, exported files may include:

- Video Information
- Audio Information
- Transcript
- AI Analysis
- Chat History
- Processing Metadata

---

# Export Location

All exported reports are stored inside:

```
exports/
```

Subfolders:

```
pdf/
html/
markdown/
txt/
json/
```

---

# Managing Exports

The application supports:

- View exported reports
- Load exported reports
- Delete exported reports
- Clear all exported reports

---

# Best Practices

- Use **PDF** for sharing reports.
- Use **Markdown** for GitHub documentation.
- Use **HTML** for browser viewing.
- Use **TXT** for simple text archives.
- Use **JSON** for integrations and automation.

---

# Troubleshooting

### Export Failed

Possible causes:

- Invalid report data
- Missing export directory
- Insufficient file permissions
- Disk space unavailable

---

### PDF Not Generated

Verify:

- ReportLab is installed.
- The export directory is writable.

---

### JSON Export Error

Ensure the report data contains valid JSON-serializable values.

---

# Summary

The Export module provides a simple and flexible way to save AI-generated reports in multiple formats. It supports PDF, HTML, Markdown, TXT, and JSON exports, organizing all generated files into dedicated folders under the `exports/` directory for easy access and management.