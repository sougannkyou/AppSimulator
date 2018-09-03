import os

APPSIMULATOR_MODE = os.getenv('APPSIMULATOR_MODE')  # multi or single
LOCAL_IP = os.getenv('APPSIMULATOR_IP')
WORK_PATH = os.getenv('APPSIMULATOR_WORK_PATH')
SCOPE_TIMES = 1 * 60

GB = 1024 * 1024 * 1024

# ---------------------- 模拟器屏幕尺寸 -----------------------------
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 480

# ---------------------- db -----------------------------
MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

REDIS_SERVER = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/11'

# ---------------------- status -----------------------------
STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'  # wait

STATUS_DOCKER_RUN = 'docker_run'  # docker running(create and run) ...
STATUS_DOCKER_RUN_OK = 'docker_run_ok'
STATUS_DOCKER_RUN_NG = 'docker_run_ng'

STATUS_SCRIPT_START = 'script_start'  # script running ...
STATUS_SCRIPT_START_OK = 'script_start_ok'
STATUS_SCRIPT_START_NG = 'script_start_ng'
STATUS_SCRIPT_SUSPEND = 'script_suspend'  # task interrupt
STATUS_SCRIPT_RUN_OK = 'script_run_ok'  # task run complete
STATUS_SCRIPT_RUN_NG = 'script_run_ng'  # script运行时间累计3次小于预期

LIVE_CYCLE_NEVER = 'never'
LIVE_CYCLE_ONCE = 'once'

MODE_SINGLE = 'single'
MODE_MULTI = 'multi'

TIMER_ON = 'on'
TIMER_OFF = 'off'
# ---------------------- rpc -----------------------------
RPC_SERVER_TIMEOUT = 30
RPC_PORT = 8003

# ---------------------- adb -----------------------------
NOX_BIN_PATH = 'C:\\Nox\\bin'
NOX_BACKUP_PATH = 'C:\\Nox\\backup'
ADB_BINARY_PATH = NOX_BIN_PATH + '\\nox_adb.exe'
CONSOLE_BINARY_PATH = NOX_BIN_PATH + '\\NoxConsole.exe'
TIMER = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]

# ---------------------- VMware -----------------------------
VMRUN_BINARY_PATH = 'C:\\VMware\\Workstation\\vmrun.exe'
VM_IMAGES_PATH = 'C:\\VMware\\VM'
VMX_NAME = 'Windows 7 x64.vmx'
VM_MAX = 5

# ---------------------- FTP -----------------------------
FTP_SERVER_IP = '172.16.253.37'
FTP_USER_NAME = 'zhxg'
FTP_PASSWORD = 'zhxg2018'

# ---------------------- ControllerManager -----------------------------
CHECK_TIMES = 10  # min

# --------------------- Android KeyCode -----------------------------
KEYCODE_CALL = 5  # 拨号键
KEYCODE_ENDCALL = 6  # 挂机键
KEYCODE_HOME = 3  # 按键Home
KEYCODE_MENU = 82  # 菜单键
KEYCODE_BACK = 4  # 返回键
KEYCODE_SEARCH = 84  # 搜索键
KEYCODE_CAMERA = 27  # 拍照键
KEYCODE_FOCUS = 80  # 拍照对焦键
KEYCODE_POWER = 26  # 电源键
KEYCODE_NOTIFICATION = 83  # 通知键
KEYCODE_MUTE = 91  # 话筒静音键
KEYCODE_VOLUME_MUTE = 164  # 扬声器静音键
KEYCODE_VOLUME_UP = 24  # 音量增加键
KEYCODE_VOLUME_DOWN = 25  # 音量减小键

KEYCODE_ENTER = 66  # 回车键
KEYCODE_ESCAPE = 111  # ESC键
KEYCODE_DPAD_CENTER = 23  # 导航键 确定键
KEYCODE_DPAD_UP = 19  # 导航键 向上
KEYCODE_DPAD_DOWN = 20  # 导航键 向下
KEYCODE_DPAD_LEFT = 21  # 导航键 向左
KEYCODE_DPAD_RIGHT = 22  # 导航键 向右
KEYCODE_MOVE_HOME = 122  # 光标移动到开始键
KEYCODE_MOVE_END = 123  # 光标移动到末尾键
KEYCODE_PAGE_UP = 92  # 向上翻页键
KEYCODE_PAGE_DOWN = 93  # 向下翻页键
KEYCODE_DEL = 67  # 退格键
KEYCODE_FORWARD_DEL = 112  # 删除键
KEYCODE_INSERT = 124  # 插入键
KEYCODE_TAB = 61  # Tab键
KEYCODE_NUM_LOCK = 143  # 小键盘锁
KEYCODE_CAPS_LOCK = 115  # 大写锁定键
KEYCODE_BREAK = 121  # Break/Pause键
KEYCODE_SCROLL_LOCK = 116  # 滚动锁定键
KEYCODE_ZOOM_IN = 168  # 放大键
KEYCODE_ZOOM_OUT = 169  # 缩小键
