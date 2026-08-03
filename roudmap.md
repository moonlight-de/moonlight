# Moonlight Roadmap

> **Moonlight** — vi-like Desktop Shell для Linux.
>
> **Core:** C++20 + Qt/QML
> **Plugins:** Lua
> **Configuration:** JSON
> **Supported:** Wayland + X11
>
> ---
>
> ## Главная цель
>
> Создать полностью модульный Desktop Shell, который пользователь сможет
> собрать под себя так же, как сегодня собирают Neovim из плагинов.

---

# Version 0.0.1 — Foundation

## Repository

- [ ] Создать GitHub Repository
- [ ] LICENSE
- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] ROADMAP.md
- [ ] CODE_OF_CONDUCT.md

## Documentation

- [ ] Architecture
- [ ] Core Overview
- [ ] Plugin System
- [ ] Theme System
- [ ] Lua API
- [ ] JSON Configuration
- [ ] IPC
- [ ] Compositor Support

---

# Version 0.1.0 — Core

## Application

- [ ] Application Entry
- [ ] Logger
- [ ] Config Manager
- [ ] Event Bus
- [ ] Action Registry
- [ ] Service Manager
- [ ] Plugin Manager
- [ ] Theme Manager
- [ ] IPC Manager
- [ ] Resource Manager
- [ ] Thread Pool
- [ ] Task Scheduler
- [ ] Cache Manager

---

# Version 0.2.0 — Platform Layer

## Linux

- [ ] Wayland Backend
- [ ] X11 Backend

## Compositors

- [ ] Hyprland
- [ ] Sway
- [ ] i3
- [ ] BSPWM
- [ ] DWM
- [ ] Niri

---

# Version 0.3.0 — Linux Services

## Services

- [ ] Battery
- [ ] Audio
- [ ] Bluetooth
- [ ] Brightness
- [ ] Notifications
- [ ] Clipboard
- [ ] Wallpaper
- [ ] Window Manager
- [ ] Workspace
- [ ] Power
- [ ] Session
- [ ] Network
- [ ] MPRIS
- [ ] File Watcher

---

# Version 0.4.0 — IPC

## IPC

- [ ] IPC Server
- [ ] IPC Client
- [ ] Action Dispatcher
- [ ] CLI Communication

Commands

- [ ] moonlightctl reload
- [ ] moonlightctl plugin install
- [ ] moonlightctl plugin remove
- [ ] moonlightctl theme set
- [ ] moonlightctl doctor
- [ ] moonlightctl logs

---

# Version 0.5.0 — Plugin System

## Plugin Loader

- [ ] Lua Runtime
- [ ] Plugin Loader
- [ ] Plugin Manifest
- [ ] Plugin Permissions
- [ ] Plugin Sandbox
- [ ] Plugin API Versioning
- [ ] Hot Reload

Manifest

- [ ] plugin.json
- [ ] main.lua
- [ ] Main.qml
- [ ] README.md
- [ ] icon.png

---

# Version 0.6.0 — Moonlight SDK

## Lua API

- [ ] moon.widget
- [ ] moon.popup
- [ ] moon.window
- [ ] moon.animation
- [ ] moon.timer
- [ ] moon.process
- [ ] moon.audio
- [ ] moon.bluetooth
- [ ] moon.network
- [ ] moon.notification
- [ ] moon.workspace
- [ ] moon.window
- [ ] moon.theme
- [ ] moon.config
- [ ] moon.fs
- [ ] moon.http
- [ ] moon.dbus

---

# Version 0.7.0 — UI Framework

## Containers

- [ ] Window
- [ ] Panel
- [ ] Dock
- [ ] Desktop
- [ ] Popup
- [ ] Overlay
- [ ] Notification

## Layout

- [ ] Row
- [ ] Column
- [ ] Grid
- [ ] Stack
- [ ] Overlay
- [ ] Center
- [ ] Padding
- [ ] Margin
- [ ] Spacer

---

# Version 0.8.0 — Animation System

Animations

- [ ] Fade
- [ ] Scale
- [ ] Rotate
- [ ] Slide
- [ ] Blur
- [ ] Bounce
- [ ] Spring
- [ ] Bezier
- [ ] Elastic

