# 线性代数 MCP

这是一个可直接发布的 Python 版 MCP 服务，提供常见线性代数工具。

## 现成工具

当前版本内置 10 个工具：

1. `matrix_info`
2. `matrix_add`
3. `matrix_subtract`
4. `matrix_multiply`
5. `matrix_transpose`
6. `matrix_determinant`
7. `matrix_inverse`
8. `matrix_rank`
9. `matrix_rref`
10. `solve_linear_system`

## 为什么你之前会显示 0 个工具

你之前发布的内容，本质上只有一个启动脚本 `xiandaiMCP`，而这个脚本会再去导入 `src.server` 里的 `mcp` 实例和工具定义。
如果发布包里没有完整的 `src/server.py` 和工具函数，平台就扫不到工具，结果通常就是显示 `0 个工具`。

## 项目结构

```text
.
├── .github/workflows/release.yml
├── README.md
├── requirements.txt
├── run.py
├── xiandaiMCP
├── src
│   ├── __init__.py
│   ├── linear_algebra.py
│   └── server.py
└── tests
    └── test_linear_algebra.py
```

## 本地启动

先安装依赖：

```bash
pip install -r requirements.txt
```

### 1) stdio 模式

```bash
python run.py
```

### 2) HTTP / Streamable HTTP 模式

```bash
python run.py --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

兼容旧参数：

```bash
python run.py --http --port 8000
```

## 本地测试

```bash
python -m unittest discover -s tests -v
```

## 发布到 GitHub Release

这个项目已经附带自动打包工作流：`.github/workflows/release.yml`。

你只需要：

```bash
git add .
git commit -m "feat: add real MCP tools"
git tag v1.0.1
git push origin main --tags
```

推送 tag 后，GitHub Actions 会：

1. 运行单元测试
2. 打包完整项目为 zip
3. 创建或更新对应 Release
4. 把 zip 上传到 Release Assets

## 你在平台里应该怎么上传

重点不是“单独上传工具”，而是：

- 在 `src/server.py` 里用 `@mcp.tool` 注册工具
- 发布**完整项目压缩包**到 GitHub Release Assets
- 在你的插件平台里导入/更新这个 zip 资产，而不是只传一个启动脚本

## 建议的发布文件名

建议发布成这样的 zip：

```text
xianxingdaishu-mcp-v1.0.1.zip
```

这样平台更容易识别，也便于后续升级版本。
