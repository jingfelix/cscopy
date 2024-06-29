# cscopy

cscopy 是一个 Cscope 的 Python 封装，旨在提供简单易用的接口来搜索 C 代码中的符号。它允许用户在一个临时的工作空间中对 C 代码进行索引和搜索，适合需要在不同项目或代码库中快速查找符号定义和引用的场景。

## 特性

- **临时工作空间**：支持自动创建临时文件夹，将需要追踪的文件复制进这个文件夹，并在其中运行 Cscope。
- **简单的 API**：提供了简单直观的 API 来搜索符号的定义、引用等。

## 安装

确保你的系统中已安装 Python 3 和 cscope。然后，使用 pip 或你喜欢的包管理器安装 cscopy：

```bash
pip install cscopy
# or
pdm add cscopy
```

## 快速开始

以下是一个简单的示例，展示了如何使用 cscopy 来搜索 C 代码中符号的定义：

```python
from cscopy.cli import CscopeCLI
from cscopy.model import SearchType
from cscopy.workspace import CscopeWorkspace

# 初始化 CscopeCLI
cli = CscopeCLI(path="/usr/bin/cscope")

# 创建一个 CscopeWorkspace 实例
with CscopeWorkspace(files=["c_code/exit.c"], cli=cli) as workspace:
    print(workspace.tempdir_path)

    # 搜索符号 "exit" 的定义
    res = workspace.search(mode=SearchType.C_SYMBOL, symbol="exit")
    # equals to
    # res = workspace.search_c_symbol("exit")


    # 打印搜索结果
    for r in res:
        print(r.line, r.parent)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
