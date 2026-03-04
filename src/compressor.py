import os
import fitz  # PyMuPDF
from loguru import logger

class PDFCompressorService:
    @staticmethod
    def compress(input_path: str, output_path: str, compression_level: int) -> bool:
        """
        压缩指定的 PDF 文件，支持简单的内部参数控制。
        由于这是大纲级的框架脚手架，我们使用 fitz 执行标准压缩。

        :param input_path: 输入文件路径
        :param output_path: 输出文件路径
        :param compression_level: 压缩级别
        :return: bool 是否成功
        """
        try:
            doc = fitz.open(input_path)
            
            # 使用基本的优化配置进行保存（可根据具体 compression_level 定制不同的 garbage 级别或图像重采样策略）
            garbage_level = 3 if compression_level == 1 else 4
            
            doc.save(
                output_path, 
                garbage=garbage_level, 
                deflate=True, 
                clean=True
            )
            doc.close()
            return True
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}")
            return False
