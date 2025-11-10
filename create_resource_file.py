import pickle

# 定义三层级客户端资源信息
resource_info = {
    # Tier-1: 强算力客户端 (2个, ID: 0-1)
    0: {
        'computation': 50.0,      # 计算速度 (ms/sample)
        'communication': 1000.0,  # 网络带宽 (Mbps)
        'gpu_memory': 8192,       # 8GB显存
        'tier': 'tier1'
    },
    1: {
        'computation': 50.0,
        'communication': 1000.0,
        'gpu_memory': 8192,
        'tier': 'tier1'
    },
    
    # Tier-2: 中等算力客户端 (3个, ID: 2-4)
    2: {
        'computation': 150.0,     # 计算速度降低
        'communication': 100.0,   # 100Mbps带宽
        'gpu_memory': 4096,       # 4GB显存
        'tier': 'tier2'
    },
    3: {
        'computation': 150.0,
        'communication': 100.0,
        'gpu_memory': 4096,
        'tier': 'tier2'
    },
    4: {
        'computation': 150.0,
        'communication': 100.0,
        'gpu_memory': 4096,
        'tier': 'tier2'
    },
    
    # Tier-3: 弱算力客户端 (5个, ID: 5-9)
    5: {
        'computation': 800.0,     # CPU计算更慢
        'communication': 50.0,    # 10-50Mbps带宽
        'gpu_memory': 0,          # 无GPU
        'tier': 'tier3'
    },
    6: {
        'computation': 900.0,
        'communication': 30.0,
        'gpu_memory': 0,
        'tier': 'tier3'
    },
    7: {
        'computation': 850.0,
        'communication': 40.0,
        'gpu_memory': 0,
        'tier': 'tier3'
    },
    8: {
        'computation': 950.0,
        'communication': 20.0,
        'gpu_memory': 0,
        'tier': 'tier3'
    },
    9: {
        'computation': 880.0,
        'communication': 25.0,
        'gpu_memory': 0,
        'tier': 'tier3'
    },
}

# 保存为pickle文件
with open('client_heterogeneous_config.pkl', 'wb') as f:
    pickle.dump(resource_info, f)

print("资源配置文件已创建！")