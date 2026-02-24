# 五子棋 Android APK 构建指南

本项目已将 Pygame 版本的五子棋游戏迁移到 Kivy 框架，支持打包为 Android APK。

## 项目结构

```
D:\my_projects\lab\AI\gomoku\
├── main.py           # Kivy 版本的主程序
├── buildozer.spec    # Buildozer 打包配置文件
├── game.py           # 原始 Pygame 版本（PC端）
└── AGENTS.md         # 项目说明文档
```

## 前提条件

### 在 Windows 上构建 APK

1. **安装 Python 依赖**：
```bash
pip install kivy numpy buildozer
```

2. **安装 Java JDK**：
   - 下载并安装 [JDK 8 或更高版本](https://www.oracle.com/java/technologies/downloads/)
   - 设置环境变量 `JAVA_HOME`

3. **安装 Android SDK 和 NDK**：
   - 下载 [Android Studio](https://developer.android.com/studio)
   - 或使用 Buildozer 自动下载（推荐）

4. **其他依赖**：
   - Python 3.7+
   - Cython
   - Git

## 构建 APK

### 方法 1: 使用 Buildozer（推荐）

1. **初始化 Buildozer**：
```bash
cd D:\my_projects\lab\AI\gomoku
buildozer init
```

2. **构建 APK**：
```bash
buildozer -v android debug
```

3. **构建 Release 版本**：
```bash
buildozer android release
```

### 方法 2: 使用 python-for-android

```bash
p4a apk --private . --package=org.myapp.gomoku --name="五子棋" --version=0.1 --bootstrap=sdl2 --requirements=python3,kivy,numpy
```

## 测试应用

### 在 PC 上测试

```bash
python main.py
```

### 在 Android 设备上测试

1. 启用 USB 调试模式
2. 连接设备
3. 安装 APK：
```bash
adb install bin/gomoku-0.1-arm64-v8a-debug.apk
```

## 常见问题

### 1. 构建失败

**问题**: 缺少依赖
```bash
pip install --upgrade buildozer cython
```

**问题**: NDK 版本问题
在 `buildozer.spec` 中设置：
```
android.ndk = 25b
```

### 2. APK 安装失败

确保 Android 设备允许安装未知来源的应用。

### 3. 应用崩溃

检查 `adb logcat` 输出：
```bash
adb logcat | grep python
```

## 与原版的区别

| 特性 | Pygame 版本 | Kivy 版本 |
|------|------------|-----------|
| 平台 | PC (Windows/Linux/Mac) | Android + PC |
| 输入方式 | 鼠标 + 键盘 | 触屏 + 按钮 |
| 打包 | 无需打包 | 可打包为 APK |
| UI 库 | Pygame | Kivy |

## 游戏功能

- ✅ 15x15 标准棋盘
- ✅ 人机对战（AI 对手）
- ✅ 触屏操作
- ✅ 自动判定胜负
- ✅ 重新开始按钮
- ✅ 游戏结果弹窗

## 下一步

1. 优化 UI 界面设计
2. 添加音效
3. 实现网络对战功能
4. 添加难度选择
5. 添加悔棋功能