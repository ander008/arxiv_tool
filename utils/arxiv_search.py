from typing import List, Dict, Optional
import arxiv
import datetime
from arxiv import SortCriterion

def search_arxiv(
    query: str,
    category: str,
    date: str = "all",
    selectivityrule: str = "date",
    max_results: int = 20
) -> Optional[List[Dict]]:
    """
    在arXiv上搜索论文并返回格式化的结果
    
    参数:
        query (str): 搜索关键词
        category (str): 关键词查询类别
        date (str): 时间范围 ('all', 'week', 'month', 'year')
        selectivityrule (str): 排序规则 ('date' 或 'correlation')
        max_results (int): 最大返回结果数
    
    返回:
        Optional[List[Dict]]: 论文结果列表，每个结果包含标题、摘要、作者、日期和PDF链接
                             如果出错返回None
    """
    # 初始化arXiv客户端
    client = arxiv.Client()
    
    # 定义排序规则字典
    sort_rules = {
        "date": SortCriterion.SubmittedDate,
        "correlation": SortCriterion.Relevance
    }
    
    # 验证和处理排序规则
    sort_by = sort_rules.get(selectivityrule, SortCriterion.SubmittedDate)
    
    # 处理日期范围
    now = datetime.datetime.now()
    date_query = ""
    date_ranges = {
        "week": datetime.timedelta(weeks=1),
        "month": datetime.timedelta(days=30),
        "year": datetime.timedelta(days=365)
    }
    
    if date in date_ranges:
        start_date = (now - date_ranges[date]).strftime("%Y%m%d%H%M%S")
        end_date = now.strftime("%Y%m%d%H%M%S")
        date_query = f" AND submittedDate:[{start_date} TO {end_date}]"
    
    # 构造搜索查询
    full_query = f"{category}:{query}{date_query}"
    
    # 配置搜索参数
    search = arxiv.Search(
        query=full_query,
        max_results=max_results,
        sort_by=sort_by
    )
    
    # 执行搜索并格式化结果
    try:
        results = [
            {
                "title": paper.title,
                "abstract": paper.summary,
                "authors": [author.name for author in paper.authors],
                "date": paper.published,
                "pdfUrl": f"https://arxiv.org/pdf/{paper.entry_id.split('/')[-1]}.pdf"
            }
            for paper in client.results(search)
        ]
        return results
    
    except arxiv.HTTPError as e:
        print(f"arXiv API请求出错：{e}")
        return None
    except Exception as e:
        print(f"发生未知错误：{e}")
        return None

# 示例用法
if __name__ == "__main__":
    results = search_arxiv(
        query="machine learning",
        category="ti",
        date="month",
        selectivityrule="correlation",
        max_results=5
    )
    if results:
        for result in results:
            print(f"标题: {result['title']}")
            print(f"日期: {result['date']}")
            print(f"PDF: {result['pdfUrl']}\n")