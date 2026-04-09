# python3-study

python语言学习

## Requirements

- Python>=3.10

## Installation

### Install with conda

```
conda env create -f environment.yml
```

### Install requirements

1. 安装第三方依赖时, 首先要使用如下命令激活当前conda虚拟环境

```shell
conda activate extractor
```

2. 安装依赖

```
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> pip install marker-pdf==1.8.4 -i https://pypi.tuna.tsinghua.edu.cn/simple

### Notes

通过指定国内的镜像源，可以显著提高下载速度。例如，使用清华大学的镜像源：

示例：

```
pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> 这种方法可以显著提高下载速度。
