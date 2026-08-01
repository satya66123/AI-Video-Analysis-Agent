"""
dashboard_page_agent.py

Dashboard Page Agent

Responsibilities
----------------
- Scan project folders
- Dashboard statistics
- Storage information
- Recent activity
"""

from __future__ import annotations

import os
import platform

from datetime import datetime
from pathlib import Path

import streamlit as st

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class DashboardPageAgent:
    ROOT = Path(".")

    FOLDERS = {

        # Main folders
        "Videos": ROOT / "uploads",
        "Audio": ROOT / "audio",
        "Transcripts": ROOT / "transcripts",
        "Analysis": ROOT / "analysis",
        "Chats": ROOT / "chat_history",


    }

    EXPORT_FILE_FOLDERS = {
        "Exports / PDF": ROOT / "exports/pdf",
        "Exports / HTML": ROOT / "exports/html",
        "Exports / Markdown": ROOT / "exports/markdown",
        "Exports / TXT": ROOT / "exports/txt",
        "Exports / JSON": ROOT / "exports/json",
    }

    REPORT_FILE_FOLDERS = {
        "Reports / PDF": ROOT / "reports/pdf",
        "Reports / HTML": ROOT / "reports/html",
        "Reports / Markdown": ROOT / "reports/markdown",
        "Reports / TXT": ROOT / "reports/txt",
        "Reports / JSON": ROOT / "reports/json",
    }

    EXPORT_FOLDERS = {
        "PDF": ROOT / "exports" / "pdf",
        "HTML": ROOT / "exports" / "html",
        "Markdown": ROOT / "exports" / "markdown",
        "TXT": ROOT / "exports" / "txt",
        "JSON": ROOT / "exports" / "json",
    }

    REPORT_FOLDERS = {
        "PDF": ROOT / "reports" / "pdf",
        "HTML": ROOT / "reports" / "html",
        "Markdown": ROOT / "reports" / "markdown",
        "TXT": ROOT / "reports" / "txt",
        "JSON": ROOT / "reports" / "json",
    }

    def __init__(self):

        self.ensure_folders()

    ########################################################
    # Folder Creation
    ########################################################

    def ensure_folders(self):

        for folder in self.FOLDERS.values():
            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

        for folder in self.EXPORT_FOLDERS.values():
            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

    ########################################################
    # Size Formatter
    ########################################################

    @staticmethod
    def format_size(size):

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        size = float(size)

        for unit in units:

            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"

    ########################################################
    # Count Files
    ########################################################


    @staticmethod
    def count_files(path: Path):

        if not path.exists():
            return 0

        return sum(
            1
            for file in path.rglob("*")
            if file.is_file()
        )

    ########################################################
    # Folder Size
    ########################################################

    @staticmethod
    def folder_size(path: Path):

        if not path.exists():
            return 0

        total = 0

        for file in path.rglob("*"):

            if file.is_file():
                total += file.stat().st_size

        return total

    ########################################################
    # Folder Statistics
    ########################################################

    def folder_statistics(self):

        statistics = {}

        for name, folder in self.FOLDERS.items():
            statistics[name] = {

                "count": self.count_files(folder),

                "size": self.folder_size(folder),

                "path": folder,

            }

        ####################################################
        # Exports
        ####################################################

        export_count = 0

        export_size = 0

        export_details = {}

        for name, folder in self.EXPORT_FOLDERS.items():
            count = self.count_files(folder)

            size = self.folder_size(folder)

            export_count += count

            export_size += size

            export_details[name] = {

                "count": count,

                "size": size,

                "path": folder,

            }

        statistics["Exports"] = {

            "count": export_count,

            "size": export_size,

            "details": export_details,

        }

        ####################################################
        # Reports
        ####################################################

        report_count = 0

        report_size = 0

        report_details = {}

        for name, folder in self.REPORT_FOLDERS.items():
            count = self.count_files(folder)

            size = self.folder_size(folder)

            report_count += count

            report_size += size

            report_details[name] = {

                "count": count,

                "size": size,

                "path": folder,

            }

        statistics["Reports"] = {

            "count": report_count,

            "size": report_size,

            "details": report_details,

        }

        return statistics

    ########################################################
    # Recent Files
    ########################################################

    def recent_files(
            self,
            limit=10,
    ):

        files = []

        folders = list(
            self.FOLDERS.values()
        )

        folders.extend(
            self.EXPORT_FOLDERS.values()
        )

        for folder in folders:

            if not folder.exists():
                continue

            for file in folder.rglob("*"):

                if file.is_file():
                    files.append(file)

        files.sort(

            key=lambda x: x.stat().st_mtime,

            reverse=True,

        )

        return files[:limit]

    ########################################################
    # System Information
    ########################################################

    def system_information(self):

        return {

            "Python": platform.python_version(),

            "OS": platform.system(),

            "Platform": platform.platform(),

            "Working Directory": os.getcwd(),

            "Generated":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

        }

    ########################################################
    # Render
    ########################################################

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

        recent = self.recent_files()

        system = self.system_information()

        ##########################################################
        # Overall Statistics
        ##########################################################

        ##########################################################
        # Overall Statistics
        ##########################################################

        st.subheader("📊 Overall Statistics")

        row1 = st.columns(4)

        with row1[0]:
            st.metric(
                "🎥 Videos",
                stats["Videos"]["count"],
            )

        with row1[1]:
            st.metric(
                "🎵 Audio",
                stats["Audio"]["count"],
            )

        with row1[2]:
            st.metric(
                "📝 Transcripts",
                stats["Transcripts"]["count"],
            )

        with row1[3]:
            st.metric(
                "🤖 Analysis",
                stats["Analysis"]["count"],
            )

        row2 = st.columns(3)

        with row2[0]:
            st.metric(
                "📑 Reports",
                stats["Reports"]["count"],
            )

        with row2[1]:
            st.metric(
                "💬 Chats",
                stats["Chats"]["count"],
            )

        with row2[2]:
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

        for folder in [
            "Videos",
            "Audio",
            "Transcripts",
            "Analysis",
            "Reports",
            "Chats",
            "Exports",
        ]:

            total_storage += stats[folder]["size"]

        for folder in [
            "Videos",
            "Audio",
            "Transcripts",
            "Analysis",
            "Reports",
            "Chats",
            "Exports",
        ]:

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write(
                    f"**{folder}**"
                )

            with col2:

                st.write(
                    self.format_size(
                        stats[folder]["size"]
                    )
                )

        st.success(
            f"Total Storage : {self.format_size(total_storage)}"
        )

        st.divider()

        ##########################################################
        # Export Statistics
        ##########################################################

        st.subheader("📤 Export Statistics")

        export = stats["Exports"]["details"]

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            st.metric(
                "PDF",
                export["PDF"]["count"],
            )

        with c2:

            st.metric(
                "HTML",
                export["HTML"]["count"],
            )

        with c3:

            st.metric(
                "Markdown",
                export["Markdown"]["count"],
            )

        with c4:

            st.metric(
                "TXT",
                export["TXT"]["count"],
            )

        with c5:

            st.metric(
                "JSON",
                export["JSON"]["count"],
            )

        st.divider()

        ##########################################################
        # Export Statistics
        ##########################################################

        st.subheader("📤 Report Statistics")

        report = stats["Reports"]["details"]

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            st.metric(
                "PDF",
                report["PDF"]["count"],
            )

        with c2:

            st.metric(
                "HTML",
                report["HTML"]["count"],
            )

        with c3:

            st.metric(
                "Markdown",
                report["Markdown"]["count"],
            )

        with c4:

            st.metric(
                "TXT",
                report["TXT"]["count"],
            )

        with c5:

            st.metric(
                "JSON",
                report["JSON"]["count"],
            )

        st.divider()

        ##########################################################
        # Folder Statistics
        ##########################################################

        st.subheader("📂 Folder Statistics")

        table = []

        for folder in [
            "Videos",
            "Audio",
            "Transcripts",
            "Analysis",
            "Reports",
            "Chats",
            "Exports",
        ]:

            table.append(
                {
                    "Folder": folder,
                    "Files": stats[folder]["count"],
                    "Storage": self.format_size(
                        stats[folder]["size"]
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
        # Recent Files
        ##########################################################

        st.subheader("🕒 Recent Files")

        if recent:

            for file in recent:

                col1, col2, col3 = st.columns([5, 2, 2])

                with col1:

                    st.write(f"📄 {file.name}")

                with col2:

                    st.write(
                        self.format_size(
                            file.stat().st_size
                        )
                    )

                with col3:

                    st.write(
                        datetime.fromtimestamp(
                            file.stat().st_mtime
                        ).strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    )

        else:

            st.info(
                "No files available."
            )

        st.divider()

        ##########################################################
        # System Information
        ##########################################################

        st.subheader("⚙️ System Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Operating System:** {system['OS']}"
            )

            st.write(
                f"**Python Version:** {system['Python']}"
            )

            st.write(
                f"**Platform:** {system['Platform']}"
            )

        with col2:

            st.write(
                f"**Working Directory:**"
            )

            st.code(
                system["Working Directory"]
            )

            st.write(
                f"**Dashboard Generated:**"
            )

            st.success(
                system["Generated"]
            )

        st.divider()

        ##########################################################
        # Processing Statistics
        ##########################################################

        st.subheader(
            "📈 Processing Statistics"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Workflow Progress",
                f"{st.session_state.get('workflow_progress',0)}%",
            )

        with col2:

            st.metric(
                "Current Agent",
                st.session_state.get(
                    "current_agent",
                    "Idle",
                ),
            )

        with col3:

            st.metric(
                "Workflow Status",
                "Running"
                if st.session_state.get(
                    "workflow_running",
                    False,
                )
                else "Idle",
            )

        st.divider()

        ##########################################################
        # Quick Actions
        ##########################################################

        st.subheader("🚀 Quick Actions")

        c1, c2, c3 = st.columns(3)

        with c1:

            if st.button(
                "Refresh",
                use_container_width=True,
            ):

                st.rerun()

        with c2:

            if st.button(
                "Clear History",
                use_container_width=True,
            ):

                st.session_state.video_history = []
                st.session_state.report_history = []
                st.session_state.chat_history = []

                st.success(
                    "Session history cleared."
                )

        with c3:

            if st.button(
                "Reset Dashboard",
                use_container_width=True,
            ):

                st.session_state.workflow_progress = 0
                st.session_state.current_agent = "Idle"
                st.session_state.workflow_running = False

                st.success(
                    "Dashboard reset."
                )

        st.divider()

        ##########################################################
        # Export Folder Details
        ##########################################################

        st.subheader("📤 Export Folder Details")

        export = stats["Exports"]["details"]

        for name, data in export.items():
            with st.expander(
                    f"{name} ({data['count']} files)"
            ):
                st.write(
                    f"Folder : {data['path']}"
                )

                st.write(
                    f"Files : {data['count']}"
                )

                st.write(
                    f"Storage : {self.format_size(data['size'])}"
                )

        st.divider()

        ##########################################################
        # Report Folder Details
        ##########################################################

        st.subheader("📤 Report Folder Details")

        export = stats["Reports"]["details"]

        for name, data in export.items():
            with st.expander(
                    f"{name} ({data['count']} files)"
            ):
                st.write(
                    f"Folder : {data['path']}"
                )

                st.write(
                    f"Files : {data['count']}"
                )

                st.write(
                    f"Storage : {self.format_size(data['size'])}"
                )

        st.divider()

        ##########################################################
        # Folder Browser
        ##########################################################

        st.subheader("📁 Project Folders")

        folders = {}

        folders.update(self.FOLDERS)
        folders.update(self.EXPORT_FILE_FOLDERS)
        folders.update(self.REPORT_FILE_FOLDERS)

        selected_folder = st.selectbox(
            "Select Folder",
            list(folders.keys()),
        )

        folder = folders[selected_folder]

        if folder.exists():

            files = sorted(
                folder.glob("*"),
                key=lambda f: f.stat().st_mtime,
                reverse=True,
            )

            if files:

                for file in files:

                    if file.is_file():
                        col1, col2 = st.columns([5, 1])

                        with col1:
                            st.write(file.name)

                        with col2:
                            st.write(
                                self.format_size(
                                    file.stat().st_size
                                )
                            )

            else:

                st.info(
                    "Folder is empty."
                )

        else:

            st.warning(
                "Folder does not exist."
            )

        st.divider()

        ##########################################################
        # Session Information
        ##########################################################

        st.subheader("📋 Current Session")

        st.json(
            {
                "Provider": st.session_state.get(
                    "provider",
                    "N/A",
                ),
                "Model": st.session_state.get(
                    "model",
                    "N/A",
                ),
                "Workflow Progress": st.session_state.get(
                    "workflow_progress",
                    0,
                ),
                "Workflow Running": st.session_state.get(
                    "workflow_running",
                    False,
                ),
                "Current Agent": st.session_state.get(
                    "current_agent",
                    "Idle",
                ),
            }
        )

        st.divider()

        ##########################################################
        # Dashboard Summary
        ##########################################################

        st.success(
            f"""
        Dashboard Summary

        🎥 Videos       : {stats['Videos']['count']}\n
        🎵 Audio        : {stats['Audio']['count']}\n
        📝 Transcripts  : {stats['Transcripts']['count']}\n
        🤖 Analysis     : {stats['Analysis']['count']}\n
        📑 Reports      : {stats['Reports']['count']}\n
        💬 Chats        : {stats['Chats']['count']}\n
        📤 Exports      : {stats['Exports']['count']}\n

        Total Storage : {self.format_size(total_storage)}\n
                    """
        )

        FooterAgent.render()