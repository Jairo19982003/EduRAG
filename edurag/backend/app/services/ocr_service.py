"""
OCR Service for Scanned PDFs
Handles text extraction from image-based PDFs using Tesseract OCR
"""

import os
import logging
from typing import Tuple, Dict, Optional
from pathlib import Path
import tempfile

try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("OCR dependencies not installed. Scanned PDF support disabled.")

import pdfplumber

logger = logging.getLogger(__name__)


def is_scanned_pdf(file_path: str, sample_pages: int = 3) -> bool:
    """
    Detecta si un PDF es escaneado (imagen) o digital (texto seleccionable)
    
    Args:
        file_path: Ruta al archivo PDF
        sample_pages: Número de páginas a muestrear
        
    Returns:
        True si es PDF escaneado, False si tiene texto seleccionable
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            pages_to_check = min(sample_pages, len(pdf.pages))
            
            for i in range(pages_to_check):
                page_text = pdf.pages[i].extract_text()
                
                # Si alguna página tiene más de 50 caracteres de texto, es digital
                if page_text and len(page_text.strip()) > 50:
                    return False
            
            # Si ninguna página tiene texto significativo, es escaneado
            return True
            
    except Exception as e:
        logger.error(f"Error detecting PDF type: {str(e)}")
        return False


async def extract_text_with_ocr(file_path: str) -> Tuple[str, Dict]:
    """
    Extrae texto de PDF escaneado usando OCR
    
    Args:
        file_path: Ruta al archivo PDF
        
    Returns:
        Tuple de (texto_extraído, metadata)
    """
    if not OCR_AVAILABLE:
        raise RuntimeError(
            "OCR not available. Install: pip install pytesseract pdf2image Pillow\n"
            "Also install Tesseract: https://github.com/tesseract-ocr/tesseract"
        )
    
    try:
        logger.info(f"Starting OCR extraction for: {file_path}")
        
        # Convertir PDF a imágenes
        images = convert_from_path(file_path, dpi=300)
        
        text_content = []
        metadata = {
            "total_pages": len(images),
            "extraction_method": "pytesseract_ocr",
            "ocr_language": "spa+eng",  # Español + Inglés
            "page_breaks": [],
            "ocr_confidence": []
        }
        
        for page_num, image in enumerate(images, 1):
            logger.info(f"Processing page {page_num}/{len(images)} with OCR")
            
            # Extraer texto con OCR
            # Configuración para español e inglés
            custom_config = r'--oem 3 --psm 6 -l spa+eng'
            page_text = pytesseract.image_to_string(image, config=custom_config)
            
            # Obtener confianza del OCR (opcional)
            try:
                ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_config)
                confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                metadata["ocr_confidence"].append({
                    "page": page_num,
                    "confidence": round(avg_confidence, 2)
                })
            except Exception as e:
                logger.warning(f"Could not get OCR confidence for page {page_num}: {str(e)}")
            
            # Agregar texto de la página
            if page_text and page_text.strip():
                current_length = sum(len(t) for t in text_content)
                metadata["page_breaks"].append({
                    "page": page_num,
                    "char_position": current_length
                })
                
                text_content.append(f"\n\n--- Página {page_num} ---\n\n")
                text_content.append(page_text)
            else:
                logger.warning(f"No text extracted from page {page_num}")
        
        full_text = "".join(text_content)
        metadata["total_chars"] = len(full_text)
        metadata["avg_confidence"] = round(
            sum(p["confidence"] for p in metadata["ocr_confidence"]) / len(metadata["ocr_confidence"])
            if metadata["ocr_confidence"] else 0,
            2
        )
        
        logger.info(f"OCR extraction completed: {len(full_text)} chars, avg confidence: {metadata['avg_confidence']}%")
        
        return full_text, metadata
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        raise RuntimeError(f"Failed to extract text with OCR: {str(e)}")


async def extract_text_smart(file_path: str) -> Tuple[str, Dict]:
    """
    Extrae texto de PDF automáticamente detectando si es escaneado o digital
    
    Args:
        file_path: Ruta al archivo PDF
        
    Returns:
        Tuple de (texto_extraído, metadata)
    """
    try:
        # Detectar tipo de PDF
        is_scanned = is_scanned_pdf(file_path)
        
        if is_scanned:
            logger.info(f"Detected scanned PDF: {file_path}")
            if not OCR_AVAILABLE:
                raise RuntimeError(
                    "PDF appears to be scanned but OCR is not available. "
                    "Install: pip install pytesseract pdf2image Pillow"
                )
            return await extract_text_with_ocr(file_path)
        else:
            logger.info(f"Detected digital PDF: {file_path}")
            # Usar método existente de pdfplumber
            from app.services.pdf_processor import extract_text_from_pdf
            return await extract_text_from_pdf(file_path)
            
    except Exception as e:
        logger.error(f"Smart text extraction failed: {str(e)}")
        raise


def check_ocr_availability() -> Dict[str, bool]:
    """
    Verifica si OCR está disponible y configurado correctamente
    
    Returns:
        Dict con status de componentes OCR
    """
    status = {
        "pytesseract_installed": False,
        "pdf2image_installed": False,
        "pillow_installed": False,
        "tesseract_executable": False,
        "ocr_ready": False
    }
    
    try:
        import pytesseract
        status["pytesseract_installed"] = True
        
        # Verificar que Tesseract esté instalado en el sistema
        try:
            pytesseract.get_tesseract_version()
            status["tesseract_executable"] = True
        except:
            pass
            
    except ImportError:
        pass
    
    try:
        import pdf2image
        status["pdf2image_installed"] = True
    except ImportError:
        pass
    
    try:
        import PIL
        status["pillow_installed"] = True
    except ImportError:
        pass
    
    # OCR está listo si todos los componentes están disponibles
    status["ocr_ready"] = all([
        status["pytesseract_installed"],
        status["pdf2image_installed"],
        status["pillow_installed"],
        status["tesseract_executable"]
    ])
    
    return status
