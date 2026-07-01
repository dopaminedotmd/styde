import sys
path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('*** ${adminToken}', 'Bearer ${adminToken}')
with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
print('Fixed')
