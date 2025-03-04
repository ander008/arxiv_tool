// 监听折叠事件并调整聊天区大小
document.addEventListener('DOMContentLoaded', function() {
    const collapseElement = document.getElementById('settingsCollapse');
    const chatArea = document.getElementById('chatArea');
    
    // Bootstrap 折叠事件监听
    collapseElement.addEventListener('shown.bs.collapse', function() {
        adjustChatAreaHeight();
    });
    
    collapseElement.addEventListener('hidden.bs.collapse', function() {
        adjustChatAreaHeight();
    });

    // 窗口大小调整时重新计算
    window.addEventListener('resize', adjustChatAreaHeight);

    // 初始调整
    adjustChatAreaHeight();

    function adjustChatAreaHeight() {
        const sidebar = document.querySelector('.sidebar');
        const fixedElementsHeight = Array.from(sidebar.children)
            .filter(child => !child.classList.contains('chat-area'))
            .reduce((sum, child) => sum + child.offsetHeight, 0);
        
        const availableHeight = sidebar.offsetHeight - fixedElementsHeight;
        chatArea.style.height = `${availableHeight}px`;
    }
});

// 监听折叠事件并调整聊天区大小
document.addEventListener('DOMContentLoaded', function() {
    const collapseElement = document.getElementById('searchCollapse');
    const chatArea = document.getElementById('results');
    
    // Bootstrap 折叠事件监听
    collapseElement.addEventListener('shown.bs.collapse', function() {
        adjustChatAreaHeight();
    });
    
    collapseElement.addEventListener('hidden.bs.collapse', function() {
        adjustChatAreaHeight();
    });

    // 窗口大小调整时重新计算
    window.addEventListener('resize', adjustChatAreaHeight);

    // 初始调整
    adjustChatAreaHeight();

    function adjustChatAreaHeight() {
        const sidebar = document.querySelector('.sidebar');
        const fixedElementsHeight = Array.from(sidebar.children)
            .filter(child => !child.classList.contains('chat-area'))
            .reduce((sum, child) => sum + child.offsetHeight, 0);
        
        const availableHeight = sidebar.offsetHeight - fixedElementsHeight;
        chatArea.style.height = `${availableHeight}px`;
    }
});

// 搜索论文
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const keywords = document.getElementById('keywords').value;
    const category = document.getElementById('category').value;
    const dateRange = document.getElementById('dateRange').value;
    const selectivityrule = document.getElementById('selectivity-rule').value;

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords, category, dateRange ,selectivityrule})
        });
        const results = await response.json();
        displayResults(results);
    } catch (error) {
        console.error('搜索失败:', error);
        // document.getElementById('results').innerHTML = '<p class="text-danger">搜索失败，请稍后重试。</p>';
        document.getElementById('results').innerHTML = `${error}`;
    }
});


// 显示搜索结果
function displayResults(results) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';
    results.forEach((result, index) => {
        const div = document.createElement('div');
        div.className = 'mb-3';
        div.innerHTML = `
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#collapse${index}" aria-expanded="false" 
                            aria-controls="collapse${index}">
                        <p><strong>题目: </strong>${result.title}</p>
                    </button>
                </h2>
                <div id="collapse${index}" class="accordion-collapse collapse" 
                     aria-labelledby="heading${index}" data-bs-parent="#resultsAccordion">
                    <div class="accordion-body">
                        <p><strong>作者:</strong> ${result.authors}</p>
                        <p><strong>摘要:</strong> ${result.abstract}</p>
                        <p><strong>发布日期:</strong> ${result.date}</p>
                        <a href="#" class="btn btn-sm btn-outline-primary pdf-link" data-pdf="${result.pdfUrl}" target="pdfViewer">查看PDF</a>
                    </div>
                </div>
            </div>`;
        resultsContainer.appendChild(div);
    });

    document.querySelectorAll('.pdf-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pdfUrl = this.getAttribute('data-pdf');
            document.getElementById('pdfViewer').src = pdfUrl
        });
    });
}

