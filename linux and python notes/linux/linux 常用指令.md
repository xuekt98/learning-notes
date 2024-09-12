# 1. linux 指令

</br>

# 2. conda 指令

### 2.1 创建环境
```
conda create -n EnvName python=3.10
```

### 2.2 删除环境
```
conda env remove -n EnvName
```

### 2.3 搜索可用包
```
conda search PkgName
```

### 2.4 列出已安装包的版本

列出所有包
```
conda list
```

列出指定包
```
conda list PkgName
```
### 2.5 安装包

默认安装最新的包
```
conda install PkgName
```

安装指定版本的包
```
conda install PkgName=PkgVersion 
```

</br>

# 3. pip 指令

### 3.1 pip 列出所有可用的包版本
```
pip index versions PkgName
```