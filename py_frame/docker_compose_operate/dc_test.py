# docker-compose.yaml
"""
version: '3.9'
services:
  nginx:
    container_name: nginx
    environment:
    - TZ=Asia/Shanghai
    extra_hosts:
    - db.netkiller.cn:127.0.0.1
    - cache.netkiller.cn:127.0.0.1
    - api.netkiller.cn:127.0.0.1
    hostname: www.netkiller.cn
    image: nginx:latest
    ports:
    - 80:80
    - 443:443
    restart: always
    volumes:
    - /tmp:/tmp
"""
"""
安装：
pip install netkiller-devops
"""
# 以上通过python实现，以下
from netkiller.docker import Services, Composes
service = Services('nginx')
service.image('nginx:latest')
service.container_name('nginx')
service.restart('always')
service.hostname('www.netkiller.cn')
service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
service.environment(['TZ=Asia/Shanghai'])
service.ports(['77:80'])
service.volumes(['/tmp:/tmp'])
# service.debug()
# print(service.dump())

compose = Composes('development')
compose.version('3.9')
compose.services(service)
# print (compose.debug())
print(compose.dump())
compose.save()

