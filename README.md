# Readme
此仓库保存了论文中第四章和第五章所涉及的模型和代码。运行方式和参考视频如下：

## 运行环境 
Python 3.8
PIP 21.2.3
- For Python dependencies, please, check `requirements.txt` or `environment.yml`
- For external tools: **Java 1.8**
- Java dependencies alongside with others are located at `external_tools` folder
  - [SplitMiner](https://apromore.com/research-lab/) (v1, 2, 3)
## char5原始模型
文件夹中为第五章提到的叶轮快速制造系统仿真模型Model.doe，在Arena中运行后在C:\Users\123\Documents\mould\output\txt中输出事件记录文件  
## char5事件日志生成
文件夹中为第五章提到的文档处理及BPMN模型生成代码。运行main.py文件即可，分割算法的参数可以在splitminer.py中进行调整。运行后在C:\Users\123\Documents\mould\output中bpmn格式流程模型及xes格式事件日志文件  
## char4&5离散事件仿真模型
生成通过读取bpmn模型和xes文件生成Arena离散事件仿真模型，并自动执行和诊断模型一致性和资源配置问题。直接运行menu.py上传bpmn模型即可。  

实例视频：https://www.loom.com/share/ac883c428a1b40c2a4441e2426e3705c?sid=7ab85ae8-1ca2-4715-b837-eb714571e367