---

# Version 0.9.0 — Theme System

## Theme

- [ ] Colors
- [ ] Radius
- [ ] Blur
- [ ] Opacity
- [ ] Shadows
- [ ] Icons
- [ ] Fonts
- [ ] Animation Tokens
- [ ] Spacing
- [ ] liquid glass

Theme Manager

- [ ] Live Reload
- [ ] Theme Import
- [ ] Theme Export

---

# Version 1.0.0 — Default Plugins

## Official Plugins

- [ ] Status Bar
- [ ] Dock
- [ ] Launcher
- [ ] Notification Center
- [ ] Control Center
- [ ] Desktop Widgets
- [ ] Workspace Switcher
- [ ] Lock Screen
- [ ] Power Menu
- [ ] Clipboard Manager
- [ ] Dashboard

---

# Version 1.1.0 — Widgets

Official Widgets

- [ ] Clock
- [ ] Calendar
- [ ] Weather
- [ ] Battery
- [ ] CPU
- [ ] GPU
- [ ] RAM
- [ ] Storage
- [ ] Network
- [ ] Bluetooth
- [ ] Spotify
- [ ] MPRIS
- [ ] GitHub
- [ ] Docker
- [ ] Todo

---

# Version 1.2.0 — Vi-like Navigation

Navigation

- [ ] Focus Manager
- [ ] Modes
- [ ] hjkl Navigation
- [ ] Command Palette
- [ ] Search
- [ ] Leader Key
- [ ] Mouse Support

---

# Version 1.3.0 — Desktop

Desktop

- [ ] Desktop Icons
- [ ] Desktop Widgets
- [ ] Drag & Drop
- [ ] Widget Resize
- [ ] Widget Snap
- [ ] Widget Layers

---

# Version 1.4.0 — Configuration

JSON

- [ ] Import
- [ ] Export
- [ ] Backup
- [ ] Version History
- [ ] Validation
- [ ] Auto Migration

---

# Version 1.5.0 — Plugin Manager

Plugin Manager

- [ ] Install
- [ ] Remove
- [ ] Update
- [ ] Rollback
- [ ] Dependencies
- [ ] Lazy Loading

---

# Version 1.6.0 — Marketplace

Marketplace

- [ ] Plugins
- [ ] Themes
- [ ] Widgets
- [ ] Wallpapers
- [ ] Icons
- [ ] Configurations

---

# Version 1.7.0 — Wallpapers

Wallpaper Engine

- [ ] Static Wallpapers
- [ ] Video Wallpapers
- [ ] QML Wallpapers
- [ ] Lua Wallpapers
- [ ] Wallpaper API

---

# Version 1.8.0 — Cloud

Moonlight Cloud

- [ ] Login
- [ ] Sync
- [ ] Backup
- [ ] Restore
- [ ] Config Sharing

Profile

- [ ] Avatar
- [ ] Banner
- [ ] Username
- [ ] Public Configurations

---

# Version 1.9.0 — Community

Community

- [ ] Plugin Publishing
- [ ] Theme Publishing
- [ ] Widget Publishing
- [ ] Wallpaper Publishing
- [ ] Reviews
- [ ] Ratings

---

# Version 2.0.0 — Stable Release

Release

- [ ] Stable API
- [ ] Stable SDK
- [ ] Stable Plugin System
- [ ] Documentation
- [ ] Website
- [ ] Examples
- [ ] Benchmarks
- [ ] Packaging

Supported Packages

- [ ] Arch

---

# Future

- [ ] Multi Monitor Improvements
- [ ] Wayland Protocol Extensions
- [ ] AI Assistant
- [ ] Lua LSP
- [ ] Visual Widget Builder
- [ ] Visual Theme Builder
- [ ] Visual Animation Editor

---

# Philosophy

- Core должен быть минимальным.
- Всё должно быть модульным.
- Любую часть системы можно заменить.
- Все действия доступны через Action API.
- Lua отвечает за логику.
- QML отвечает за интерфейс.
- C++ отвечает за производительность.
- JSON отвечает за конфигурацию.
- Пользователь должен иметь полный контроль над системой.
