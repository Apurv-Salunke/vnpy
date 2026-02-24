# VSCode Development Guide

VSCode (Visual Studio Code) is a cross-platform free source code editor developed by Microsoft. Users can install extensions through the built-in extension store to expand its functionality. This document aims to provide users with a reference solution for developing VeighNa in VSCode.

This content is based on the Windows system, but most of it also applies to Linux and Mac systems.

Windows systems supported by VeighNa include:

- Windows 11
- Windows Server 2019/2022

> Other versions of Windows systems may encounter various dependency library problems during installation and are not recommended.

To use VeighNa on Windows systems, it is recommended to install the official [VeighNa Studio] Python distribution, **especially suitable for new users who are new to Python development**.


## VSCode Installation

First, download the VS Code for Windows installation package from the [VSCode official website](https://code.visualstudio.com/):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/1.png)

After downloading, double-click the installation package to enter the VSCode(User) installation wizard:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/2.png)

Select [I accept this agreement] and click [Next] to enter the Select Destination Location page for installation directory selection:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/3.png)

Click [Next] to enter the Select Start Menu Folder page for shortcut selection:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/4.png)

Click [Next] to enter the Select Additional Tasks page for additional task selection:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/5.png)

It is recommended to select all checkboxes here. The specific functions of each checkbox are as follows:

 - Checking [Add "Open with Code" action to Windows Explorer file context menu] allows users to directly open individual files in VSCode through the right-click menu;
 - Checking [Add "Open with Code" action to Windows Explorer directory context menu] allows users to directly open entire folders and their contents in VSCode through the right-click menu;
 - Checking [Register Code as an editor for supported file types] will set VSCode as the system's default editor for opening supported file types (such as .py, .txt, etc.);
 - Checking [Add to PATH (restart required)] will add the VSCode installation directory to the PATH environment variable after installation is complete.

Click [Next] to enter the Ready to Install page, which will display the installation settings content selected previously:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/6.png)

Click [Install] to start installation. After installation is complete, it will jump to the installation success page:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/7.png)

If you checked the Run Visual Studio Code option, VSCode will automatically open at this time.


## VeighNa Development

### Opening a Single File

After starting VSCode, click [Open File] in the welcome interface to open a single file, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/8.png)

In the Open File window that pops up, select the path where the file is stored, and click the [Open] button to open the file in VSCode, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/9.png)

> Please note: If you open a file in restricted mode and want to temporarily disable the restricted mode for that file, you can find the restricted mode prompt at the top of the window, click [Manage], and click [Trust] on the Workspace Trust page that pops up to disable the restricted mode for that file.

### Opening a Folder

After starting VSCode, click [Open Folder] in the welcome interface to open a folder, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/10.png)

In the Open Folder window that pops up, select the path where the folder is stored, and click the [Open] button to open the folder in VSCode, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/11.png)

### Saving VSCode Development Projects

To facilitate centralized management of code resources and avoid environment switching confusion, VSCode provides workspace support. Click [File] - [Save Workspace As...] to save the workspace to a specified path for subsequent access and use.

To solve the problem of project switching difficulties, workspaces also allow different projects to be placed in the same workspace. Click [File] - [Add Folder to Workspace...] to add folders to the workspace.

### Python Environment Selection

After installing the Python plugin, open any .py file, and you can see the currently used Python environment information in the lower right corner of the VSCode window, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/14.png)

Please note that the default display is the automatically searched Python environment. If there are multiple Python environments in the current system, you can click the Python environment information in the lower right corner, and select other environments to switch in the drop-down box that pops up at the top of the window, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/15.png)

### Running Programs

Download the VeighNa Trader [startup script file run.py](https://github.com/vnpy/vnpy/blob/master/examples/veighna_trader/run.py) from the Github code repository, open the run.py file through VSCode, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/23.png)

Click the run button in the upper right corner of VSCode and select [Run Python File] to run the run.py script:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/24.png)

At this time, in the TERMINAL terminal content output tab at the bottom of the interface, you can see the print information when the program is running:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/25.png)

