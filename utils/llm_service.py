from typing import List, Dict, Union
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

class LLMService:
    """大型语言模型服务类，用于处理LangChain的交互"""
    
    def __init__(self, 
                 base_url: str, 
                 api_key: str, 
                 model: str = "gpt-3.5-turbo",
                 temperature: float = 0.7) -> None:
        """
        初始化LLMService，设置连接参数
        
        参数:
            base_url (str): API端点的基础URL
            api_key (str): API认证密钥
            model (str): 模型标识符 (默认: "gpt-3.5-turbo")
            temperature (float): 采样温度 (默认: 0.7)
            
        异常:
            ValueError: 如果必要参数为空或无效
        """
        if not all([base_url, api_key, model]):
            raise ValueError("base_url, api_key 和 model 不能为空")
        if not 0 <= temperature <= 1:
            raise ValueError("温度值必须在0到1之间")

        # 创建ChatOpenAI客户端实例
        self.client = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature
        )
        
    def generate_response(self, 
                         prompt_template: str, 
                         input_variables: List[str]) -> RunnablePassthrough:
        """
        根据提示模板和变量生成单一响应
        
        参数:
            prompt_template (str): 提示的模板字符串
            input_variables (List[str]): 输入变量名称列表
            
        返回:
            RunnablePassthrough: 配置好的响应生成链
            
        异常:
            ValueError: 如果提示模板为空或输入变量无效
        """
        if not prompt_template:
            raise ValueError("提示模板不能是空值")

        # 创建提示模板
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_variables
        )
        
        # 创建并返回处理链
        chain = (
            RunnablePassthrough()
            | prompt
            | self.client
            | StrOutputParser()
        )
        return chain
    
    def generate_multi_round(self, 
                           message: Union[List[Dict], List[tuple]]) -> RunnablePassthrough:
        """
        生成多轮对话的响应
        
        参数:
            message: 包含角色和内容的字典或元组列表
            
        返回:
            RunnablePassthrough: 配置好的多轮响应生成链
            
        异常:
            ValueError: 如果消息格式无效
        """
        if not message or not isinstance(message, list):
            raise ValueError("消息必须是非空列表")
            
        # 从消息创建聊天提示模板
        prompt = ChatPromptTemplate.from_messages(message)
        
        # 创建并返回处理链
        chain = (
            RunnablePassthrough()
            | prompt
            | self.client
            | StrOutputParser()
        )
        return chain
