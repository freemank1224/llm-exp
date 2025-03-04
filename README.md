# LLM Experiment Project
This project is designed to demostrate the LLM's predict mechanism, that is, the next token prediction. 
本项目是为了演示LLM的预测工作机制而设计的，它可以演示LLM的下一个token预测特性。项目提供了命令行演示方式和网页演示方式。能够显示备选token列表及其概率。
**本项目适合纳入任何介绍LLM工作原理的课程体系中，作为互动演示软件存在，直观且可交互。**

## 项目结构

```
llm-exp/
├── README.md
├── main.py
├── model.py
├── llm-token-prediction.py
├── .gitignore
└── requirements.txt
```

## 安装

1. 克隆项目
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明
项目主要有三个文件，其中`main.py`和`model.py`两个文件共同构成网页演示程序，基于Streamlit工具实现网页显示效果。
`llm-token-prediction.py`文件，提供了从命令行运行的方式，但是只支持英文模型演示。

## 许可证
MIT
