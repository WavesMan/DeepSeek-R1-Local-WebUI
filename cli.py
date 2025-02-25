#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess
import functools
from pathlib import Path
from typing import Tuple, Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
from dotenv import load_dotenv
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Confirm

# 环境配置
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')
console = Console()

# ====================
# 版本控制模块（增强版）
# ====================
class VersionController:
    _session = requests.Session()
    _retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    _session.mount('https://', HTTPAdapter(max_retries=_retries))

    @staticmethod
    def get_local_version() -> Optional[str]:
        """增强的版本文件解析"""
        version_file = BASE_DIR / ".version"
        try:
            content = version_file.read_text(encoding="utf-8")
            if match := re.search(r"version\s*=\s*['\"](.*?)['\"]", content):
                return match.group(1).strip()
            console.print(f"[red]× 版本文件格式错误: {version_file}[/]")
            return None
        except Exception as e:
            console.print(f"[red]× 无法读取版本文件: {str(e)}[/]")
            return None

    @classmethod
    def get_remote_version(cls) -> Tuple[Optional[str], Optional[str]]:
        """带重试机制的版本获取"""
        api_url = "https://api.github.com/repos/WavesMan/DeepSeek-R1-Local-WebUI/releases/latest"
        try:
            response = cls._session.get(api_url, timeout=(3.05, 9))
            response.raise_for_status()
            data = response.json()
            return data["tag_name"].strip(), data.get("body", "").strip()
        except requests.RequestException as e:
            console.print(f"[red]× 检查更新失败: {str(e)}[/]")
            return None, None

    @staticmethod
    def compare_versions(local: str, remote: str) -> bool:
        """健壮的版本比较"""
        def safe_parse(v: str) -> Tuple[int, ...]:
            cleaned = re.sub(r"[^\d.]", "", v)
            parts = cleaned.split('.') if cleaned else ['0']
            try:
                return tuple(map(int, parts))
            except ValueError:
                return (0,)
        return safe_parse(remote) > safe_parse(local)

    @classmethod
    def check_update(cls) -> Tuple[bool, str, str]:
        """带错误处理的更新检查"""
        try:
            if not (local := cls.get_local_version()):
                return False, "", ""
            
            remote, notes = cls.get_remote_version()
            if not remote:
                return False, "", ""
            
            return cls.compare_versions(local, remote), local, remote
        except Exception as e:
            console.print(f"[red]更新检查异常: {str(e)}[/]")
            return False, "", ""

    @staticmethod
    def perform_update() -> bool:
        """增强的更新操作"""
        try:
            result = subprocess.run(
                ["git", "pull", "--autostash"],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                check=True
            )
            console.print(Panel.fit(
                f"[green]✓ 更新成功[/]\n[dim]{result.stdout}[/]",
                title="系统更新",
                border_style="green",
                padding=(1, 2)
            ))
            return True
        except subprocess.CalledProcessError as e:
            console.print(Panel.fit(
                f"[red]× 更新失败 {e.returncode}[/]\n"
                f"[white]{e.stderr}[/]",
                title="错误",
                border_style="red",
                padding=(1, 2)
            ))
            return False

