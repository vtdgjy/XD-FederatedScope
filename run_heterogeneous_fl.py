import sys
sys.path.append('.')

from federatedscope.core.cmd_args import parse_args
from federatedscope.core.auxiliaries.data_builder import get_data
from federatedscope.core.auxiliaries.utils import setup_seed
from federatedscope.core.auxiliaries.logging import update_logger
from federatedscope.core.configs.config import global_cfg
from federatedscope.core.auxiliaries.runner_builder import get_runner
from federatedscope.core.auxiliaries.worker_builder import get_server_cls, get_client_cls

# 注册自定义客户端
from federatedscope.core.workers.heterogeneous_client import HeterogeneousClient

if __name__ == '__main__':
    init_cfg = global_cfg.clone()
    
    # 加载配置
    init_cfg.merge_from_file('heterogeneous_fedavg.yaml')
    
    update_logger(init_cfg, clear_before_add=True)
    setup_seed(init_cfg.seed)
    
    # 获取数据
    data, modified_cfg = get_data(config=init_cfg.clone())
    init_cfg.merge_from_other_cfg(modified_cfg)
    init_cfg.freeze()
    
    # 创建runner，使用自定义客户端类
    runner = get_runner(
        data=data,
        server_class=get_server_cls(init_cfg),
        client_class=HeterogeneousClient,  # 使用自定义客户端
        config=init_cfg.clone(),
        client_configs=None
    )
    
    # 运行联邦学习
    runner.run()