# 使用 KivyLauncher 运行五子棋

## 什么是 KivyLauncher？

KivyLauncher 是一个 Android 应用，允许你在 Android 设备上直接运行 Python/Kivy 应用，无需打包 APK。

## 安装步骤

### 1. 下载 KivyLauncher

- **Google Play**: 搜索 "Kivy Launcher"
- **F-Droid**: https://f-droid.org/packages/org.kivy.kivylauncher/
- **APK 下载**: https://github.com/kivy/kivy-launcher/releases

### 2. 在 Android 设备上创建项目目录

在你的 Android 设备上创建以下目录结构：

```
/sdcard/kivy/gomoku/
├── main.py
├── android.txt (可选，配置文件)
```

### 3. 复制文件

将项目的 `main.py` 文件复制到 `/sdcard/kivy/gomoku/` 目录。

### 4. 创建 android.txt 配置文件（可选）

在 `/sdcard/kivy/gomoku/` 目录下创建 `android.txt` 文件：

```ini
title = 五子棋
author = Your Name
orientation = portrait
icon = (可选，图标文件路径)
```

### 5. 运行应用

1. 打开 KivyLauncher 应用
2. 你会看到 "gomoku" 应用图标
3. 点击图标运行游戏

## 注意事项

- **numpy 依赖**: KivyLauncher 可能不包含 numpy 库
- 如果遇到 `ModuleNotFoundError: No module named 'numpy'`，需要使用其他方案

## 优点

- 快速测试，无需打包
- 支持热更新（修改代码后重新打开应用即可）
- 无需开发环境

## 缺点

- 可能缺少某些 Python 库
- 性能不如打包后的 APK
- 不适合发布到应用商店