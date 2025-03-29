from kaiwu_agent.conf import yaml_metagent
from kaiwu_agent.utils.extool import get_global_logger, GlobalMonitor
from kaiwu_agent.utils.extool import reset_global_logger
from kaiwu_agent.main import init_agent_runtime
import random

__doc__ = (
    "This is kaiwu_agent, a algorithm libary for RL study, research or competition"
)

# 一个随机数生成器，与普通的random互不影响
random_generator = random.Random()
if yaml_metagent.exam_random_seed != "default":
    random_generator.seed(int(yaml_metagent.exam_random_seed))

# 只启动一个进程, 使用唯一的logger, 如果是采用drl模式, 则需要使用drl传递的logger和monitor即可
logger = None if yaml_metagent.aisvr_type == "drl" else get_global_logger()
monitor = None if yaml_metagent.aisvr_type == "drl" else GlobalMonitor(logger)

# 如果aisvr_type是drl, 需要从七彩石拉取配置写入configure_system.toml文件
if yaml_metagent.use_rainbow:
    from kaiwu_agent.utils.extool import GlobalRainbow

    rainbow = GlobalRainbow(logger)
    dict_data = rainbow.read_from_rainbow("main")
    rainbow.dump_dict_to_toml_file(dict_data, "main", "main_system")


# arena启动需要调用初始化
def setup(**kargs):
    # 覆盖metagent.yaml 的配置
    for k in kargs.keys():
        if k not in yaml_metagent.keys():
            raise KeyError(k)
    yaml_metagent.update(kargs)

    # 如果setup改掉默认配置，则要重新设置random_generator
    if yaml_metagent.exam_random_seed != "default":
        global random_generator
        random_generator.seed(int(yaml_metagent.exam_random_seed))


def init(agents, envs):
    if yaml_metagent.aisvr_type == "kaiwu_agent":
        return init_agent_runtime(agents[0], envs[0].game_name)
    elif yaml_metagent.aisvr_type == "drl":
        return init_agent_runtime(agents[0], envs[0].game_name)


__all__ = ["make", "random_generator", "logger", "monitor", "init"]
