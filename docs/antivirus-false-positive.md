# 杀软误报说明（下载前必读）

## 现象

从 Release 下载**单文件版** `KissScan.exe` / `PortScan.exe` 后，Windows Defender 会在下载落盘的瞬间把它删掉，提示：

```
Trojan:Win32/Wacatac.B!ml
```

## 结论：这是误报，不是病毒

- **`!ml` 后缀 = 机器学习启发式判定**（不是病毒特征库命中）。`Wacatac.B!ml` 是 PyInstaller / Nuitka 这类
  「自解压单文件打包器」最著名的误报名，GitHub 上大量正常开源工具都被它拦过——它判定的是
  "打包器 + 未签名 + 会自我解压执行" 这个**形状**，而不是代码内容。
- 本项目源码完全公开：`Kiss Scan.py`（73 行）、`端口扫描.py`（853 行），只用到
  `requests` / `socket` / `threading` / `re` / `json`，**没有任何下载执行、开机自启、持久化、
  加密勒索、进程注入类代码**。
- 可以用 Release 说明里的 **SHA256** 校验：下载物与你本地用源码构建的产物哈希一致，即证明没有夹带。

## 三种解决办法（按推荐顺序）

### 方案 1：下载 zip 版（推荐，最省事）

Release 里的 `KissScan-win-x64.zip` / `PortScan-win-x64.zip` 是 **onedir（文件夹）版**：没有自解压 stub，
**下载环节不会被拦**。

1. 下载 zip 并解压（**必须整个文件夹一起解压**，exe 依赖同目录的 `_internal`）；
2. 双击文件夹里的 `KissScan.exe` / `PortScan.exe`。

### 方案 2：自己从源码构建（最可信，零信任成本）

```bash
pip install pyinstaller pillow requests

# 文件夹版（推荐，不易误报）
pyinstaller --noconfirm --onedir --console --noupx --name KissScan "Kiss Scan.py"
pyinstaller --noconfirm --onedir --console --noupx --name PortScan "端口扫描.py"
```

甚至连打包都不用，直接跑源码：

```bash
pip install requests
python "Kiss Scan.py"
python "端口扫描.py"
```

### 方案 3：本机加白名单 / 还原被隔离的文件

1. **还原**：Windows 安全中心 → 病毒和威胁防护 → **保护历史记录** → 找到 `KissScan.exe` 那次拦截 →
   操作 → **允许**（Allow on device）；
2. **加排除目录**（管理员 PowerShell；把路径换成你放工具的位置）：
   ```powershell
   Add-MpPreference -ExclusionPath "C:\Tools\kiss-tools"
   ```
3. 只在浏览器下载项里点「保留」是不够的 —— Defender 仍会在落盘后删除，**必须先加排除**。

## 提交误报给微软（让以后的版本不再被拦）

打开 <https://www.microsoft.com/en-us/wdsi/filesubmission>，选择 **Software developer**，
上传 exe 并填写下列信息（可直接复制）：

```
Detection name : Trojan:Win32/Wacatac.B!ml
File           : KissScan.exe / PortScan.exe (PyInstaller builds)
SHA256         : <填入 Release 说明里的哈希>
Project        : https://github.com/xingGe-arch/kiss-tools  (MIT, open source)
Description    : Open-source Python recon utilities: a subdomain brute-forcer with a
                 built-in 1581-entry wordlist, and a top-1000 TCP port scanner with an
                 HTTP fingerprint pass. Full source is public (73 + 853 lines, only
                 requests / socket / threading / re). Built with PyInstaller, unsigned.
                 Requesting review of this ML heuristic false positive.
```

微软一般在 **1–3 个工作日**内调整启发式规则；规则更新后，同哈希的文件就不再被拦。

## 根治方案：给 exe 做代码签名

代码签名能显著降低 SmartScreen / Defender 的启发式怀疑：

- **付费**：OV 代码签名证书（约 ¥1000+/年）；
- **开源免费**：[SignPath.io](https://signpath.io/) 为开源项目提供免费代码签名；
  微软 [Trusted Signing](https://azure.microsoft.com/products/trusted-signing) 也有低价档。

签名后再配合上面第 1、2 条（zip 版 + 误报提交），基本可以做到"下载即用、不再报毒"。
