from flask import Flask, request, jsonify,render_template,Response
from utils.arxiv_search import search_arxiv
from utils.llm_service import LLMService
from utils.google_search import google_scholar_search

app = Flask(__name__)

# 存储模型设置的全局变量（简单起见，实际应用中应使用数据库）
model_settings = {
    "base_url": "http://183.162.252.212:11434/v1",
    "api_key": "1",
    "model": "deepseek-r1:70b"
}
model = LLMService(model_settings["base_url"], model_settings["api_key"], model_settings["model"],1)
SERPAPI_KEY = "ef6533809d34c615ee1b38ab0dd87fe1b09b4d47f667a53aabd2531ef5b45143"

@app.route('/')
def index():
    return render_template('index.html')

# 路由：处理论文搜索请求
@app.route('/api/search', methods=['POST'])
def search_papers():
    data = request.json
    print(data)
    keywords = data.get('keywords', '')
    category = data.get('category', '')
    date_range = data.get('dateRange', 'all')
    selectivityrule = data.get('selectivityrule', 'date')
    results = search_arxiv(keywords,category,date_range,selectivityrule)

    return jsonify(results)

@app.route('/api/google_scholar_search', methods=['POST'])
def google_scholar_search_route():
    """处理Google Scholar搜索请求"""
    data = request.get_json()
    keywords = data.get('keywords', '')
    max_results = data.get('maxResults', 10)
    
    results = google_scholar_search(keywords, SERPAPI_KEY, max_results)
    return jsonify(results or [])

# 路由：保存模型设置
@app.route('/api/settings', methods=['POST'])
def save_settings():
    global model_settings, model
    data = request.json
    model_settings["base_url"] = data.get("baseUrl", "")
    model_settings["api_key"] = data.get("apiKey", "")
    model_settings["model"] = data.get("model", "")
    model = LLMService(model_settings["base_url"], model_settings["api_key"], model_settings["model"],0.5)
    return jsonify({"message": "设置已保存"})

temp_message = ''

# 路由：处理translate请求
@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    message = data.get('message', '')
    prompt_template = """请将以下提供的英文论文段落翻译成中文。你的回答需要满足以下要求：
        准确性：确保翻译忠实于原文含义，不遗漏关键信息，不添加未提及的内容。
        学术规范：采用符合中文学术写作的正式语言，避免口语化表达，正确翻译专业术语。
        流畅性：翻译后的中文文本语法正确、自然通顺，适合中文母语读者阅读。
        术语处理：识别并准确翻译专业术语，若术语有特定含义，可在括号中保留英文原文或添加简短解释。
        格式清晰：直接输出中文翻译内容，不需要其他解释。
        上下文感知：根据段落内容推测可能的学术背景（如学科或研究主题），确保翻译符合相关领域惯例。
        以下是待翻译的英文论文段落：{message} 请基于上述要求进行翻译。"""
    input_variables = {"message"}
    if model_settings["base_url"] and model_settings["api_key"] and model_settings["model"]:
        chain = model.generate_response(prompt_template,input_variables)
        def generate():
            try:
                response_chunks = []
                for chunk in chain.stream(message):
                    response_chunks.append(chunk)
                    yield chunk
            except Exception as e:
                yield f"data:[Error]{str(e)}\n\n"
            finally:
                global temp_message
                if response_chunks:
                    response_chunks = ''.join(response_chunks)
                    temp_message=response_chunks.split('</think>')[1]

    else:
        reply = "请先配置模型设置！"

    return Response(generate(), content_type="text/event-stream")