# ====================
# 主应用类（优化版）
# ====================
class DeepSeekCLI:
    def __init__(self):
        self.menu_stack = []
        self.menu_structure = self.init_menu_structure()

    def error_handler(func):
        """错误处理装饰器"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.show_error_panel(e)
                self.menu_stack = []
                return None
        return wrapper

    def init_menu_structure(self):
        """完整的菜单结构"""
        return [
            {
                "id": "system",
                "name": "🛠️ 系统维护",
                "children": [
                    {
                        "id": "install",
                        "name": "📦 安装依赖",
                        "action": self.install_dependencies
                    },
                    {
                        "id": "update",
                        "name": "🔄 检查更新",
                        "action": self.enhanced_update_system
                    }
                ]
            },
            {
                "id": "model",
                "name": "🤖 模型管理",
                "children": [
                    {
                        "id": "download",
                        "name": "⬇️ 下载模型",
                        "action": self.download_model
                    },
                    {
                        "id": "delete",
                        "name": "🗑️ 删除模型", 
                        "action": self.delete_model
                    },
                    {
                        "id": "open_dir",
                        "name": "📂 模型目录",
                        "action": self.open_model_dir
                    }
                ]
            },
            {
                "id": "service",
                "name": "🚀 模型服务",
                "children": [
                    {
                        "id": "start",
                        "name": "▶️ 启动服务",
                        "action": self.run_service
                    },
                    {
                        "id": "config",
                        "name": "⚙️ 服务配置",
                        "action": self.service_config
                    }
                ]
            }
        ]

    def get_current_menu(self):
        """安全获取当前菜单层级"""
        current = self.menu_structure
        for idx in self.menu_stack:
            if isinstance(current, list) and 0 <= idx < len(current):
                current = current[idx].get("children", [])
            else:
                raise IndexError("菜单路径损坏")
        return current

    def clear_screen(self):
        """清屏函数"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu_header(self):
        """显示带路径的菜单标题"""
        path_names = []
        temp_menu = self.menu_structure
        for idx in self.menu_stack:
            if isinstance(temp_menu, list) and 0 <= idx < len(temp_menu):
                path_names.append(temp_menu[idx]["name"])
                temp_menu = temp_menu[idx].get("children", [])
        
        title = "DeepSeek-R1 控制台"
        if path_names:
            title = " > ".join(path_names)
        
        console.print(
            Panel.fit(
                f"[bold cyan]{title}[/]",
                border_style="blue"
            )
        )

    def build_menu_choices(self):
        """构建菜单选项"""
        current_menu = self.get_current_menu()
        choices = []
        for idx, item in enumerate(current_menu):
            choice = questionary.Choice(
                title=item.get("name", "未命名选项"),
                value={
                    "type": "item",
                    "index": idx,
                    "action": item.get("action"),
                    "children": item.get("children")
                }
            )
            choices.append(choice)
            
        # 添加返回选项
        if self.menu_stack:
            choices.append(questionary.Choice(
                "↩️ 返回上一级", 
                value={"type": "back"}
            ))
        else:
            choices.append(questionary.Choice(
                "🚪 退出系统", 
                value={"type": "exit"}
            ))
            
        return choices

    def show_current_menu(self):
        """显示当前层级的菜单"""
        while True:
            try:
                self.clear_screen()
                self.show_menu_header()
                
                choices = self.build_menu_choices()
                selected = questionary.select(
                    "请选择操作:",
                    choices=choices,
                    qmark=" ",
                    pointer="👉",
                    style=questionary.Style([
                        ('selected', 'fg:#00ff00 bold'),
                        ('qmark', 'fg:#ff0000 bold'),
                    ])
                ).ask()

                if not selected:
                    continue

                # 处理返回/退出
                if selected["type"] == "back":
                    if self.menu_stack:
                        self.menu_stack.pop()
                    return
                elif selected["type"] == "exit":
                    self.exit_app()
                    return
                
                # 处理菜单项选择
                if selected["children"]:
                    self.menu_stack.append(selected["index"])
                elif selected["action"]:
                    selected["action"]()
                    
            except Exception as e:
                self.show_error_panel(e)
                return

    def show_error_panel(self, error):
        """显示错误信息面板"""
        error_msg = f"[bold red]{type(error).__name__}:[/] {str(error)}"
        if isinstance(error, (IndexError, TypeError)):
            error_msg += "\n[dim]可能原因: 菜单配置损坏或程序更新不完整[/]"
        elif "version" in str(error).lower():
            error_msg += "\n[dim]建议检查.version文件格式[/]"
        elif "git" in str(error).lower():
            error_msg += "\n[dim]请确认Git已安装且有写入权限[/]"
            
        console.print(
            Panel.fit(
                error_msg,
                title="[bold white on red] 系统错误 [/]",
                border_style="red",
                padding=(1, 2)
            )
        )
        input("\n按回车键返回主菜单...")

    @error_handler
    def install_dependencies(self):
        """安装依赖"""
        from install_dependencies import interactive_install
        interactive_install()

    @error_handler
    def download_model(self):
        """下载模型"""
        from scripts.model_downloader import interactive_download
        interactive_download()

    @error_handler 
    def delete_model(self):
        """删除模型"""
        models_dir = BASE_DIR / "models"
        if not models_dir.exists():
            raise FileNotFoundError(f"模型目录不存在: {models_dir}")

        choices = [
            questionary.Choice(f.name, value=f)
            for f in models_dir.iterdir()
            if f.is_dir()
        ]
        
        selected = questionary.select(
            "\n".join([
                f"\n按 Ctrl+C 返回上一级",
                f"选择要删除的模型:"
            ]),
            choices=choices,
            qmark="⚠️"
        ).ask()
        
        if selected and questionary.confirm(f"确认永久删除 {selected.name}?", default=False).ask():
            shutil.rmtree(selected)
            console.print(f"[bold green]✅ 已删除: {selected.name}[/]")
            input("\n按回车键返回...")

    @error_handler
    def run_service(self):
        """启动模型服务"""
        model_path = self.select_model()
        if not model_path:
            return
            
        from core.model_manager import ModelManager
        from flask import Flask
        
        with console.status("[bold cyan]正在加载模型...[/]", spinner="dots"):
            model_mgr = ModelManager(model_path)
            
        app = Flask(__name__,
            static_url_path='/static',
            static_folder=str(BASE_DIR / 'static'),
            template_folder=str(BASE_DIR / 'templates')
        )
        
        from web.routes import create_routes
        app.register_blueprint(create_routes(model_mgr))
        
        console.print(
            Panel.fit(
                "\n".join([
                    f"[green]已加载模型 {os.getenv('MODEL_NAME')}[/]",
                    f"[green]服务已启动: http://{os.getenv('WEBUI_HOST', '127.0.0.1')}:{os.getenv('WEBUI_PORT', 5000)}[/]",
                    f"[green]按 Ctrl+C 退出服务[/]"
                ]),
                title="[bold]服务信息[/]",
                border_style="green",
                padding=(1, 4)
            )
        )
        app.run(
            host=os.getenv('WEBUI_HOST', '127.0.0.1'),
            port=int(os.getenv('WEBUI_PORT', 5000)),
            debug=False
        )

    def select_model(self):
        """模型选择"""
        models_dir = BASE_DIR / "models"
        if not models_dir.exists():
            raise FileNotFoundError(f"模型目录不存在: {models_dir}")

        choices = [
            questionary.Choice(f.name, value=models_dir / f.name)
            for f in models_dir.iterdir()
            if f.is_dir()
        ]
        choices.append(questionary.Choice("↩️ 取消操作", value=None))

        selected = questionary.select(
            "选择要加载的模型:",
            choices=choices,
            qmark="🤖"
        ).ask()
        
        return selected

    def open_model_dir(self):
        """打开模型目录"""
        models_dir = BASE_DIR / "models"
        if not models_dir.exists():
            models_dir.mkdir()
            
        if sys.platform == 'win32':
            os.startfile(models_dir)
        else:
            os.system(f'open "{models_dir}"' if sys.platform == 'darwin' else f'xdg-open "{models_dir}"')
        
        console.print(f"[bold green]✅ 已打开模型目录: {models_dir}[/]")
        input("\n按回车键返回...")

    def service_config(self):
        """服务配置（整合新版配置系统）"""
        from config import WEBUI_CONFIG
        
        # 获取当前配置
        current_host = WEBUI_CONFIG.host
        current_port = WEBUI_CONFIG.port

        # 交互式输入
        new_host = questionary.text(
            f"输入服务地址（当前: {current_host}）:",
            default=current_host
        ).ask()

        new_port = questionary.text(
            f"输入服务端口（当前: {current_port}）:",
            default=str(current_port),
            validate=lambda val: val.isdigit() and 0 < int(val) < 65535
        ).ask()

        # 更新配置
        WEBUI_CONFIG.host = new_host
        WEBUI_CONFIG.port = int(new_port)
        
        try:
            WEBUI_CONFIG.save()
            console.print(
                Panel.fit(
                    f"[bold green]✓ 配置更新成功[/]\n",
                    # f"[bold red]✓ 更新需要重新启动Cli[/]\n"
                    f"[dim]新地址: {new_host}:{new_port}[/]",
                    border_style="green",
                    padding=(1, 2)
                )
            )
        except Exception as e:
            console.print(
                Panel.fit(
                    f"[red]× 配置保存失败[/]\n{str(e)}",
                    border_style="red",
                    padding=(1, 2)
                )
            )
        
        input("\n按回车键返回...")

    def enhanced_update_system(self):
        """完全修复的更新流程"""
        try:
            with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                transient=True,
                console=console
            ) as progress:
                task = progress.add_task("[cyan]检查更新...", total=3)
                
                # 获取版本信息
                progress.update(task, advance=1, description="[cyan]读取本地版本")
                local_version = VersionController.get_local_version()
                if not local_version:
                    progress.update(task, completed=3)
                    return

                progress.update(task, advance=1, description="[cyan]获取远程信息")
                remote_version, release_notes = VersionController.get_remote_version()
                if not remote_version:
                    progress.update(task, completed=3)
                    return

                # 版本比较
                progress.update(task, advance=1, description="[cyan]分析差异")
                needs_update = VersionController.compare_versions(local_version, remote_version)
                progress.update(task, completed=3)

            # 显示结果
            if needs_update:
                console.print(Panel.fit(
                    f"[bold green]新版本 {remote_version}[/]\n"
                    f"[dim]当前版本: {local_version}[/]\n\n"
                    f"{release_notes or '暂无更新说明'}",
                    title="更新可用",
                    border_style="green",
                    padding=(1, 4)
                ))
                if Confirm.ask("[yellow]是否立即执行更新？[/]"):
                    if VersionController.perform_update():
                        console.print("[bold green]✓ 请重启应用完成更新[/]")
                        Confirm.ask("[yellow]按回车键退出...[/]")
                        sys.exit(0)
            else:
                console.print(
                    Panel.fit(
                        f"[bold green]✓ 已是最新版本 ({local_version})[/]",
                        border_style="green",
                        padding=(1, 2)
                    )
                )
            Confirm.ask("[dim]是否返回...[/]")

        except Exception as e:
            self.show_error_panel(e)

    def exit_app(self):
        """退出程序"""
        console.print(
            Panel.fit(
                "[bold cyan]👋 感谢使用，再见！[/]",
                border_style="blue"
            )
        )
        sys.exit(0)

if __name__ == '__main__':
    try:
        cli = DeepSeekCLI()
        while True:
            cli.show_current_menu()
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]致命错误:[/]\n{str(e)}",
                title="[blink]系统崩溃[/]",
                border_style="red",
                padding=1
            )
        )
        sys.exit(1)