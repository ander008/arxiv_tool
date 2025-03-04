import requests
from typing import List, Dict, Optional

def google_scholar_search(
    query: str,
    api_key: str,
    max_results: int = 10,
    language: str = "en"
) -> Optional[List[Dict]]:
    """
    通过SerpApi搜索Google Scholar论文并返回格式化结果
    
    参数:
        query (str): 搜索关键词
        api_key (str): SerpApi的API密钥
        max_results (int): 最大返回结果数，默认为10
        language (str): 返回结果的语言，默认为"en"（英语）
    
    返回:
        Optional[List[Dict]]: 包含论文信息的字典列表，若失败则返回None
            每个字典包含: title, abstract, authors, date, pdf_url
    
    异常:
        返回None并打印错误信息
    """
    # 输入验证
    if not query or not api_key:
        print("错误：查询关键词和API密钥不能为空")
        return None
    
    # SerpApi请求参数
    params = {
        "engine": "google_scholar",  # 指定Google Scholar引擎
        "q": query,                  # 搜索关键词
        "hl": language,              # 返回语言
        "num": max_results,          # 最大结果数
        "api_key": api_key           # SerpApi密钥
    }
    
    # 发送请求
    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()  # 检查HTTP状态码
        data = response.json()
        
        # 提取搜索结果
        organic_results = data.get("organic_results", [])
        if not organic_results:
            print("警告：未找到任何结果")
            return []
        
        # 格式化结果
        results = []
        for result in organic_results[:max_results]:  # 限制结果数
            publication_info = result.get("publication_info", {})
            authors = [author["name"] for author in publication_info.get("authors", [])]
            pdf_resource = next(
                (res for res in result.get("resources", []) if "pdf" in res.get("file_format", "").lower()),
                {}
            )
            
            formatted_result = {
                "title": result.get("title", "无标题"),
                "abstract": result.get("snippet", "无摘要"),
                "authors": authors if authors else ["未知作者"],
                "date": publication_info.get("summary", "").split(" - ")[0] if "summary" in publication_info else "未知日期",
                "pdfUrl": pdf_resource.get("link") if pdf_resource else result.get("link")
            }
            results.append(formatted_result)
        
        return results
    
    except requests.RequestException as e:
        print(f"请求错误：{str(e)}")
        return None
    except Exception as e:
        print(f"未知错误：{str(e)}")
        return None

# 示例用法
if __name__ == "__main__":
    api_key = "ef6533809d34c615ee1b38ab0dd87fe1b09b4d47f667a53aabd2531ef5b45143"  # 替换为实际密钥
    search_query = "machine learning"
    
    results = google_scholar_search(search_query, api_key, max_results=5)
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"标题: {result['title']}")
            print(f"摘要: {result['abstract']}")
            print(f"作者: {', '.join(result['authors'])}")
            print(f"日期: {result['date']}")
            print(f"PDF链接: {result['pdf_url']}")