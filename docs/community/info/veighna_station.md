# VeighNa Station

## Starting the Program

### Launch by Clicking Icon

After successful installation, double-click the VeighNa Station shortcut on the desktop:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/1.png)

to run VeighNa Station.

### Launch via Command Line

Open the command line tool, enter veighna and press Enter to run, and VeighNa Station will start.

## User Login

When using VeighNa Station for the first time, a VeighNa Studio disclaimer will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/2.png)

After reading carefully and clicking [Confirm], a user login interface containing a username input box, password input box, login button, and register button will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/3.png)

The user enters the username in the username input box and the password in the password input box according to the requirements, then clicks the [Login] button to complete the login and enter the VeighNa Station main program.

New users can click the [Register] button to register an account, and log in after registration. Please note during registration:

- Personal email should be filled in truthfully (used for password retrieval and other forum functions later);
- Username automatically uses the WeChat [nickname] at the time of registration (does not support modification);
- Please remember the password, as this password is also used to log in to the VeighNa community forum.

**The login interface only pops up when running VeighNa Station for the first time**. VeighNa Station will automatically log in when running subsequently.

## Interface Window

After login is complete, the VeighNa Station interface will automatically pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/4.png)

The interface is mainly divided into several parts: menu bar, title bar, function bar, main display area, learning and usage area, and official channel area.

### Menu Bar

The menu bar is located at the top and contains two buttons: [System] and [Help].

#### Configuration

Click [System] - [Configuration], and a system configuration window will pop up. You can modify the PyPI index and pip proxy, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/5.png)

The PyPI index is used to change the pypiserver address used by VeighNa Station. When left blank, the default PyPI server https://pypi.org is used.

The pip proxy is empty by default, and users can set it themselves. After modification, click the [Save] button to save the configuration and exit the window.

#### Logout

Click [System] - [Logout], and a logout window will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/6.png)

Click [Yes] to log out the user and immediately close the program. After the user logs out, they need to log in again when starting next time.

#### Close

Click [System] - [Close], and an exit window will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/7.png)

Click [Yes] to immediately close the program.


### Main Window

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/9.png)

As shown in the figure above, the left area of the figure is the function bar, and the right area is the main display area. The function bar includes community, trading, investment research, encryption, updates, and other content. With different selections in the function bar on the left, the main display area on the right will display corresponding content.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/10.png)

As shown in the figure above, the bottom left corner of the VeighNa Station interface is the learning and usage area.

Clicking [User Documentation] will open a browser and jump to the official documentation https://www.vnpy.com/docs/cn/index.html, where users can query detailed usage instructions.

Clicking [Community Help] will open a browser and jump to the official forum https://www.vnpy.com/forum/, where users can query technical posts and post for discussion.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/11.png)

As shown in the figure above, below the learning and usage area is the official channel area.

From left to right are the official Github repository, official WeChat public account, and official Zhihu account. Click to open the browser and jump directly to the relevant page.


## Function Usage

### Community

Click the [Community] button on the left side of VeighNa Station, and the right main display area displays the official forum content, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/4.png)

Users can browse official forum content in this area.

### Trading

Click the [Trading] button on the left side of VeighNa Station, and the right main display area displays the trading interface, application module selection area, and information output area, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/12.png)

Click the white checkbox after the trading interface or application module you want to load to select. Then click the [Start] button in the lower left corner of the main display area to start VeighNa Trader. At this time, the output area on the right will output information during program operation, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/13.png)

Click the [Modify] button in the lower right corner of the main display area to modify the run directory.

### Investment Research

Click the [Investment Research] button on the left side of VeighNa Station, and the right main display area is the jupyterlab application operation directory, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/14.png)

After clicking the [Start] button in the lower left corner of the main display area, the jupyterlab application will run in the run directory specified in the lower right corner. You can perform investment research operations in the jupyterlab application, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/15.png)

### Encryption

Click the [Encryption] button on the left side of VeighNa Station, and the right main display area displays encryption-related content, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/16.png)

Users can compile selected .py files into .pyd files in this interface to encrypt strategies.

Click the [Select] button, select the strategy file path to be encrypted in the pop-up window, and click the [Open] button. At this time, the input bar in the lower left corner of the main display area will change to the absolute path of the file to be encrypted, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/17.png)

Click the [Encrypt] button to compile the file. At this time, the central display area will output relevant information during the encryption process, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/18.png)

After the output file encryption process terminates, an encrypted pyd file will be generated at the location of the encrypted file.

Please note that after encryption, you need to **remove the .cp310-win_amd64 part from the pyd file name** first, and then put it in the self-built strategies folder.

### Updates

Click the [Updates] button on the left side of VeighNa Station, and the right main display area displays component update-related content, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/19.png)

Click the [Check] button in the lower left corner of the main display area to display locally installed modules and versions, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/20.png)

Click the [Update] button in the lower right corner of the main display area, and the background will start the update process and output relevant information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/veighna_station/21.png)

After the update is complete, a notification window will pop up. Click [OK] and restart VeighNa Station.
