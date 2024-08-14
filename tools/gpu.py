import subprocess


def get_gpu_info():
    try:
        # 运行nvidia-smi命令并捕获其输出
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # 假设每行GPU信息以"GPU "开头，这里简化处理，实际可能需要更复杂的解析
        gpus = []
        for line in output.split("\n"):
            if line.startswith("GPU "):
                # 假设' GPU 0: '这样的格式，然后我们可以提取GPU编号和状态
                gpu_info = line.split()
                gpu_id = gpu_info[1].split(":")[0]
                # 尝试找到利用率信息，这可能在不同的输出格式中有所不同
                # 这里假设利用率在'  %d%%'这样的格式中
                utilization = None
                for word in gpu_info:
                    if "%" in word and "C" not in word:  # 忽略CPU使用率
                        utilization = word.strip("%").split("%")[0]
                        break
                gpus.append({"id": gpu_id, "utilization": utilization})

        return gpus
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return []


# 调用函数并打印结果
gpu_infos = get_gpu_info()
for gpu in gpu_infos:
    print(f"GPU {gpu['id']}: Utilization {gpu['utilization']}% if available")
