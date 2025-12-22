import subprocess

# 使用subprocess执行脚本
cmd = [
    'python', 'manage.py', 'shell',
    '-c', 'exec(open("add_tickets.py").read())'
]

print('执行命令:', ' '.join(cmd))

result = subprocess.run(cmd, capture_output=True, text=True)

print('\n返回码:', result.returncode)
print('\n标准输出:')
print(result.stdout)

if result.stderr:
    print('\n标准错误:')
    print(result.stderr)
