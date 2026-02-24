# PyCharm Development Guide

PyCharm is an IDE for the Python language launched by JetBrains. It has a complete set of tools that can help users improve their efficiency when using the Python language for development. This document is intended to provide users with a reference solution for developing and using VeighNa through PyCharm.

The content in this document is based on the Windows system, but most of it also applies to Linux/Mac systems.

Windows systems supported by VeighNa include:

- Windows 10/11
- Windows Server 2019/2022

> Other versions of Windows systems may encounter various dependency library problems during installation and are not recommended.

To use VeighNa on Windows systems, it is recommended to install the official [VeighNa Studio] Python distribution, **especially for new users who are new to Python development**.


## PyCharm Installation

First, download the PyCharm Community installation package from the [PyCharm official website](https://www.jetbrains.com/pycharm/download/?section=windows#section=windows):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/1.png)

After downloading, double-click the installation package to enter the PyCharm installation wizard:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/2.png)

If you want to set installation options, you can check the relevant options on the PyCharm Community Edition Setup page:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/3.png)

After installation is complete, you will be redirected to the installation success page:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/4.png)

If you checked the Create Desktop Shortcut option to create a desktop shortcut, the PyCharm icon will appear on the desktop at this time. Double-click the icon to run PyCharm.


## VeighNa Development

### Creating a Project

After starting PyCharm, click [New Project] in the welcome interface to create a new project, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/6.png)

In the new project window that pops up, first select the folder path [Location] for storing the project, then check the [Previously configured interpreter] option in the Python interpreter option (i.e., the Python environment already installed in the current system):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/7.png)

Click [Add Local Interpreter] in the Add Interpreter drop-down box on the right, and in the dialog box that pops up, click the [System Interpreter] tab on the left, and select the path where the Python interpreter included with VeighNa Studio is located in the drop-down box that appears on the right:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/8.png)

Click the [OK] button at the bottom to save the interpreter configuration, return to the new project window, and click the [Create] button in the lower right corner to complete the creation of the new project:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/9.png)

The successfully created project window is shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/10.png)

At this time, click [External Libraries] in the upper left corner to see the external libraries that can be called in the project:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/11.png)

Click the site_packages folder and scroll down to find the vnpy core framework package and vnpy_ prefixed plugin module packages in VeighNa Studio. You can view the file source code of each package by clicking the corresponding icon, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/13.png)

Move the mouse cursor over the code, and the document information of the corresponding code will automatically pop up:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/14.png)

If you click the code with the left mouse button while holding down the Ctrl key, it will jump to the declaration part of the code:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/15.png)

Click the [Python 3.10] button in the lower right corner of the window, and the [Settings] project configuration window will pop up. You can see the package name, local version number, and latest version number installed in the current interpreter environment. Packages with an upgrade symbol (upward arrow) indicate that the current version is not the latest. Click the upgrade symbol to automatically upgrade.

> Please note: Due to VeighNa's strict version requirements for some dependency libraries, it is not recommended for users to manually upgrade installed packages to the latest version, as version conflicts may occur.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/49.png)

### Running Programs

Download the [VeighNa Trader startup script file run.py](https://github.com/vnpy/vnpy/blob/master/examples/veighna_trader/run.py) from the Github code repository and place it in the trader folder, then you can see the run.py file in the project navigation bar on the left side of the window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/16.png)

If you can see green wavy lines displayed under some code (variable name English word check), you can click the main menu button on the left of the project name - [File] - [Settings] - [Editor] - [Inspections] - [Proofreading], uncheck [Typo] and click [OK] to confirm. Then return to the main window, and you can find that the green wavy lines have disappeared:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/17.png)

Right-click and select [Run 'run'] to start running the run.py script:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/21.png)

At this time, in the terminal content output area at the bottom of the interface, you can see the print information when the program is running:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/19.png)

<span id="jump">

At the same time, the main window of VeighNa Trader will also automatically pop up and display:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/20.png)

</span>

Return to PyCharm, you can see that the run script record already exists in the upper right corner of the project interface. You can also click the triangle run button to run the script subsequently, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/18.png)


### Breakpoint Debugging

PyCharm's breakpoint debugging function is very powerful. Here we use a VeighNa strategy historical backtesting script to demonstrate.

Right-click in the project navigation bar on the left, select [New] - [File], and create backtest.py in the dialog box that pops up:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/25.png)

