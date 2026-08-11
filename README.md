# DeepRouter Editorial Print Studio

一个通过 Codex 和 DeepRouter 将照片转换为复古编辑印刷插画的 Skill。

它不是简单套用滤镜，而是先分析原图的主体、构图、色彩和画幅，再生成保留原始空间关系的日系档案印刷、Mid-century、Risograph 和手工编辑插画。

## 功能

- 支持风景、建筑、美食、饮品、人像和产品照片。
- 保持原图方向和长宽比，不强制裁成正方形。
- 根据图片类别控制主体比例、留白与不规则印刷边缘。
- 自动生成与画面内容相关的装饰元素和档案排版。
- 通过 `https://deeprouter.top/v1` 调用 OpenAI 兼容的图片接口。
- 内置提示词构建、比例验证和视觉复核工作流。

## 安装

在 GitHub 仓库页面复制仓库地址，然后执行：

```bash
git clone <repository-url> ~/.codex/skills/deeprouter-editorial-print-studio
```

如果当前 Python 环境没有依赖：

```bash
python3 -m pip install -r ~/.codex/skills/deeprouter-editorial-print-studio/requirements.txt
```

重启 Codex 后，通过以下方式调用：

```text
$deeprouter-editorial-print-studio
```

## API 配置

Skill 优先读取 `DEEPROUTER_API_KEY`，也兼容 `OPENAI_API_KEY`。请在本机环境中配置密钥，不要把密钥写入仓库、提示词或聊天消息。

```bash
export DEEPROUTER_API_KEY="your-api-key"
```

macOS 也可以通过 `launchctl` 配置：

```bash
launchctl setenv DEEPROUTER_API_KEY "your-api-key"
```

检查配置状态时只返回布尔结果，不会显示密钥：

```bash
python3 scripts/deeprouter_image.py --show-config
```

## 使用示例

上传一张有权使用的图片，然后输入：

```text
使用 $deeprouter-editorial-print-studio，把这张照片转换成复古编辑印刷插画，保持原图画幅和构图。
```

Skill 会依次执行：

```text
图片分析 -> 类型路由 -> 构图控制 -> 提示词生成 -> DeepRouter 图片编辑 -> 比例与视觉质检
```

## 隐私

使用 API 生成时，源图片和提示词会发送到 DeepRouter。请确认你有权处理和上传相关图片，并自行了解第三方服务的隐私与数据政策。

## 致谢与许可

编辑插画工作流基于 [ai-editorial-print-studio](https://github.com/liuzihe849-png/ai-editorial-print-studio) 扩展，并加入独立的 DeepRouter 图片客户端和配置流程。

本项目采用 MIT License，详情见 [LICENSE](LICENSE)。
