import requests
import pdfplumber
from io import BytesIO

def extract_pdf_text(url, title_height=100, split_threshold=0.5, space_threshold=0.2):
    """
    增强版PDF文本提取，处理特殊空格和文本粘连
    
    新增参数:
    space_threshold (float): 字符间距阈值（相对于字符宽度）
    """
    response = requests.get(url)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)
    
    full_text = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            if page_num == 0:
                # 提取标题区域
                title_bbox = (0, 0, page.width, title_height)
                title_text = page.crop(title_bbox).extract_text()
                
                # 处理内容区域
                split_x = page.width * split_threshold
                left_bbox = (0, title_height, split_x, page.height)
                right_bbox = (split_x, title_height, page.width, page.height)
                
                left_text = process_text(page.crop(left_bbox).extract_text(), space_threshold)
                right_text = process_text(page.crop(right_bbox).extract_text(), space_threshold)
                
                full_text.append(f"{title_text}\n{left_text}\n{right_text}")
            else:
                split_x = page.width * split_threshold
                left_text = process_text(page.crop((0, 0, split_x, page.height)).extract_text(), space_threshold)
                right_text = process_text(page.crop((split_x, 0, page.width, page.height)).extract_text(), space_threshold)
                full_text.append(f"{left_text}\n{right_text}")
    
    return "\n".join(full_text).replace('\n\n\n', '\n\n')

def process_text(text, space_threshold):
    """处理文本粘连问题"""
    if not text:
        return ""
        
    processed = []
    for line in text.split('\n'):
        new_line = []
        prev_char = None
        for char in line:
            if prev_char and needs_space(prev_char, char, space_threshold):
                new_line.append(' ')
            new_line.append(char)
            prev_char = char
        processed.append(''.join(new_line))
    return '\n'.join(processed)

def needs_space(prev_char, curr_char, threshold):
    """根据字符间距判断是否需要添加空格"""
    # 这里需要根据具体PDF调整阈值逻辑
    # 示例实现基于简单字符宽度判断
    return prev_char.isalnum() and curr_char.isalnum()

if __name__ == "__main__":
    url = "https://arxiv.org/pdf/2501.00353v1.pdf"
    text = extract_pdf_text(url)
    print(text)