Then write a strategy backtesting code in the file (for details, refer to the [backtesting example](https://github.com/vnpy/vnpy/blob/master/examples/cta_backtesting/backtesting_demo.ipynb) in the Github repository), and set breakpoints where you want to debug, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/26.png)

Right-click and select [Debug 'backtest'] to start debugging the script:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/27.png)

At this time, you can see the run record of backtest.py in the upper right corner of the project interface. You can also directly start the debugging task by clicking the button here subsequently:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/28.png)

After starting debugging, you can see that the Debug window at the bottom of the main interface starts to output program run information, and the program will pause at the first breakpoint. The left side displays thread information, and the right side displays variable information in the current context:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/29.png)

Click the [Resume Program] similar to the play button to continue running debugging until it pauses again at the next breakpoint:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/30.png)

At this time, you can see that the variables in the current context have changed in the bottom right monitoring window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/31.png)

Subsequently repeat the above steps, click [Resume Program] until debugging ends, and you can see the corresponding output in the Debug window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/32.png)

After debugging, click [Rerun 'backtest'] to debug again:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/33.png)

During the debugging process, click [Step Into] to enter the internal of the function to view the detailed state during operation:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/34.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/35.png)

Click [Step Out] to jump out of the current function and view the status of the outer call stack:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/37.png)

Click [Step Over] to skip the sub-function (the sub-function will be executed):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/36.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/38.png)

Click [Stop 'backtest'] to directly stop the current program run:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/39.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/40.png)

#### Specifying Program Run Directory

When creating a new project in PyCharm, the program is run in the current directory by default. If you need to specify the directory where the program runs, you can click [Edit] in the upper right corner of the project interface to enter the [Run/Debug Configurations] interface:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/43.png)

Modify the program startup directory [Working directory]:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/44.png)

#### C++ Callback Breakpoint Debugging

Typically, PyCharm can only perform code breakpoint debugging in threads started by the Python interpreter. Previously, some users reported that they tried to set breakpoints in C++ callback functions (such as CTP API interface, PySide graphics library, etc.) but failed to take effect. In response to this situation, you can achieve breakpoint debugging for non-Python threads (i.e., C++) by setting breakpoints in the code.

Right-click in the navigation bar on the left of the project, select [New] - [File], and create geteway_test.py.

Add a script strategy code to the successfully created geteway_test.py (refer to [this file](https://github.com/vnpy/vnpy/blob/master/examples/veighna_trader/demo_script.py)), then hold down Ctrl and click CtpGateway in the code with the left mouse button to jump to the source code of ctp_gateway.py, and set a breakpoint in the callback function you want to debug (note not to set it on the def line of the function definition), as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/50.png)

Return to gateway_test.py, right-click and select [Debug 'gateway_test'] to start debugging:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/51.png)

> Please note that if you use the load_json function to read connect_ctp.json, please ensure that the CTP account login information is configured in the json file of the corresponding .vntrader folder.

At this time, you can observe that it did not enter the previously set breakpoint, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/52.png)

After terminating debugging, find the breakpoint previously set in ctp_gateway.py, and add the following code before the breakpoint in the callback function:

```Python 3
import pydevd
pydevd.settrace(suspend=False, trace_only_current_thread=True)
```

Please note:
 - pydevd is a debugging plugin included with PyCharm, not installed in the Python environment where the Python interpreter is located;
 - After the suspend parameter is set to True, debugging will pause after this line of code finishes running, rather than stopping at the breakpoint. After the trace_only_current_thread parameter is set to True, only the current thread will be monitored during debugging;
 - Don't forget to delete this code after debugging is finished.

Then run and debug the gateway_test.py script again:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/53.png)

At this time, you can see that the debugging window at the bottom starts to output relevant information, and the program pauses at the breakpoint previously set. The left side displays thread information (you can see an additional Dummy thread display), and the right side displays variable information (you can see the input parameters of the callback function):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/pycharm/54.png)


## Comparison with VS Code

1. In PyCharm, each project requires configuration of the Python environment. In VS Code, the Python environment is selected by default through the Python interpreter in the lower right corner of the window (for all open files);

2. PyCharm's Community version only provides read-only support for Jupyter, and the Professional version is required to edit and run. VS Code only needs to install functional plugins to use all Jupyter-related functions (including reading, editing, running).
