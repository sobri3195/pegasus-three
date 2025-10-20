"""
Metadata Extractor Module - Extract metadata from various file types
"""

import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import PyPDF2
import json

class MetadataExtractor:
    def __init__(self, config):
        self.config = config
        
    def extract(self, file_path):
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        extractors = {
            '.jpg': self.extract_image_metadata,
            '.jpeg': self.extract_image_metadata,
            '.png': self.extract_image_metadata,
            '.gif': self.extract_image_metadata,
            '.pdf': self.extract_pdf_metadata,
            '.docx': self.extract_document_metadata,
            '.xlsx': self.extract_document_metadata
        }
        
        extractor = extractors.get(file_extension, self.extract_generic_metadata)
        
        results = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'file_type': file_extension,
            'timestamp': datetime.now().isoformat(),
            'basic_info': self.get_basic_file_info(file_path),
            'hashes': self.compute_hashes(file_path),
            'mime_signature': self.detect_mime_signature(file_path),
            'entropy': self.compute_entropy(file_path),
            'metadata': extractor(file_path)
        }
        
        return results
    
    def get_basic_file_info(self, file_path):
        stat_info = os.stat(file_path)
        
        return {
            'size': stat_info.st_size,
            'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            'accessed': datetime.fromtimestamp(stat_info.st_atime).isoformat()
        }
    
    def extract_image_metadata(self, file_path):
        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            
            metadata = {}
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    if tag == 'GPSInfo':
                        gps_data = {}
                        for gps_tag_id in value:
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag] = value[gps_tag_id]
                        
                        metadata['GPS'] = gps_data
                        metadata['Location'] = self.get_coordinates(gps_data)
                    else:
                        metadata[tag] = str(value)
            else:
                metadata['message'] = 'No EXIF data found'
            
            metadata['Image_Size'] = f"{image.width}x{image.height}"
            metadata['Image_Format'] = image.format
            metadata['Image_Mode'] = image.mode
            metadata['Orientation'] = exif_data.get(274) if exif_data else None
            metadata['Histogram'] = self.color_histogram_summary(image)
            
            return metadata
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_coordinates(self, gps_data):
        try:
            def convert_to_degrees(value):
                d, m, s = value
                return d + (m / 60.0) + (s / 3600.0)
            
            lat = convert_to_degrees(gps_data.get('GPSLatitude', [0, 0, 0]))
            lon = convert_to_degrees(gps_data.get('GPSLongitude', [0, 0, 0]))
            
            if gps_data.get('GPSLatitudeRef') == 'S':
                lat = -lat
            if gps_data.get('GPSLongitudeRef') == 'W':
                lon = -lon
            
            return {
                'latitude': lat,
                'longitude': lon,
                'maps_url': f'https://maps.google.com/?q={lat},{lon}',
                'accuracy_estimate': 'unknown'
            }
        except Exception:
            return None
    
    def extract_pdf_metadata(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                
                metadata = pdf.metadata
                embedded = self.detect_pdf_embedded_files(pdf)
                
                info = {
                    'pages': len(pdf.pages),
                    'embedded_files': embedded
                }
                
                if metadata:
                    info.update({
                        'title': metadata.get('/Title', 'N/A'),
                        'author': metadata.get('/Author', 'N/A'),
                        'subject': metadata.get('/Subject', 'N/A'),
                        'creator': metadata.get('/Creator', 'N/A'),
                        'producer': metadata.get('/Producer', 'N/A'),
                        'creation_date': metadata.get('/CreationDate', 'N/A'),
                        'modification_date': metadata.get('/ModDate', 'N/A')
                    })
                else:
                    info['message'] = 'No metadata found'
                
                return info
                    
        except Exception as e:
            return {'error': str(e)}
    
    def extract_document_metadata(self, file_path):
        try:
            if file_path.endswith('.docx'):
                from docx import Document
                doc = Document(file_path)
                core_properties = doc.core_properties
                
                return {
                    'author': core_properties.author,
                    'title': core_properties.title,
                    'subject': core_properties.subject,
                    'keywords': core_properties.keywords,
                    'created': str(core_properties.created),
                    'modified': str(core_properties.modified),
                    'last_modified_by': core_properties.last_modified_by,
                    'revision': core_properties.revision
                }
            else:
                return {'message': 'Document type not fully supported'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def extract_generic_metadata(self, file_path):
        return {
            'message': 'Generic metadata extraction',
            'file_info': self.get_basic_file_info(file_path)
        }
    
    def extract_all_metadata(self, directory):
        results = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                results.append(self.extract(file_path))
        
        return results
    
    def compute_hashes(self, file_path):
        import hashlib
        hashes = {'md5': None, 'sha1': None, 'sha256': None}
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                hashes['md5'] = hashlib.md5(data).hexdigest()
                hashes['sha1'] = hashlib.sha1(data).hexdigest()
                hashes['sha256'] = hashlib.sha256(data).hexdigest()
        except Exception as e:
            hashes['error'] = str(e)
        return hashes
    
    def detect_mime_signature(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
            sig = header.hex()
            mime = 'application/octet-stream'
            if header.startswith(b'\xFF\xD8'):
                mime = 'image/jpeg'
            elif header.startswith(b'\x89PNG'):
                mime = 'image/png'
            elif header.startswith(b'%PDF'):
                mime = 'application/pdf'
            return {'signature': sig, 'mime': mime}
        except Exception as e:
            return {'error': str(e)}
    
    def compute_entropy(self, file_path):
        try:
            import math
            from collections import Counter
            with open(file_path, 'rb') as f:
                data = f.read()
            counts = Counter(data)
            total = len(data) if data else 1
            entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
            return round(entropy, 4)
        except Exception as e:
            return {'error': str(e)}
    
    def color_histogram_summary(self, image):
        try:
            hist = image.histogram()
            return hist[:10]  # sample first 10 bins for brevity
        except Exception:
            return None
    
    def detect_pdf_embedded_files(self, pdf_reader):
        try:
            if '/Names' in pdf_reader.trailer['/Root'] and '/EmbeddedFiles' in pdf_reader.trailer['/Root']['/Names']:
                return True
        except Exception:
            pass
        return False