At the same time, the main window of VeighNa Trader will also automatically pop up and display:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/26.png)

Please note:
 - When starting the script here, it will run in the Python environment currently used by VSCode. If you need to use other Python environments, please refer to the previous steps to switch;
 - If you want to run the script directly in the terminal, you can press Ctrl + J to open Terminal and enter the command to start VeighNa Trader;
 - The output "No data service configured to use, please modify the datafeed content in the global configuration" printed in the figure above does not affect the operation of VeighNa Trader; if you need to configure the data service, you can configure it in the VeighNa Trader main interface [Configuration] - [Global Configuration], or ignore this output if you do not need to configure the data service.

### Breakpoint Debugging

VSCode provides powerful breakpoint debugging functions. Here we use a VeighNa strategy historical backtesting script to demonstrate.

Click [New File], select [Python File] in the window that pops up at the top of the interface, and create backtest.py in the pop-up tab:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/27.png)

Then write a strategy backtesting code in the file (for details, refer to the [backtesting example](https://github.com/vnpy/vnpy/blob/master/examples/cta_backtesting/backtesting_demo.ipynb) in the Github repository), and set breakpoints where you want to pause debugging, as shown below (small red circle on the left):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/28.png)

Click the downward button in the upper right corner of VSCode and select [Python Debugger: Debug Python File] to start debugging the script:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/29.png)

Click the Run and Debug icon on the left menu bar![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/30.png) or press F5 to start debugging.

After starting debugging, you can see that the RUN AND DEBUG area on the left side of the window starts to output program run information, and the program will pause at the first breakpoint. The left side displays variable information, watch information, call stack information, and breakpoint information respectively. Click on variables to see detailed information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/31.png)

Click [Continue] similar to the play button or press F5 to continue running debugging until it pauses again at the next breakpoint, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/32.png)

At this time, you can see that the variables in the current context have changed in the VARIABLES area on the bottom left:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/33.png)

Subsequently repeat the above steps, click [Continue] until debugging ends, and you can see the corresponding output in Terminal:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/34.png)

During the debugging process:

- Click [Step Into] to enter the internal of the sub-function to view the detailed state during operation;
- Click [Step Out] to jump out of the current function and view the status of the outer call stack;
- Click [Step Over] to skip the sub-function (the sub-function will be executed);
- Click [Restart] will restart the debugging task;
- Click [Stop] will directly stop the current debugging task.

In the VARIABLES area, select the variable name you want to monitor, right-click and select [Add to Watch], and you can observe the variable changes in the WATCH monitoring area, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/35.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/36.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/37.png)

The DEBUG CONSOLE at the bottom of the window provides interactive debugging function support. You can run any command during the debugging process, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/38.png)

#### C++ Callback Breakpoint Debugging

Typically, VSCode can only perform code breakpoint debugging in threads started by the Python interpreter. If users want to set breakpoints in C++ callback functions (such as CTP API interface, PySide graphics library, etc.), they can achieve breakpoint debugging for non-Python threads (i.e., C++ threads) by setting breakpoints in the code.

Click [New File], select [Python File] in the window that pops up at the top of the interface, and create geteway_test.py.

Add a script strategy code to the successfully created geteway_test.py (refer to [this file](https://github.com/vnpy/vnpy/blob/master/examples/veighna_trader/demo_script.py)), then hold down Ctrl and click CtpGateway in the code with the left mouse button to jump to the source code of ctp_gateway.py, and set a breakpoint in the callback function you want to debug (note not to set it on the def line of the function definition). Return to gateway_test.py and start debugging, you will find that it did not enter the previously set breakpoint, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/39.png)

> Please note that if you use the load_json function to read connect_ctp.json, please ensure that the CTP account login information is configured in the json file of the corresponding .vntrader folder.

After terminating debugging, find the breakpoint previously set in ctp_gateway.py, and add the following code before the breakpoint in the callback function:

```Python 3
import pydevd
pydevd.settrace(suspend=False, trace_only_current_thread=True)
```

Please note:
 - pydevd is a debugging plugin included with VSCode, not installed in the Python environment where the Python interpreter is located;
 - After the suspend parameter is set to True, debugging will pause after this line of code finishes running, rather than stopping at the breakpoint;
 - After the trace_only_current_thread parameter is set to True, only the current thread will be monitored during debugging;
 - **Don't forget to delete this code after debugging is finished.**

Then run and debug the gateway_test.py script again. At this time, you can see that the debugging window at the bottom starts to output relevant information, and the program pauses at the breakpoint previously set. The call stack information window displays thread information (you can see an additional Dummy thread display), and the variable window displays variable information (you can see the input parameters of the callback function):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/40.png)

**Please note** that if there is no jump during the debugging process, you can click the settings button above the [Run and Debug] page, open launch.json, and set the justMyCode parameter to false to enable jumping during debugging, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/41.png)


