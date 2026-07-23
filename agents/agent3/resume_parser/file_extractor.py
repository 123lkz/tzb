"""
FileExtractor —— PDF/Word/TXT 文件提取为纯文本分段
"""
import os
import tempfile
from pathlib import Path
from loguru import logger

from agents.agent3.config import SUPPORTED_FILE_TYPES


class FileExtractor:
    """文件提取器：根据文件后缀分发到不同提取引擎"""

    @staticmethod
    def extract(file_path: str) -> dict[str, str]:
        """提取文件内容为分段文本

        Args:
            file_path: 简历文件路径

        Returns:
            dict[str, str]: 按段落类型分段的文本，key 为段落类型，value 为文本内容
        """
        ext = Path(file_path).suffix.lower()
        if ext not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"不支持的文件格式: {ext}，支持: {SUPPORTED_FILE_TYPES}")

        if ext == ".pdf":
            return FileExtractor._extract_pdf(file_path)
        elif ext == ".docx":
            return FileExtractor._extract_docx(file_path)
        elif ext == ".txt":
            return FileExtractor._extract_txt(file_path)
        else:
            raise ValueError(f"未处理的格式: {ext}")

    @staticmethod
    def _extract_pdf(file_path: str) -> dict[str, str]:
        """提取 PDF 文件"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            logger.warning("PyMuPDF (fitz) 未安装，请执行: pip install PyMuPDF")
            raise

        full_text = ""
        doc = fitz.open(file_path)
        for page in doc:
            full_text += page.get_text()
        doc.close()

        if not full_text.strip():
            logger.warning("PDF 文件提取文本为空")

        return {"full_text": full_text.strip()}

    @staticmethod
    def _extract_docx(file_path: str) -> dict[str, str]:
        """提取 Word 文件"""
        try:
            from docx import Document
        except ImportError:
            logger.warning("python-docx 未安装，请执行: pip install python-docx")
            raise

        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs)

        return {"full_text": full_text}

    @staticmethod
    def _extract_txt(file_path: str) -> dict[str, str]:
        """提取纯文本文件"""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            full_text = f.read()
        return {"full_text": full_text.strip()}


__all__ = ["FileExtractor"]
