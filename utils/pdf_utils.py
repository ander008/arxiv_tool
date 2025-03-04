import pdfplumber
import requests
from io import BytesIO

def extract_text_from_pdf(pdf_path):
    # 处理在线 PDF 链接
    if pdf_path.startswith("http"):
        response = requests.get(pdf_path)
        pdf_file = BytesIO(response.content)
    else:
        pdf_file = pdf_path

    full_text = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # 获取页面宽度和中间分隔线
            page_width = page.width
            middle_x = page_width / 2
            
            # 提取所有文本行及其位置信息
            lines = page.extract_text_lines()
            
            left_lines = []
            right_lines = []
            
            for line in lines:
                x0 = line["x0"]
                x1 = line["x1"]
                text = line["text"]
                
                # 判断文本行归属：根据文本行的中心点分配到左/右栏
                line_center = (x0 + x1) / 2
                
                if line_center < middle_x:
                    left_lines.append((line["top"], text))
                else:
                    right_lines.append((line["top"], text))
            
            # 按垂直位置（top坐标）排序，确保阅读顺序
            left_lines.sort(key=lambda x: x[0])
            right_lines.sort(key=lambda x: x[0])
            
            # 合并文本（左栏 + 右栏）
            page_text = " ".join([text for _, text in left_lines]) + " " + \
                        " ".join([text for _, text in right_lines])
            full_text.append(page_text)
    
    return "\n".join(full_text)

if __name__ == "__main__":
    # 使用示例
    pdf_url = "https://arxiv.org/pdf/2502.15680v1.pdf"  # 替换为实际PDF链接
    text = extract_text_from_pdf(pdf_url)
    print(text)