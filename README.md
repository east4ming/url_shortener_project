## .env 文件的使用与配置

在许多现代Web开发框架和项目中，如Vue.js、Laravel、FastAdmin以及Node.js应用中，`.env` 文件被用来存储敏感信息和环境特定的变量，这些变量不会提交到版本控制系统（如Git），以确保安全性和灵活性。

### 步骤说明

#### 1. 创建或复制 `.env.sample` 文件
通常项目初始化时会提供一个名为 `.env.sample` 的文件，它包含了项目的默认环境变量模板。按照以下步骤操作：

复制模板：将 `.env.sample` 文件复制一份，并重命名为 `.env`。

```bash
cp .env.sample .env
```

#### 2. 配置环境变量

打开 `.env` 文件，您会看到一系列以 `VARIABLE_NAME=value` 格式排列的键值对。例如：

```dotenv
ENV_NAME="Development"
BASE_URL="http://localhost:8000"
DB_URL="sqlite:////./shortener.sqlite"
```

#### 3. 替换默认值

根据您的实际部署环境，替换每个变量对应的值。例如，如果您需要设置数据库凭据，将 `DB_USERNAME` 和 `DB_PASSWORD` 分别替换为实际的用户名和密码。

#### 4. 环境特定配置

对于不同环境（如本地开发、测试、预生产及生产环境），您可以创建多个 `.env` 文件，如 `.env.development`、`.env.test`、.`env.staging` 和 `.env.production`。框架一般会通过环境变量或其他方式识别当前运行环境并加载相应的 `.env` 文件。

#### 5. 应用程序加载 .env 文件

大多数支持 `.env` 文件的框架都会自动加载该文件，将其中的变量注入到应用程序环境中供代码引用。

### 🐾注意事项

* 不要将包含**敏感信息**（如API密钥、密码）的 `.env` 文件提交到版本控制仓库。
* 在团队协作中，确保每个人都正确设置了各自的环境变量。
* 对于不同的环境，务必保持环境变量的一致性，避免因环境差异导致的问题。

### 示例

```dotenv
ENV_NAME="Development"
BASE_URL="http://localhost:8000"
DB_URL="sqlite:////./shortener.sqlite"
```

请根据项目文档具体指导进行配置，并确保所设置的环境变量能够满足项目运行的需求。