// 保存模型设置
document.querySelector('#settingsForm button').addEventListener('click', async function() {
    const baseUrl = document.getElementById('baseUrl').value;
    const apiKey = document.getElementById('apiKey').value;
    const model = document.getElementById('model').value;

    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ baseUrl, apiKey, model })
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('保存设置失败:', error);
        alert('保存设置失败');
    }
});


// 聊天记录存储
let chatHistory = '';


document.addEventListener('DOMContentLoaded', function() {
    const collapseElements = [document.getElementById('leftSidebar'), document.getElementById('rightSidebar')];
    
    collapseElements.forEach(element => {
        element.addEventListener('shown.bs.collapse', function() {
            // 可选：调整样式或布局
        });
        element.addEventListener('hidden.bs.collapse', function() {
            // 可选：调整样式或布局
        });
    });

    window.addEventListener('resize', function() {
        // 可选：窗口调整时重新计算
    });
});


document.getElementById('pdfUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    // 验证文件类型
    if (file.type !== 'application/pdf') {
        alert('请选择有效的PDF文件');
        return;
    }
    
    // 创建对象URL
    const url = URL.createObjectURL(file);
    console.log(url);
    
    // 更新PDF查看器
    document.getElementById('pdfViewer').src = url;
    
});

document.getElementById('loadPdfLink').addEventListener('click', function() {
    const pdfLink = document.getElementById('pdfLinkInput').value.trim();
    
    if (pdfLink) {
        // 简单的URL验证
        try {
            new URL(pdfLink); // 检查是否为有效URL
            document.getElementById('pdfViewer').src = pdfLink; // 直接加载在线PDF
        } catch (e) {
            alert('请输入有效的URL链接！');
        }
    } else {
        alert('请输入PDF链接！');
    }
});

