import jieba.analyse as jal
import time
import datetime

detail = '''岗位职责】

1. 可独立或协助完成地产行业满意度、神秘客调研项目的研究方案，制定调研计划，设计调研问卷；

2. 运用数据挖掘/统计学习的理论和方法，根据已有数据完成各类地产项目的数据分析报告；

3. 根据数据挖掘结果，协助撰写满意度、神秘客研究报告，提出相关建议和意见；

4. 完成领导临时交办的其他事情及配合其他同事完成调研工作。



【任职要求】

1. 计算机、统计学、数学、心理学等相关专业大专以上学历，1年以上数据分析或市场调研工作经验，有能力者可不考虑具体经验；

2. 具备市场分析、市场调研研究方法等知识；

3. 精通excel，尤其是熟练使用办公自动化软件，熟练使用spss等数理统计及分析工具；

4. 良好的数据敏感度，逻辑思维能力强，能够举一反三，能制作数据分析报告；

5. 快速的学习能力，良好的沟通能力，简练的文字表达能力，较强的思维逻辑和分析能力、数据处理能力；

6. 乐于在充满能量的团队里工作，极具细心耐心品质，对工作压力有一定的承受能力以及良好的适应力
'''
job_details_fenci = jal.extract_tags(detail, topK=10)
print(job_details_fenci)

stamp = time.time()
last_day = stamp - 60*60*24
last_day_tupel = time.localtime(last_day)
print(time.strftime('%Y-%m-%d %H:%M:%S', last_day_tupel))

last_day = datetime.date.today()-datetime.timedelta(days=1)
print(str(last_day))