# 路由：处理summarize请求
@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.json
    message = data.get('message', '')
    prompt_template = """请根据以下提供的论文段落进行总结。你的回答需要满足以下要求：
            核心提炼：提取段落的主要观点和关键信息，去除次要细节。
            简洁性：总结控制在2-4句话，确保语言精炼但信息完整。
            准确性：忠实反映段落原意，避免歪曲或添加未提及的内容。
            学术语气：使用客观、正式的语言，符合学术表达规范。
            上下文感知：根据段落内容推测可能的学术背景（如学科或研究主题），确保总结与整体语境相关。
            以下是待总结的段落：{message}。请基于上述要求提供总结。用中文进行回答。"""
    input_variables = {"message"}
    if model_settings["base_url"] and model_settings["api_key"] and model_settings["model"]:
        chain = model.generate_response(prompt_template,input_variables)
        def generate():
            try:
                response_chunks = []
                for chunk in chain.stream(message):
                    response_chunks.append(chunk)
                    yield chunk
            except Exception as e:
                yield f"data:[Error]{str(e)}\n\n"
            finally:
                global temp_message
                if response_chunks:
                    response_chunks = ''.join(response_chunks)
                    temp_message=response_chunks.split('</think>')[1]
    else:
        reply = "请先配置模型设置！"

    return Response(generate(), content_type="text/event-stream")

# 路由：处理explain请求
@app.route('/api/explain', methods=['POST'])
def explain():
    data = request.json
    message = data.get('message', '')
    prompt_template = """请根据以下提供的论文段落进行详细解释。你的回答需要满足以下要求：
                内容拆解：将段落分解为主要观点和支持细节，逐句分析其含义。
                学术背景：结合可能的学术背景或上下文（如学科领域、研究目的），推测作者意图。
                术语解释：识别并解释段落中的关键术语或专业词汇，确保清晰易懂。
                逻辑分析：说明段落中观点之间的逻辑关系，以及它们如何支持论文的整体论点。
                简明总结：在最后提供一段简洁的总结，概括段落的核心思想。
                语言风格：使用客观、学术化的语言，避免主观臆断或过于口语化的表达。
                以下是待解释的段落：{message}。请基于上述要求进行分析和解释。用中文进行回答。"""
    input_variables = {"message"}
    if model_settings["base_url"] and model_settings["api_key"] and model_settings["model"]:
        chain = model.generate_response(prompt_template,input_variables)
        def generate():
            try:
                response_chunks = []
                for chunk in chain.stream(message):
                    response_chunks.append(chunk)
                    yield chunk
            except Exception as e:
                yield f"data:[Error]{str(e)}\n\n"
            finally:
                global temp_message
                if response_chunks:
                    response_chunks = ''.join(response_chunks)
                    temp_message=response_chunks.split('</think>')[1]
    else:
        reply = "请先配置模型设置！"

    return Response(generate(), content_type="text/event-stream")


messages = [{'role':'system','content':'作为一个ai助手，你必须根据用户的输入进行回答，不可以胡编乱造。'}]

# 路由：处理multichat请求
@app.route('/api/multichat', methods=['POST'])
def multichat():
    global messages
    global temp_message
    data = request.json
    message = data.get('message', '')
    conversation_length = 5
    if message=='clear':
        messages = [{'role':'system','content':'作为一个ai助手，你必须根据用户的输入进行回答，不可以胡编乱造。'}]
        return "**论文助手**: 已经清空对话记录"
    if temp_message:
        messages.append({'role':'assistant','content':temp_message})
        temp_message = ''
    message = {'role': 'user', 'content': message}
    messages.append(message)
    if model_settings["base_url"] and model_settings["api_key"] and model_settings["model"]:
        chain = model.generate_multi_round(messages)
        def generate():
            try:
                response_chunks = []
                for chunk in chain.stream(message):
                    response_chunks.append(chunk)
                    yield chunk
            except Exception as e:
                yield f"data:[Error]{str(e)}\n\n"
            finally:
                if response_chunks:
                    messages.append({'role':'assistant','content':''.join(response_chunks)})
                    if len(messages)>conversation_length:
                        messages.pop(0)
                        messages.pop(0)
                print(messages)
    else:
        reply = "请先配置模型设置！"

    return Response(generate(), content_type="text/event-stream")
# 运行 Flask 应用
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)