## Plugin Installation

VSCode provides extremely rich extension plugin functions, which can significantly improve user development efficiency and convenience.

### Required Plugins

#### Python

Click the Extensions icon on the left menu bar of VSCode, search for [Python], and click [install] to install the Python plugin, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/13.png)

When installing the Python plugin, Pylance (providing type checking, code completion, reference jump, and code diagnosis support) and Python Debugger (providing breakpoint debugging functions) plugins will be automatically installed.

After installing the Python plugin, you can see the Python, Pylance, and Python Debugger plugins in the Extension bar of VSCode, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/16.png)

After installing the Pylance plugin, you can move the mouse cursor over the code in the opened script, and the corresponding document information will automatically pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/17.png)

If you click the code with the left mouse button while holding down the Ctrl key, it will jump to the declaration part of the code, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/18.png)

#### Jupyter

Click the Extensions icon on the left menu bar of VSCode, search for [Jupyter], and click [install] to install the Jupyter plugin, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/19.png)

The Jupyter plugin integrates Jupyter Notebook functionality into VSCode, allowing users to open, edit, and run Notebooks in VSCode.

When installing the Jupyter plugin, the following will be automatically installed:

- Jupyter Cell Tags (providing tag support for adding in cells);
- Jupyter Keymap (providing shortcut key support);
- Jupyter Notebook Renderers (providing rendering and parsing support for different content types);
- Jupyter Slide Show (providing slideshow support) plugins.

After installing the Jupyter plugin, you can see the Jupyter, Jupyter Cell Tags, Jupyter Keymap, Jupyter Notebook Renderers, and Jupyter Slide Show plugins in the Extension bar of VSCode, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/20.png)

#### Flake8

Click the Extensions icon on the left menu bar of VSCode, search for [Flake8], and click [install] to install the Flake8 plugin, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/21.png)

The Flake8 plugin can check whether Python code conforms to PEP 8 code style specifications, including errors in the code, constructs with excessive complexity, and places that do not conform to PEP8 style guidelines.

When the Flake8 plugin detects non-standard or erroneous code, it will display red wavy lines below the code as a warning to help users quickly locate problems, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/vscode/22.png)

At the same time, the Flake8 plugin also displays all detected errors in the entire workspace in the [PROBLEMS] tab at the bottom of the window, as shown in the figure above.

### Optional Plugins

#### Chinese Language

Function: Translates the VSCode interface and menus into Chinese, suitable for users who are not very familiar with English.

#### Excel Viewer

Function: Allows users to directly view and edit CSV files in VSCode, supporting basic cell editing, filtering, and sorting functions.

#### One Monokai Theme

Function: Provides code highlighting themes, making code easier to read and understand by changing the color, font, and background of the code.

#### Material Icon Theme

Function: Replaces the file and directory icons in VSCode with Material Design style icons, making files and directories easier to distinguish and identify in the sidebar.

#### Github Copilot

Function: An artificial intelligence code assistance tool jointly developed by GitHub and OpenAI, improving code portability and consistency.

#### C/C++ and C/C++ Extension Pack

Function: Provides C/C++ language support, code debugging, code formatting, code completion, header file inclusion, and other function support.
