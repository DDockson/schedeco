import discord
import json
import os
import json

from discord.ext import commands
from discord import app_commands

def lastwordrulul(word):
    last = word[-1]
    if (ord(last) - 44032) % 28:
        return "을"
    else:
        return "를"
    
def lastwordiga(word):
    last = word[-1]
    if (ord(last) - 44032) % 28:
        return "이"
    else:
        return "가"

with open("token.json", "r") as f:
    TOKEN = json.load(f)["token"]
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# 저장할 폴더 경로 설정
DATA_DIR = "./userdata/"

# 폴더가 없으면 생성
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 사용자 데이터를 로드/세이브하는 함수
def load_user_data(user_id):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_user_data(user_id, data):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}!')

# 할일 그룹 커맨드 생성
task_group = app_commands.Group(name="할일", description="할 일 관리 명령어 그룹")

@task_group.command(name="추가", description="특정 프로젝트에 할 일을 추가합니다")
@app_commands.describe(project="프로젝트 이름", task="할 일 이름")
async def add_task(interaction: discord.Interaction, project: str, task: str):
    user_id = str(interaction.user.id)
    data = load_user_data(user_id)

    if project not in data:
        data[project] = {}
    data[project][task] = {}
    save_user_data(user_id, data)

    await interaction.response.send_message(f'"{project}" 프로젝트에 "{task}"{lastwordrulul(task)} 추가하였습니다!', ephemeral=True)

@task_group.command(name="조회", description="특정 프로젝트의 할 일을 조회합니다.")
@app_commands.describe(project="프로젝트 이름")
async def view_tasks(interaction: discord.Interaction, project: str = None):
    user_id = str(interaction.user.id)
    data = load_user_data(user_id)

    if not data:
        await interaction.response.send_message("현재 할 일이 없습니다.", ephemeral=True)
        return

    # 프로젝트별로 할 일 출력
    if project:
        if project in data:
            tasks = "\n".join(f"- {task} {'✅' if data[project][task].get('완료') else ''}" for task in data[project])
            await interaction.response.send_message(f'## "{project}" 프로젝트의 할 일 목록:\n{tasks}', ephemeral=True)
        else:
            await interaction.response.send_message(f'해당 프로젝트는 존재하지 않습니다.', ephemeral=True)
    else:
        response = "## 전체 프로젝트 및 할 일 목록\n"
        for proj, tasks in data.items():
            response += f'\n**{proj}**:\n'
            response += "\n".join(f"- {task} {'✅' if data[proj][task].get('완료') else ''}" for task in tasks)
        await interaction.response.send_message(response, ephemeral=True)

@task_group.command(name="삭제", description="프로젝트 또는 할 일을 삭제합니다.")
@app_commands.describe(project="프로젝트 이름", task="할 일 이름")
async def remove_task(interaction: discord.Interaction, project: str, task: str = None):
    user_id = str(interaction.user.id)
    data = load_user_data(user_id)

    if project not in data:
        await interaction.response.send_message(f'프로젝트 "{project}"를 찾을 수 없습니다.', ephemeral=True)
        return

    if task:
        if task in data[project]:
            del data[project][task]
            if not data[project]:  # 프로젝트에 할 일이 없으면 프로젝트도 삭제
                del data[project]
            save_user_data(user_id, data)
            await interaction.response.send_message(f'"{project}" 프로젝트에서 할 일 "{task}"{lastwordrulul(task)} 삭제했습니다.', ephemeral=True)
        else:
            await interaction.response.send_message(f'할 일 "{task}"{lastwordiga(task)} "{project}" 프로젝트에 없습니다.', ephemeral=True)
    else:
        del data[project]
        save_user_data(user_id, data)
        await interaction.response.send_message(f'"{project}" 프로젝트를 삭제했습니다.', ephemeral=True)

@task_group.command(name="완료", description="특정 프로젝트의 할 일을 완료로 표시합니다.")
@app_commands.describe(project="프로젝트 이름", task="할 일 이름")
async def complete_task(interaction: discord.Interaction, project: str, task: str):
    user_id = str(interaction.user.id)
    data = load_user_data(user_id)

    if project in data and task in data[project]:
        data[project][task] = {"완료": True}

        # 모든 할 일이 완료되었는지 확인
        all_tasks_completed = all(task_data.get("완료") for task_data in data[project].values())
        if all_tasks_completed:
            del data[project]

        save_user_data(user_id, data)
        if all_tasks_completed:
            await interaction.response.send_message(f'"{project}" 프로젝트의 모든 할 일이 완료되어 프로젝트를 삭제했습니다!', ephemeral=True)
        else:
            await interaction.response.send_message(f'"{project}"의 "{task}"{lastwordrulul(task)} 완료 처리했습니다!', ephemeral=True)
    else:
        await interaction.response.send_message(f'"{project}" 프로젝트 또는 할 일 "{task}"{lastwordrulul(task)} 찾을 수 없습니다.', ephemeral=True)

# 그룹 커맨드를 트리에 추가
tree.add_command(task_group)

# 봇 실행
bot.run(TOKEN)