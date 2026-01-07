
### 文件: `backend/README.md`

```markdown
# 调查系统后端

这是调查系统的后端部分，使用 FastAPI 和 SQLModel 构建，使用 PostgreSQL 作为数据库。

## 前置要求

*   Python 3.8+
*   PostgreSQL 服务器正在运行 (本地或远程)

## 设置 (使用 `uv`)

1.  **安装 `uv`**: 请按照 [https://github.com/astral-sh/uv#installation](https://github.com/astral-sh/uv#installation) 的说明进行安装。
2.  **导航到 `backend` 目录**。
3.  **创建并激活虚拟环境 (可选但推荐)**:
    ```bash
    # uv 会自动使用虚拟环境，但您可以根据需要显式创建一个
    # uv venv
    # source .venv/bin/activate # Linux/macOS
    # .venv\Scripts\activate.bat # Windows
    ```
4.  **安装依赖**:
    ```bash
    uv pip install fastapi uvicorn[standard] sqlmodel psycopg2-binary python-multipart
    ```
    或者，如果您有 `uv` 生成的 `requirements.txt`:
    ```bash
    uv pip sync requirements.txt
    ```
5.  **设置环境变量**: 在 `backend` 目录中创建一个 `.env` 文件，根据 `.env.example` (如果提供) 或下面的示例进行配置，并设置您的数据库连接和其他设置。

    示例 `.env` 内容:
    ```ini
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypass
    POSTGRES_DB=surveydb
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    UPLOAD_DIR=./uploads
    PUBLIC_FILE_BASE_URL=http://localhost:8000 # 供 /config/ 端点使用
    ```

## 运行应用程序

```bash
uv run uvicorn main:app --reload
```

**这将在** `http://localhost:8000` **启动服务器。**

## 设置 (使用 `venv`)

1. **导航到 `backend` **目录**** **。**
2. **创建虚拟环境** **:**
   **bash****编辑**

```
   python -m venv venv
```

1. **激活虚拟环境** **:**

* **Linux/macOS** **:**
  **bash****编辑**

    ``     source venv/bin/activate     ``

* **Windows** **:**
  **cmd****编辑**

    ``     venv\Scripts\activate.bat      # 或 PowerShell      # venv\Scripts\Activate.ps1     ``

1. **安装依赖** **:**
   **bash****编辑**

```
   pip install fastapi uvicorn[standard] sqlmodel psycopg2-binary python-multipart
```

1. **设置环境变量** **(如** `uv` **部分所述)。**
2. **运行应用程序** **(如** `uv` **部分所述)。**

## API 端点

* `GET /`: 根端点。
* `GET /config/`: 获取前端配置 (例如，文件上传基础 URL)。
* `POST /surveys/`: 创建新调查。
* `GET /surveys/`: 列出所有调查。
* `GET /surveys/{survey_id}`: 获取特定调查。
* `POST /surveys/{survey_id}/responses/`: 提交调查回复。
* `GET /surveys/{survey_id}/responses/`: 列出特定调查的所有回复。

## 功能

* **创建和管理调查。**
* **提交包含文本和文件上传的回复。**
* **将数据存储在 PostgreSQL 数据库中。**
* **从本地目录提供上传的文件。**
* **通过 API 端点向前端暴露配置。**