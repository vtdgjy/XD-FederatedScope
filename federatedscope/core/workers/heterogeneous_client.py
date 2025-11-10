import torch
import logging
from federatedscope.core.workers import Client

logger = logging.getLogger(__name__)

class HeterogeneousClient(Client):
    """
    支持异构资源的客户端
    """
    def __init__(self, *args, **kwargs):
        # 先获取资源信息（在调用super之前）
        resource_info = kwargs.get('resource_info', None)
        
        # 调用父类初始化
        super(HeterogeneousClient, self).__init__(*args, **kwargs)
        
        # 处理资源信息并配置
        if resource_info:
            self.tier = resource_info.get('tier', 'unknown')
            self.gpu_memory_limit = resource_info.get('gpu_memory', 0)
            
            # 根据tier配置不同的训练策略
            self._configure_by_tier()
            
            logger.info(f"Client {self.ID}: Tier={self.tier}, "
                       f"GPU Memory={self.gpu_memory_limit}MB, "
                       f"Device={self.device}")
        else:
            self.tier = 'unknown'
            self.gpu_memory_limit = 0
    
    def _configure_by_tier(self):
        """根据层级配置训练参数"""
        try:
            if self.tier == 'tier1':
                # Tier-1: 完整训练能力，使用GPU
                if torch.cuda.is_available():
                    self.device = 'cuda:0'
                    if hasattr(self, 'model') and self.model is not None:
                        self.model.to(self.device)
                    if hasattr(self, 'trainer') and self.trainer is not None:
                        self.trainer.ctx.device = self.device
                        self.trainer.ctx.model.to(self.device)
                
            elif self.tier == 'tier2':
                # Tier-2: 使用GPU但减小batch size
                if hasattr(self, '_cfg') and hasattr(self._cfg, 'dataloader'):
                    original_bs = self._cfg.dataloader.batch_size
                    new_bs = max(original_bs // 2, 1)
                    logger.info(f"Client {self.ID} (Tier-2): "
                               f"Reducing batch size from {original_bs} to {new_bs}")
                    
                    # 重新创建dataloader（如果已经存在）
                    if hasattr(self, 'data') and self.data is not None:
                        self._cfg.defrost()
                        self._cfg.dataloader.batch_size = new_bs
                        self._cfg.freeze()
                
                if torch.cuda.is_available():
                    self.device = 'cuda:0'
                    if hasattr(self, 'model') and self.model is not None:
                        self.model.to(self.device)
                    if hasattr(self, 'trainer') and self.trainer is not None:
                        self.trainer.ctx.device = self.device
                        self.trainer.ctx.model.to(self.device)
                
            elif self.tier == 'tier3':
                # Tier-3: 使用CPU，大幅减小batch size
                if hasattr(self, '_cfg') and hasattr(self._cfg, 'dataloader'):
                    original_bs = self._cfg.dataloader.batch_size
                    new_bs = max(original_bs // 4, 1)
                    logger.info(f"Client {self.ID} (Tier-3): "
                               f"Reducing batch size from {original_bs} to {new_bs}, using CPU")
                    
                    self._cfg.defrost()
                    self._cfg.dataloader.batch_size = new_bs
                    self._cfg.freeze()
                
                # 强制使用CPU
                self.device = 'cpu'
                if hasattr(self, 'model') and self.model is not None:
                    self.model.to('cpu')
                if hasattr(self, 'trainer') and self.trainer is not None:
                    self.trainer.ctx.device = 'cpu'
                    self.trainer.ctx.model.to('cpu')
                    
        except Exception as e:
            logger.warning(f"Client {self.ID}: Error in _configure_by_tier: {e}")