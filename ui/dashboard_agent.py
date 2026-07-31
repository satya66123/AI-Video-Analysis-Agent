"""
dashboard_page_agent.py

Dashboard Page Agent

Responsibilities
----------------
- Scan project folders
- Calculate statistics
- Display dashboard
"""

from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import streamlit as st

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class DashboardAgent:

    FOLDERS = {
        "Videos": "videos",
        "Audio": "audio",
        "Transcripts": "transcripts",
        "Analysis": "analysis",
        "Reports": "reports",
        "Exports": "exports",
        "Chats": "chat_history",
    }

    def __init__(self):

        for folder in self.FOLDERS.values():
            Path(folder).mkdir(
                parents=True,
                exist_ok=True,
            )

    ##########################################################
    # Helpers
    ##########################################################

    @staticmethod
    def format_size(size: int) -> str:

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        value = float(size)

        for unit in units:

            if value < 1024:
                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} PB"

    ##########################################################
    # Folder Statistics
    ##########################################################

    def folder_statistics(self) -> Dict:

        stats = {}

        for name, folder in self.FOLDERS.items():

            path = Path(folder)

            files = [
                f
                for f in path.iterdir()
                if f.is_file()
            ]

            total_size = sum(
                file.stat().st_size
                for file in files
            )

            stats[name] = {
                "folder": folder,
                "count": len(files),
                "size": total_size,
                "files": files,
            }

        return stats

    ##########################################################
    # Recent Files
    ##########################################################

    def recent_files(
        self,
        limit: int = 10,
    ) -> List[Dict]:

        recent = []

        for name, folder in self.FOLDERS.items():

            path = Path(folder)

            for file in path.glob("*"):

                if not file.is_file():
                    continue

                recent.append(
                    {
                        "category": name,
                        "name": file.name,
                        "path": str(file),
                        "modified": file.stat().st_mtime,
                        "size": file.stat().st_size,
                    }
                )

        recent.sort(
            key=lambda x: x["modified"],
            reverse=True,
        )

        return recent[:limit]

    ##########################################################
    # Export Statistics
    ##########################################################

    def export_statistics(self) -> Dict:

        export_folder = Path("exports")

        export_types = {
            "PDF": 0,
            "HTML": 0,
            "Markdown": 0,
            "TXT": 0,
            "JSON": 0,
        }

        if not export_folder.exists():
            return export_types

        for file in export_folder.rglob("*"):

            if not file.is_file():
                continue

            suffix = file.suffix.lower()

            if suffix == ".pdf":
                export_types["PDF"] += 1

            elif suffix == ".html":
                export_types["HTML"] += 1

            elif suffix == ".md":
                export_types["Markdown"] += 1

            elif suffix == ".txt":
                export_types["TXT"] += 1

            elif suffix == ".json":
                export_types["JSON"] += 1

        return export_types

    ##########################################################
    # System Information
    ##########################################################

    def system_information(self) -> Dict:

        return {
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "Python Version": platform.python_version(),
            "Current Directory": os.getcwd(),
            "Generated": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

    ##########################################################
    # Render
    ##########################################################

    def render(self):

        HeaderAgent.render(
            "📊 Dashboard"
        )

        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True,
        ):
            st.rerun()

        stats = self.folder_statistics()

        exports = self.export_statistics()

        recent = self.recent_files()

        system = self.system_information()

        ##########################################################
        # Metrics
        ##########################################################

        st.subheader("📊 Overall Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🎥 Videos",
                stats["Videos"]["count"],
            )

        with col2:
            st.metric(
                "🎵 Audio",
                stats["Audio"]["count"],
            )

        with col3:
            st.metric(
                "📝 Transcripts",
                stats["Transcripts"]["count"],
            )

        with col4:
            st.metric(
                "🤖 Analysis",
                stats["Analysis"]["count"],
            )

        col5, col6, col7 = st.columns(3)

        with col5:
            st.metric(
                "📑 Reports",
                stats["Reports"]["count"],
            )

        with col6:
            st.metric(
                "💬 Chats",
                stats["Chats"]["count"],
            )

        with col7:
            st.metric(
                "📤 Exports",
                stats["Exports"]["count"],
            )

        st.divider()

        ##########################################################
        # Storage Usage
        ##########################################################

        st.subheader("💾 Storage Usage")

        total_storage = 0

        for name, info in stats.items():

            total_storage += info["size"]

            st.progress(1.0)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(
                    f"**{name}**"
                )

            with col2:
                st.write(
                    self.format_size(
                        info["size"]
                    )
                )

        st.success(
            f"Total Storage Used : {self.format_size(total_storage)}"
        )

        st.divider()

        ##########################################################
        # Export Statistics
        ##########################################################

        st.subheader("📤 Export Statistics")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "PDF",
                exports["PDF"],
            )

        with c2:
            st.metric(
                "HTML",
                exports["HTML"],
            )

        with c3:
            st.metric(
                "Markdown",
                exports["Markdown"],
            )

        with c4:
            st.metric(
                "TXT",
                exports["TXT"],
            )

        with c5:
            st.metric(
                "JSON",
                exports["JSON"],
            )

        st.divider()

        ##########################################################
        # Folder Details
        ##########################################################

        st.subheader("📂 Folder Statistics")

        table = []

        for name, info in stats.items():

            table.append(
                {
                    "Folder": name,
                    "Files": info["count"],
                    "Storage": self.format_size(
                        info["size"]
                    ),
                }
            )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        ##########################################################
        # Recent Activity
        ##########################################################

        st.subheader("🕒 Recent Files")

        if recent:

            recent_table = []

            for item in recent:

                recent_table.append(
                    {
                        "Category": item["category"],
                        "File": item["name"],
                        "Size": self.format_size(
                            item["size"]
                        ),
                        "Modified": datetime.fromtimestamp(
                            item["modified"]
                        ).strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                    }
                )

            st.dataframe(
                recent_table,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No files found."
            )

        st.divider()

        ##########################################################
        # System Information
        ##########################################################

        st.subheader("⚙️ System Information")

        system_table = []

        for key, value in system.items():

            system_table.append(
                {
                    "Property": key,
                    "Value": value,
                }
            )

        st.dataframe(
            system_table,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        ##########################################################
        # Dashboard Summary
        ##########################################################

        st.success(
            "Dashboard loaded successfully."
        )

        FooterAgent.render()