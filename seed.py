"""
Seed script to populate the database with initial survey and response data.
Assumes the database tables already exist.
"""
import os
import sys
import uuid
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy import func # 导入 func 用于聚合查询
from models import Survey, Response
from config import DATABASE_URL, UPLOAD_DIR # 使用绝对导入
import random

# 创建引擎，连接到数据库
engine = create_engine(DATABASE_URL)

def seed_database():
    # 确保表结构存在 (通常在 main.py 的 startup 事件中也做了)
    # SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # 检查 Survey 表是否已有数据
        # 修正：使用 func.count 进行聚合查询
        existing_survey_count = session.exec(select(func.count(Survey.id))).one()

        if existing_survey_count > 0:
            print(f"Warning: Found {existing_survey_count} existing surveys. Skipping survey seed data insertion.")
        else:
            # 示例调查标题和描述
            sample_surveys = [
                {
                    "title": "员工满意度调查 - Q1",
                    "description": "第一季度员工对公司环境、福利和管理的满意度调查。"
                },
                {
                    "title": "年度绩效回顾",
                    "description": "对员工过去一年工作表现和成就的回顾。"
                },
                {
                    "title": "技术栈偏好调查",
                    "description": "了解团队成员对当前使用的技术栈的看法和未来技术选型的建议。"
                },
                {
                    "title": "办公室设施满意度",
                    "description": "收集员工对办公室设施（如休息区、会议室、设备）的满意度反馈。"
                },
                {
                    "title": "培训需求调查",
                    "description": "了解员工希望参加的培训课程或技能提升方向。"
                },
                {
                    "title": "工作与生活平衡调查",
                    "description": "评估员工对当前工作与生活平衡状况的看法。"
                },
                {
                    "title": "团队合作效率调查",
                    "description": "分析团队内部协作的效率和存在的问题。"
                },
                {
                    "title": "新员工入职体验",
                    "description": "了解新员工对入职流程和初期适应情况的感受。"
                },
                {
                    "title": "公司文化认知度",
                    "description": "评估员工对公司核心价值观和文化的理解和认同程度。"
                },
                {
                    "title": "健康与福利计划反馈",
                    "description": "收集员工对现有健康与福利计划的意见和建议。"
                },
                {
                    "title": "远程工作体验调查",
                    "description": "了解员工对远程工作模式的体验和偏好。"
                },
                {
                    "title": "项目管理工具使用情况",
                    "description": "评估团队对当前项目管理工具的使用效果和满意度。"
                },
                {
                    "title": "创新想法征集",
                    "description": "鼓励员工提出对公司产品、流程或服务的改进想法。"
                },
                {
                    "title": "年度最佳同事提名",
                    "description": "让员工提名他们认为表现出色、乐于助人的同事。"
                },
                {
                    "title": "职业发展路径探讨",
                    "description": "了解员工对个人职业发展的期望和公司能提供的支持。"
                },
                {
                    "title": "代码审查流程反馈",
                    "description": "收集开发者对当前代码审查流程的意见和改进建议。"
                },
                {
                    "title": "客户反馈处理效率",
                    "description": "评估团队处理和响应客户反馈的效率。"
                },
                {
                    "title": "安全意识培训效果",
                    "description": "评估最近一次安全意识培训的效果和员工的掌握情况。"
                },
                {
                    "title": "季度产品路线图讨论",
                    "description": "邀请员工对下一季度的产品开发路线图提供意见。"
                },
                {
                    "title": "年终总结与展望",
                    "description": "收集员工对过去一年的总结和对新一年的展望。"
                }
            ]

            created_surveys = []
            for survey_data in sample_surveys:
                survey = Survey(
                    title=survey_data["title"],
                    description=survey_data["description"]
                )
                session.add(survey)
                created_surveys.append(survey) # 存储以备后续创建 Response 时使用

            session.commit()
            # 刷新对象以获取数据库生成的 ID
            for survey in created_surveys:
                session.refresh(survey)
            print(f"Successfully added {len(created_surveys)} surveys to the database.")

        # 检查 Response 表是否已有数据
        existing_response_count = session.exec(select(func.count(Response.id))).one()

        if existing_response_count > 0:
            print(f"Warning: Found {existing_response_count} existing responses. Skipping response seed data insertion.")
        else:
            # 获取所有 Survey ID
            # 修正：select(Survey.id) 返回的每一项 s 就是 id 本身，不需要 s.id
            all_survey_ids = [s for s in session.exec(select(Survey.id)).all()]
            if not all_survey_ids:
                print("No surveys found to link responses to. Please seed surveys first or ensure tables exist.")
                return

            # 示例员工姓名列表
            employee_names = [
                "张伟", "王芳", "李娜", "刘洋", "陈静", "杨帆", "赵强", "黄丽", "周杰", "吴敏",
                "徐浩", "孙莉", "马超", "朱燕", "胡波", "郭涛", "何静", "高磊", "林娜", "郑凯"
            ]

            # 示例文本回复
            text_responses = [
                "非常满意，希望继续保持。",
                "有一些小建议，希望能改进。",
                "整体不错，期待更多培训机会。",
                "工作氛围很好，同事们都很棒。",
                "需要更多的资源支持。",
                "远程工作效率高，但偶尔沟通不畅。",
                "对新技术很感兴趣，希望能有学习机会。",
                "办公环境舒适，设施齐全。",
                "工作内容有挑战性，很有成就感。",
                "希望公司能提供更多的职业发展路径。",
                "团队合作默契，项目进展顺利。",
                "代码审查流程很规范，有助于提高代码质量。",
                "客户反馈处理及时，客户满意度高。",
                "安全意识培训很实用，学到了很多。",
                "对产品路线图很期待，希望能按计划推进。",
                "入职流程清晰，很快就适应了。",
                "公司文化积极向上，很有归属感。",
                "福利计划不错，但希望能有更多选择。",
                "工作与生活平衡把握得比较好。",
                "对公司未来的发展充满信心。"
            ]

            created_responses = []
            for i in range(20):
                # 随机选择一个调查、员工和回复
                survey_id = random.choice(all_survey_ids)
                employee_name = random.choice(employee_names)
                text_response = random.choice(text_responses)
                # 随机决定是否包含文件路径（模拟上传）
                file_response_path = None
                if random.choice([True, False]) and os.path.exists(UPLOAD_DIR): # 如果 UPLOAD_DIR 存在，才尝试创建文件
                     # 生成一个模拟的文件名
                     file_extension = random.choice([".txt", ".pdf", ".jpg", ".png"])
                     unique_filename = f"mock_response_{i}{file_extension}"
                     file_path = os.path.join(UPLOAD_DIR, unique_filename)
                     # 创建一个空的模拟文件
                     with open(file_path, "w") as f:
                         f.write(f"Mock file content for response {i}")
                     file_response_path = file_path
                # 随机生成一个过去几天的提交时间
                # 修正：使用 datetime.now(datetime.UTC) 替代已弃用的 datetime.utcnow()
                from datetime import timezone
                submitted_at = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))

                response = Response(
                    survey_id=survey_id,
                    employee_name=employee_name,
                    text_response=text_response,
                    file_response_path=file_response_path,
                    submitted_at=submitted_at
                )
                session.add(response)
                created_responses.append(response)

            session.commit()
            print(f"Successfully added {len(created_responses)} responses to the database.")

if __name__ == "__main__":
    seed_database()