document.getElementById('chatForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const functionSelect = document.getElementById('functionSelect');
    const chatInput = document.getElementById('chatInput');
    const chatArea = document.getElementById('chatArea');
    
    const functionType = functionSelect.value;
    const message = chatInput.value.trim();
    const responseBox = document.createElement('div');
    responseBox.className = 'user-message'
    responseBox.innerHTML = marked.parse(`**你**: ${message}`);
    chatArea.appendChild(responseBox);
    chatInput.value = '';
    const answerBox = document.createElement('div');
    answerBox.className = 'bot-message';
    const thinkBox = document.createElement('div');
    thinkBox.className = 'bot-message';
    chatArea.appendChild(thinkBox);
    chatArea.appendChild(answerBox);
    if (!message) {
        alert('请输入消息！');
        return;
    }
    
    let result = '';
    switch (functionType) {
        case 'translate':
            try {
                const response = await fetch('/api/translate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message})
                });
        
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                let done = false;
                let thinkText = '';
                let thinkDone = false;
                let responseText = '\n**论文助手**:\n\n';
                
                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    const chunk = decoder.decode(value);
                    console.log(chunk);
                    if (chunk.includes('</think>')) {
                        thinkDone = true;
                    } 
                    if (thinkDone) {
                        responseText += chunk;
                    } else {
                        thinkText += chunk;
                    }
                    if (thinkDone) {
                        
                        thinkBox.innerHTML = `<details>
                        <summary>思考中...点击我折叠/展开</summary>
                        <p>${thinkText}</p>
                        </details>`
                    } else {
                        // 长度小于等于20，直接显示
                        thinkBox.innerHTML = marked.parse(thinkText);
                    }
                    if (thinkDone){
                        answerBox.innerHTML = marked.parse(responseText);
                    }
                    chatArea.scrollTop = chatArea.scrollHeight;
                }
            } catch (error) {
                console.error('聊天失败:', error);
                chatHistory += `<p><strong>错误:</strong> ${error}</p>`;
                chatArea.innerHTML = marked.parse(chatHistory);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            break;
        case 'summarize':
            try {
                const response = await fetch('/api/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message})
                });
        
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                let done = false;
                let thinkText = '';
                let thinkDone = false;
                let responseText = '\n**论文助手**:\n\n';
                
                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    const chunk = decoder.decode(value);
                    console.log(chunk);
                    if (chunk.includes('</think>')) {
                        thinkDone = true;
                    } 
                    if (thinkDone) {
                        responseText += chunk;
                    } else {
                        thinkText += chunk;
                    }
                    if (thinkDone) {
                        
                        thinkBox.innerHTML = `<details>
                        <summary>思考中...点击我折叠/展开</summary>
                        <p>${thinkText}</p>
                        </details>`
                    } else {
                        // 长度小于等于20，直接显示
                        thinkBox.innerHTML = marked.parse(thinkText);
                    }
                    if (thinkDone){
                        answerBox.innerHTML = marked.parse(responseText);
                    }
                    chatArea.scrollTop = chatArea.scrollHeight;
                }
            } catch (error) {
                console.error('聊天失败:', error);
                chatHistory += `<p><strong>错误:</strong> ${error}</p>`;
                chatArea.innerHTML = marked.parse(chatHistory);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            break;
        case 'explain':
            try {
                const response = await fetch('/api/explain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message})
                });
        
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                let done = false;
                let thinkText = '';
                let thinkDone = false;
                let responseText = '\n**论文助手**:\n\n';
                
                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    const chunk = decoder.decode(value);
                    console.log(chunk);
                    if (chunk == chunk.includes('</think>')) {
                        thinkDone = true;
                    } 
                    if (thinkDone) {
                        responseText += chunk;
                    } else {
                        thinkText += chunk;
                    }
                    if (thinkDone) {
                        
                        thinkBox.innerHTML = `<details>
                        <summary>思考中...点击我折叠/展开</summary>
                        <p>${thinkText}</p>
                        </details>`
                    } else {
                        // 长度小于等于20，直接显示
                        thinkBox.innerHTML = marked.parse(thinkText);
                    }
                    if (thinkDone){
                        answerBox.innerHTML = marked.parse(responseText);
                        
                    }
                    chatArea.scrollTop = chatArea.scrollHeight;  
                }
            } catch (error) {
                console.error('聊天失败:', error);
                chatHistory += `<p><strong>错误:</strong> ${error}</p>`;
                chatArea.innerHTML = marked.parse(chatHistory);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            break;
        case 'multichat':
            try {
                const response = await fetch('/api/multichat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message})
                });
        
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                let done = false;
                let thinkText = '';
                let thinkDone = false;
                let responseText = '\n**论文助手**:\n\n';
                
                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    const chunk = decoder.decode(value);
                    console.log(chunk);
                    if (chunk.includes('</think>')) {
                        thinkDone = true;
                    } 
                    if (thinkDone) {
                        responseText += chunk;
                    } else {
                        thinkText += chunk;
                    }
                    if (thinkDone) {
                        
                        thinkBox.innerHTML = `<details>
                        <summary>思考中...点击我折叠/展开</summary>
                        <p>${thinkText}</p>
                        </details>`
                    } else {
                        // 长度小于等于20，直接显示
                        thinkBox.innerHTML = marked.parse(thinkText);
                    }
                    if (thinkDone){
                        answerBox.innerHTML = marked.parse(responseText);
                        
                    }
                    chatArea.scrollTop = chatArea.scrollHeight; 
                }
            } catch (error) {
                console.error('聊天失败:', error);
                chatHistory += `<p><strong>错误:</strong> ${error}</p>`;
                chatArea.innerHTML = marked.parse(chatHistory);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            break;
    }
    
    // 将结果显示在聊天区域
    chatArea.innerHTML += `<div>${result}</div>`;
    chatInput.value = ''; // 清空输入框
});